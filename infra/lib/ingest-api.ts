import { Duration } from 'aws-cdk-lib';
import * as apigw from 'aws-cdk-lib/aws-apigatewayv2';
import { HttpJwtAuthorizer } from 'aws-cdk-lib/aws-apigatewayv2-authorizers';
import { HttpLambdaIntegration } from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import { pyFn } from './common';
import { Auth } from './auth';
import { Data } from './data';
import { Layers } from './layers';

export interface IngestApiProps {
  buildDir: string;
  data: Data;
  layers: Layers;
  siteId: string;
  /** Browser origins allowed by CORS (localhost dev server + the CloudFront domain). */
  corsOrigins: string[];
}

/** HTTP API with the device routes and the ingest Lambda (spec §5.1). */
export class IngestApi extends Construct {
  readonly api: apigw.HttpApi;
  readonly ingestFn: lambda.Function;
  apiFn?: lambda.Function;
  private readonly props: IngestApiProps;

  constructor(scope: Construct, id: string, props: IngestApiProps) {
    super(scope, id);
    this.props = props;
    const { data } = props;
    this.api = new apigw.HttpApi(this, 'Api', {
      apiName: 'wristheat',
      createDefaultStage: false,
      corsPreflight: {
        allowOrigins: props.corsOrigins,
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

  /** Supervisor routes (spec §5.2) behind a Cognito JWT authorizer, served by one API Lambda. */
  addSupervisorApi(auth: Auth, contextFn: lambda.IFunction): lambda.Function {
    const { data, layers, buildDir, siteId } = this.props;
    const fn = pyFn(this, 'ApiFn', {
      buildDir,
      handler: 'wristheat.handlers.api.handler',
      layers: [layers.core],
      memorySize: 512,
      timeout: Duration.seconds(29),
      environment: {
        ...data.tableEnv(),
        SITE_ID: siteId,
        CONTEXT_FUNCTION_NAME: contextFn.functionName,
        AUDIO_BUCKET: data.audioBucket.bucketName,
      },
    });
    for (const t of [data.sites, data.trainees, data.sessions, data.minutes, data.readings]) t.grantReadData(fn);
    data.incidents.grantReadWriteData(fn);
    data.audioBucket.grantRead(fn);
    contextFn.grantInvoke(fn);
    const authorizer = new HttpJwtAuthorizer('Jwt', auth.userPool.userPoolProviderUrl, {
      jwtAudience: [auth.client.userPoolClientId],
    });
    const integration = new HttpLambdaIntegration('ApiIntegration', fn);
    const route = (path: string, method: apigw.HttpMethod) =>
      this.api.addRoutes({ path, methods: [method], integration, authorizer });
    route('/v1/roster', apigw.HttpMethod.GET);
    route('/v1/sessions/{session_id}/series', apigw.HttpMethod.GET);
    route('/v1/sessions/{session_id}/summary', apigw.HttpMethod.GET);
    route('/v1/incidents', apigw.HttpMethod.GET);
    route('/v1/incidents/{incident_id}', apigw.HttpMethod.GET);
    route('/v1/incidents/{incident_id}/ack', apigw.HttpMethod.POST);
    route('/v1/context/refresh', apigw.HttpMethod.POST);
    this.apiFn = fn;
    return fn;
  }
}
