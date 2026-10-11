import { Duration, RemovalPolicy, Stack } from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subs from 'aws-cdk-lib/aws-sns-subscriptions';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import { Construct } from 'constructs';
import { pyFn } from './common';
import { Data } from './data';
import { Layers } from './layers';

export const STATE_MACHINE_NAME = 'wristheat-escalation';

export interface EscalationProps {
  buildDir: string;
  data: Data;
  layers: Layers;
  siteId: string;
  ackTimeoutSeconds: number;
  supervisorEmail?: string;
  backupEmail?: string;
  bedrockModelId: string;
  dashboardUrl: string;
}

/** Step Functions escalation: Notify → WaitForAck → (Escalate → WaitForAckAfterEscalation) → WaitForRecovery → Close. */
export class Escalation extends Construct {
  readonly stateMachine: sfn.StateMachine;
  readonly stateMachineArn: string;
  readonly functions: lambda.Function[] = [];

  constructor(scope: Construct, id: string, props: EscalationProps) {
    super(scope, id);
    const { data } = props;
    const stack = Stack.of(this);
    this.stateMachineArn = `arn:aws:states:${stack.region}:${stack.account}:stateMachine:${STATE_MACHINE_NAME}`;

    const supervisor = new sns.Topic(this, 'Supervisor', { topicName: 'wristheat-supervisor' });
    const backup = new sns.Topic(this, 'Backup', { topicName: 'wristheat-backup' });
    if (props.supervisorEmail) supervisor.addSubscription(new subs.EmailSubscription(props.supervisorEmail));
    if (props.backupEmail) backup.addSubscription(new subs.EmailSubscription(props.backupEmail));

    const env = {
      ...data.tableEnv(),
      SITE_ID: props.siteId,
      SUPERVISOR_TOPIC_ARN: supervisor.topicArn,
      BACKUP_TOPIC_ARN: backup.topicArn,
      AUDIO_BUCKET: data.audioBucket.bucketName,
      DASHBOARD_URL: props.dashboardUrl,
      BEDROCK_MODEL_ID: props.bedrockModelId,
    };
    const fn = (name: string, timeout = 30) => {
      const f = pyFn(this, `${name}Fn`, {
        buildDir: props.buildDir,
        handler: `wristheat.handlers.esc_${name.toLowerCase()}.handler`,
        layers: [props.layers.core],
        timeout: Duration.seconds(timeout),
        environment: env,
      });
      data.incidents.grantReadWriteData(f);
      for (const t of [data.sites, data.trainees, data.sessions, data.minutes]) t.grantReadData(f);
      this.functions.push(f);
      return f;
    };
    const notifyFn = fn('Notify', 60);
    const registerFn = fn('Register');
    const escalateFn = fn('Escalate');
    const closeFn = fn('Close', 60);

    notifyFn.addToRolePolicy(new iam.PolicyStatement({ actions: ['polly:SynthesizeSpeech'], resources: ['*'] }));
    data.audioBucket.grantPut(notifyFn);
    supervisor.grantPublish(notifyFn);
    supervisor.grantPublish(closeFn);
    backup.grantPublish(escalateFn);
    this.grantTaskResponse(registerFn);
    closeFn.addToRolePolicy(new iam.PolicyStatement({
      actions: ['bedrock:InvokeModel'],
      resources: [
        `arn:aws:bedrock:${stack.region}:${stack.account}:inference-profile/${props.bedrockModelId}`,
        'arn:aws:bedrock:*::foundation-model/amazon.nova-lite-v1:0',
      ],
    }));

    const invoke = (id: string, f: lambda.IFunction) => new tasks.LambdaInvoke(this, id, {
      lambdaFunction: f, payloadResponseOnly: true, resultPath: sfn.JsonPath.DISCARD,
    });
    const wait = (id: string, kind: string, seconds: number) => new tasks.LambdaInvoke(this, id, {
      lambdaFunction: registerFn,
      integrationPattern: sfn.IntegrationPattern.WAIT_FOR_TASK_TOKEN,
      payload: sfn.TaskInput.fromObject({
        incident_id: sfn.JsonPath.stringAt('$.incident_id'), kind, token: sfn.JsonPath.taskToken,
      }),
      taskTimeout: sfn.Timeout.duration(Duration.seconds(seconds)),
      resultPath: sfn.JsonPath.DISCARD,
    });

    const notify = invoke('Notify', notifyFn);
    const waitForAck = wait('WaitForAck', 'ack', props.ackTimeoutSeconds);
    const escalate = invoke('Escalate', escalateFn);
    const waitForAck2 = wait('WaitForAckAfterEscalation', 'ack', 600);
    const markUnack = new sfn.Pass(this, 'MarkUnacknowledged');
    const waitForRecovery = wait('WaitForRecovery', 'recovery', 3600);
    const close = new tasks.LambdaInvoke(this, 'Close', {
      lambdaFunction: closeFn, payloadResponseOnly: true,
      payload: sfn.TaskInput.fromObject({ incident_id: sfn.JsonPath.stringAt('$.incident_id') }),
    });

    waitForAck.addCatch(escalate, { errors: ['States.Timeout'], resultPath: '$.timeout' });
    waitForAck2.addCatch(markUnack, { errors: ['States.Timeout'], resultPath: '$.timeout' });
    waitForRecovery.addCatch(close, { errors: ['States.Timeout'], resultPath: '$.recovery_timeout' });
    notify.next(waitForAck);
    waitForAck.next(waitForRecovery);
    escalate.next(waitForAck2);
    waitForAck2.next(waitForRecovery);
    markUnack.next(waitForRecovery);
    waitForRecovery.next(close);

    this.stateMachine = new sfn.StateMachine(this, 'StateMachine', {
      stateMachineName: STATE_MACHINE_NAME,
      stateMachineType: sfn.StateMachineType.STANDARD,
      definitionBody: sfn.DefinitionBody.fromChainable(notify),
      tracingEnabled: true,
      timeout: Duration.hours(2),
      logs: {
        destination: new logs.LogGroup(this, 'Logs', {
          logGroupName: '/aws/vendedlogs/states/wristheat-escalation',
          retention: logs.RetentionDays.ONE_WEEK,
          removalPolicy: RemovalPolicy.DESTROY,
        }),
        level: sfn.LogLevel.ALL,
      },
    });
  }

  /** states:SendTaskSuccess on the state machine by name (avoids a dependency cycle). */
  grantTaskResponse(f: lambda.IFunction) {
    f.addToRolePolicy(new iam.PolicyStatement({
      actions: ['states:SendTaskSuccess', 'states:SendTaskFailure', 'states:SendTaskHeartbeat'],
      resources: [this.stateMachineArn],
    }));
  }
}
