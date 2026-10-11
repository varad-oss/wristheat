import { CfnOutput, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Context } from './context';
import { Data } from './data';
import { IngestApi } from './ingest-api';
import { Layers } from './layers';

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
    const ingest = new IngestApi(this, 'Ingest', { buildDir: props.buildDir, data, layers, siteId });
    const context = new Context(this, 'Context', { buildDir: props.buildDir, data, layers, siteId });

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
  }
}
