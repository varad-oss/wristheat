import { CfnOutput, RemovalPolicy } from 'aws-cdk-lib';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import { Construct } from 'constructs';

/** Supervisor sign-in (spec §13): no self sign-up; seed.py creates the user. */
export class Auth extends Construct {
  readonly userPool: cognito.UserPool;
  readonly client: cognito.UserPoolClient;

  constructor(scope: Construct, id: string) {
    super(scope, id);
    this.userPool = new cognito.UserPool(this, 'Supervisors', {
      userPoolName: 'wristheat-supervisors',
      selfSignUpEnabled: false,
      signInAliases: { username: true, email: true },
      passwordPolicy: { minLength: 10, requireSymbols: false },
      accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
      removalPolicy: RemovalPolicy.DESTROY,
    });
    this.client = this.userPool.addClient('Dashboard', {
      generateSecret: false,
      authFlows: { userSrp: true, adminUserPassword: true },
      preventUserExistenceErrors: true,
    });
    new CfnOutput(scope, 'UserPoolId', { value: this.userPool.userPoolId });
    new CfnOutput(scope, 'UserPoolClientId', { value: this.client.userPoolClientId });
  }
}
