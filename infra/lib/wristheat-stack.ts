import { CfnOutput, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Auth } from './auth';
import { Context } from './context';
import { Data } from './data';
import { Escalation } from './escalation';
import { IngestApi } from './ingest-api';
import { Layers } from './layers';
import { Observability } from './observability';
import { Web } from './web';

export interface WristHeatStackProps extends StackProps {
  /** Directory produced by scripts/build_lambdas.sh (app/, layer-core/, layer-sci/, dashboard/). */
  buildDir: string;
}

export class WristHeatStack extends Stack {
  constructor(scope: Construct, id: string, props: WristHeatStackProps) {
    super(scope, id, props);
    const siteId: string = this.node.tryGetContext('siteId') ?? 'kgp';

    const data = new Data(this, 'Data');
    const layers = new Layers(this, 'Layers', props.buildDir);
    const web = new Web(this, 'Web');
    const corsOrigins = ['http://localhost:5173', web.url];
    const ingest = new IngestApi(this, 'Ingest', { buildDir: props.buildDir, data, layers, siteId, corsOrigins });
    const context = new Context(this, 'Context', { buildDir: props.buildDir, data, layers, siteId });
    const auth = new Auth(this, 'Auth');
    const apiFn = ingest.addSupervisorApi(auth, context.fn);
    const dashboardUrl = web.url;
    const escalation = new Escalation(this, 'Escalation', {
      buildDir: props.buildDir, data, layers, siteId, dashboardUrl,
      ackTimeoutSeconds: Number(this.node.tryGetContext('ackTimeoutSeconds') ?? 90),
      supervisorEmail: this.node.tryGetContext('supervisorEmail') || undefined,
      backupEmail: this.node.tryGetContext('backupEmail') || undefined,
      bedrockModelId: this.node.tryGetContext('bedrockModelId') ?? 'apac.amazon.nova-lite-v1:0',
    });
    ingest.ingestFn.addEnvironment('STATE_MACHINE_ARN', escalation.stateMachineArn);
    escalation.stateMachine.grantStartExecution(ingest.ingestFn);
    escalation.grantTaskResponse(ingest.ingestFn);
    escalation.grantTaskResponse(apiFn);
    new Observability(this, 'Observability', {
      functions: [ingest.ingestFn, apiFn, context.fn, ...escalation.functions],
      stateMachine: escalation.stateMachine,
    });
    web.deploy(props.buildDir, {
      apiUrl: ingest.api.apiEndpoint, region: this.region,
      userPoolId: auth.userPool.userPoolId, userPoolClientId: auth.client.userPoolClientId,
    });

    const out = (name: string, value: string) => new CfnOutput(this, name, { value });
    out('ApiUrl', ingest.api.apiEndpoint);
    out('DeviceTokenSecretArn', data.deviceToken.secretArn);
    out('TableSites', data.sites.tableName);
    out('TableTrainees', data.trainees.tableName);
    out('TableSessions', data.sessions.tableName);
    out('TableReadings', data.readings.tableName);
    out('TableMinutes', data.minutes.tableName);
    out('TableIncidents', data.incidents.tableName);
    out('AudioBucketName', data.audioBucket.bucketName);
    out('ContextFunctionName', context.fn.functionName);
    out('StateMachineArn', escalation.stateMachine.stateMachineArn);
    out('DashboardUrl', web.url);
  }
}
