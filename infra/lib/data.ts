import { RemovalPolicy } from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

const N = dynamodb.AttributeType.NUMBER;
const S = dynamodb.AttributeType.STRING;

/** Tables (spec §6), the alert-audio bucket and the device-token secret. */
export class Data extends Construct {
  readonly sites: dynamodb.Table;
  readonly trainees: dynamodb.Table;
  readonly sessions: dynamodb.Table;
  readonly readings: dynamodb.Table;
  readonly minutes: dynamodb.Table;
  readonly incidents: dynamodb.Table;
  readonly audioBucket: s3.Bucket;
  readonly deviceToken: secretsmanager.Secret;

  constructor(scope: Construct, id: string) {
    super(scope, id);
    const table = (name: string, pk: string, sk?: { name: string; type: dynamodb.AttributeType }, ttl = false) =>
      new dynamodb.Table(this, name, {
        partitionKey: { name: pk, type: S },
        sortKey: sk,
        billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
        timeToLiveAttribute: ttl ? 'ttl' : undefined,
        removalPolicy: RemovalPolicy.DESTROY,
      });
    this.sites = table('Sites', 'site_id');
    this.trainees = table('Trainees', 'trainee_id');
    this.sessions = table('Sessions', 'session_id', undefined, true);
    this.readings = table('Readings', 'session_id', { name: 't', type: N }, true);
    this.minutes = table('Minutes', 'session_id', { name: 'minute', type: N }, true);
    this.incidents = table('Incidents', 'incident_id', undefined, true);

    this.audioBucket = new s3.Bucket(this, 'Audio', {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    this.deviceToken = new secretsmanager.Secret(this, 'DeviceToken', {
      secretName: 'wristheat/device-token',
      description: 'Shared token the watch and simulator send as x-device-token',
      generateSecretString: { passwordLength: 32, excludePunctuation: true },
      removalPolicy: RemovalPolicy.DESTROY,
    });
  }

  tableEnv(): Record<string, string> {
    return {
      TABLE_SITES: this.sites.tableName,
      TABLE_TRAINEES: this.trainees.tableName,
      TABLE_SESSIONS: this.sessions.tableName,
      TABLE_READINGS: this.readings.tableName,
      TABLE_MINUTES: this.minutes.tableName,
      TABLE_INCIDENTS: this.incidents.tableName,
    };
  }
}
