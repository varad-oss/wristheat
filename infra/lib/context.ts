import { Duration } from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as scheduler from 'aws-cdk-lib/aws-scheduler';
import * as targets from 'aws-cdk-lib/aws-scheduler-targets';
import { Construct } from 'constructs';
import { pyFn } from './common';
import { Data } from './data';
import { Layers } from './layers';

/** Context Lambda (Liljegren WBGT from Open-Meteo) and its 10-minute schedule (spec §8). */
export class Context extends Construct {
  readonly fn: lambda.Function;

  constructor(scope: Construct, id: string, props: { buildDir: string; data: Data; layers: Layers; siteId: string }) {
    super(scope, id);
    this.fn = pyFn(this, 'ContextFn', {
      buildDir: props.buildDir,
      handler: 'wristheat.handlers.context.handler',
      layers: [props.layers.core, props.layers.sci],
      memorySize: 1024,
      timeout: Duration.seconds(60),
      environment: { TABLE_SITES: props.data.sites.tableName, SITE_ID: props.siteId },
    });
    props.data.sites.grantReadWriteData(this.fn);
    new scheduler.Schedule(this, 'Every10Min', {
      schedule: scheduler.ScheduleExpression.rate(Duration.minutes(10)),
      target: new targets.LambdaInvoke(this.fn, { input: scheduler.ScheduleTargetInput.fromObject({ site_id: props.siteId }) }),
      description: 'Refresh site WBGT and air quality',
    });
  }
}
