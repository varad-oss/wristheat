import { Duration } from 'aws-cdk-lib';
import * as apigw from 'aws-cdk-lib/aws-apigatewayv2';
import { HttpLambdaIntegration } from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import { pyFn } from './common';
import { Data } from './data';
import { Layers } from './layers';

export interface IngestApiProps {
  buildDir: string;
  data: Data;
  layers: Layers;
  siteId: string;
}

/** HTTP API with the device routes and the ingest Lambda (spec §5.1). */
export class IngestApi extends Construct {
  readonly api: apigw.HttpApi;
  readonly ingestFn: lambda.Function;
  readonly corsOrigins: string[] = ['http://localhost:5173'];

  constructor(scope: Construct, id: string, props: IngestApiProps) {
    super(scope, id);
    const { data } = props;
    this.api = new apigw.HttpApi(this, 'Api', {
      apiName: 'wristheat',
      createDefaultStage: false,
      corsPreflight: {
        allowOrigins: ['*'],
        allowMethods: [apigw.CorsHttpMethod.GET, apigw.CorsHttpMethod.POST, apigw.CorsHttpMethod.OPTIONS],
        allowHeaders: ['authorization', 'content-type'],
        maxAge: Duration.hours(1),
      },
    });
    this.api.addStage('Stage', {
      stageName: '$default',
      autoDeploy: true,
      throttle: { rateLimit: 20, burstLimit: 40 },
    });

    this.ingestFn = pyFn(this, 'IngestFn', {
      buildDir: props.buildDir,
      handler: 'wristheat.handlers.ingest.handler',
      layers: [props.layers.core],
      memorySize: 512,
      timeout: Duration.seconds(15),
      environment: {
        ...data.tableEnv(),
        DEVICE_TOKEN_SECRET_ARN: data.deviceToken.secretArn,
        STATE_MACHINE_ARN: '',
        SITE_ID: props.siteId,
      },
    });
    for (const t of [data.sessions, data.readings, data.minutes, data.incidents, data.trainees]) {
      t.grantReadWriteData(this.ingestFn);
    }
    data.sites.grantReadData(this.ingestFn);
    data.deviceToken.grantRead(this.ingestFn);

    const integration = new HttpLambdaIntegration('IngestIntegration', this.ingestFn);
    this.api.addRoutes({ path: '/v1/ingest', methods: [apigw.HttpMethod.POST], integration });
    this.api.addRoutes({ path: '/v1/sessions/{session_id}/end', methods: [apigw.HttpMethod.POST], integration });
  }
}
