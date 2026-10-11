import { CfnOutput, Duration, Stack } from 'aws-cdk-lib';
import * as cw from 'aws-cdk-lib/aws-cloudwatch';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import { Construct } from 'constructs';

const search = (metric: string, stat: string, label: string) => new cw.MathExpression({
  expression: `SEARCH('Namespace="WristHeat" MetricName="${metric}"', '${stat}', 60)`,
  label, period: Duration.minutes(1), usingMetrics: {},
});

/** CloudWatch dashboard "WristHeat" (spec §13). */
export class Observability extends Construct {
  constructor(scope: Construct, id: string, props: { functions: lambda.IFunction[]; stateMachine: sfn.IStateMachine }) {
    super(scope, id);
    const dash = new cw.Dashboard(this, 'Dashboard', { dashboardName: 'WristHeat', defaultInterval: Duration.hours(3) });
    const sm = props.stateMachine;
    dash.addWidgets(
      new cw.GraphWidget({ title: 'Heart-rate samples ingested (per minute)', left: [search('SamplesIngested', 'Sum', 'Samples')], width: 8 }),
      new cw.GraphWidget({ title: 'Ingest latency p95 (ms)', left: [search('IngestLatencyMs', 'p95', 'p95')], width: 8 }),
      new cw.GraphWidget({ title: 'State transitions by target', left: [search('StateTransitions', 'Sum', '')], width: 8 }),
    );
    dash.addWidgets(
      new cw.GraphWidget({ title: 'Incidents opened', left: [search('IncidentsOpened', 'Sum', 'Incidents')], width: 8 }),
      new cw.GraphWidget({
        title: 'Escalation executions', width: 8,
        left: [sm.metricStarted({ label: 'Started' }), sm.metricSucceeded({ label: 'Succeeded' }), sm.metricFailed({ label: 'Failed' })],
      }),
      new cw.GraphWidget({
        title: 'Fallbacks', width: 8,
        left: [search('ContextFetchErrors', 'Sum', 'Context fetch errors'), search('BedrockFallbacks', 'Sum', 'Bedrock fallbacks')],
      }),
    );
    dash.addWidgets(new cw.GraphWidget({
      title: 'Lambda errors', width: 24,
      left: props.functions.map((f) => f.metricErrors({ label: f.node.id.replace(/Fn$/, ''), period: Duration.minutes(1) })),
    }));
    const region = Stack.of(this).region;
    new CfnOutput(Stack.of(this), 'CloudWatchDashboardUrl', {
      value: `https://${region}.console.aws.amazon.com/cloudwatch/home?region=${region}#dashboards/dashboard/WristHeat`,
    });
  }
}
