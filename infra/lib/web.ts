import * as path from 'path';
import { Duration, RemovalPolicy } from 'aws-cdk-lib';
import * as apigw from 'aws-cdk-lib/aws-apigatewayv2';
import { HttpLambdaIntegration } from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import { Construct } from 'constructs';

/** Dashboard hosting: private S3 bucket behind CloudFront (OAC), SPA fallback to index.html. */
export class Web extends Construct {
  readonly bucket: s3.Bucket;
  readonly distribution: cloudfront.Distribution;
  readonly url: string;

  constructor(scope: Construct, id: string) {
    super(scope, id);
    this.bucket = new s3.Bucket(this, 'Site', {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });
    this.distribution = new cloudfront.Distribution(this, 'Cdn', {
      comment: 'WristHeat supervisor dashboard',
      defaultRootObject: 'index.html',
      defaultBehavior: {
        origin: origins.S3BucketOrigin.withOriginAccessControl(this.bucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
      },
      errorResponses: [403, 404].map((status) => ({
        httpStatus: status, responseHttpStatus: 200, responsePagePath: '/index.html', ttl: Duration.seconds(0),
      })),
      priceClass: cloudfront.PriceClass.PRICE_CLASS_200,
    });
    this.url = `https://${this.distribution.distributionDomainName}`;
  }

  /** Uploads the built SPA plus /config.json written from stack outputs, then invalidates the cache. */
  deploy(buildDir: string, config: Record<string, string>) {
    new s3deploy.BucketDeployment(this, 'Deploy', {
      sources: [s3deploy.Source.asset(path.join(buildDir, 'dashboard')), s3deploy.Source.jsonData('config.json', config)],
      destinationBucket: this.bucket,
      distribution: this.distribution,
      distributionPaths: ['/*'],
      memoryLimit: 512,
    });
  }
}

/**
 * Fallback hosting while CloudFront is unavailable on the account: the HTTP API's $default route serves
 * the SPA from a Lambda (same origin as the API, HTTPS via execute-api, no CORS needed).
 */
export class ApiWeb extends Construct {
  constructor(scope: Construct, id: string, props: {
    buildDir: string; api: apigw.HttpApi; userPoolId: string; userPoolClientId: string; layers: lambda.ILayerVersion[];
  }) {
    super(scope, id);
    const fn = new lambda.Function(this, 'WebFn', {
      runtime: lambda.Runtime.PYTHON_3_12,
      architecture: lambda.Architecture.ARM_64,
      code: lambda.Code.fromAsset(path.join(props.buildDir, 'web')),
      handler: 'wristheat.handlers.web.handler',
      memorySize: 256,
      timeout: Duration.seconds(10),
      environment: { USER_POOL_ID: props.userPoolId, USER_POOL_CLIENT_ID: props.userPoolClientId },
    });
    new apigw.HttpRoute(this, 'DefaultRoute', {
      httpApi: props.api,
      routeKey: apigw.HttpRouteKey.DEFAULT,
      integration: new HttpLambdaIntegration('WebIntegration', fn),
    });
  }
}
