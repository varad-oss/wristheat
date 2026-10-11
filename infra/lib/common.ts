import * as path from 'path';
import { Duration, RemovalPolicy } from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';
import { Construct } from 'constructs';

export interface PyFnProps {
  buildDir: string;
  handler: string;
  layers: lambda.ILayerVersion[];
  environment?: Record<string, string>;
  memorySize?: number;
  timeout?: Duration;
}

/** Python 3.12 arm64 Lambda from build/app with Powertools tracing and one-week logs. */
export function pyFn(scope: Construct, id: string, props: PyFnProps): lambda.Function {
  return new lambda.Function(scope, id, {
    runtime: lambda.Runtime.PYTHON_3_12,
    architecture: lambda.Architecture.ARM_64,
    code: lambda.Code.fromAsset(path.join(props.buildDir, 'app')),
    handler: props.handler,
    layers: props.layers,
    memorySize: props.memorySize ?? 512,
    timeout: props.timeout ?? Duration.seconds(15),
    tracing: lambda.Tracing.ACTIVE,
    logGroup: new logs.LogGroup(scope, `${id}Logs`, {
      retention: logs.RetentionDays.ONE_WEEK,
      removalPolicy: RemovalPolicy.DESTROY,
    }),
    environment: {
      POWERTOOLS_SERVICE_NAME: 'wristheat',
      POWERTOOLS_METRICS_NAMESPACE: 'WristHeat',
      ...props.environment,
    },
  });
}
