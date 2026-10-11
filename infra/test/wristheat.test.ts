import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { App } from 'aws-cdk-lib';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { WristHeatStack } from '../lib/wristheat-stack';

function fakeBuildDir(): string {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'wh-build-'));
  for (const d of ['app/wristheat', 'layer-core/python', 'layer-sci/python', 'dashboard', 'web/wristheat']) {
    fs.mkdirSync(path.join(dir, d), { recursive: true });
  }
  fs.writeFileSync(path.join(dir, 'app/wristheat/__init__.py'), '');
  fs.writeFileSync(path.join(dir, 'dashboard/index.html'), '<html></html>');
  return dir;
}

let template: Template;

beforeAll(() => {
  const app = new App({ context: { supervisorEmail: 'sup@example.com', backupEmail: 'backup@example.com' } });
  const stack = new WristHeatStack(app, 'TestStack', {
    env: { account: '123456789012', region: 'ap-south-1' },
    buildDir: fakeBuildDir(),
  });
  template = Template.fromStack(stack);
});

test('six on-demand DynamoDB tables', () => {
  template.resourceCountIs('AWS::DynamoDB::Table', 6);
  template.allResourcesProperties('AWS::DynamoDB::Table', { BillingMode: 'PAY_PER_REQUEST' });
});

test('python3.12 arm64 Lambdas', () => {
  const ours = Object.values(template.findResources('AWS::Lambda::Function'))
    .map((r: any) => r.Properties)
    .filter((p: any) => String(p.Handler).startsWith('wristheat.'));
  expect(ours.length).toBeGreaterThanOrEqual(1);
  for (const p of ours) {
    expect(p.Runtime).toBe('python3.12');
    expect(p.Architectures).toEqual(['arm64']);
  }
});

test('device routes exist without an authorizer', () => {
  for (const key of ['POST /v1/ingest', 'POST /v1/sessions/{session_id}/end']) {
    template.hasResourceProperties('AWS::ApiGatewayV2::Route', { RouteKey: key, AuthorizationType: 'NONE' });
  }
});

test('device token secret is 32 chars without punctuation', () => {
  template.hasResourceProperties('AWS::SecretsManager::Secret', {
    Name: 'wristheat/device-token',
    GenerateSecretString: Match.objectLike({ PasswordLength: 32, ExcludePunctuation: true }),
  });
});

test('API throttling 20/40', () => {
  template.hasResourceProperties('AWS::ApiGatewayV2::Stage', {
    DefaultRouteSettings: Match.objectLike({ ThrottlingRateLimit: 20, ThrottlingBurstLimit: 40 }),
  });
});

test('context Lambda runs every 10 minutes', () => {
  template.hasResourceProperties('AWS::Scheduler::Schedule', { ScheduleExpression: 'rate(10 minutes)' });
  template.hasResourceProperties('AWS::Lambda::Function', Match.objectLike({
    Handler: 'wristheat.handlers.context.handler', MemorySize: 1024, Timeout: 60,
  }));
});

test('supervisor routes use the JWT authorizer; device routes do not', () => {
  template.resourceCountIs('AWS::ApiGatewayV2::Authorizer', 1);
  template.hasResourceProperties('AWS::ApiGatewayV2::Authorizer', { AuthorizerType: 'JWT' });
  for (const key of ['GET /v1/roster', 'GET /v1/sessions/{session_id}/series', 'GET /v1/incidents',
    'GET /v1/incidents/{incident_id}', 'POST /v1/incidents/{incident_id}/ack', 'POST /v1/context/refresh']) {
    template.hasResourceProperties('AWS::ApiGatewayV2::Route', { RouteKey: key, AuthorizationType: 'JWT' });
  }
  template.hasResourceProperties('AWS::Cognito::UserPool', Match.objectLike({
    AdminCreateUserConfig: Match.objectLike({ AllowAdminCreateUserOnly: true }),
  }));
});

test('escalation state machine waits for task tokens and emails two topics', () => {
  const sm = Object.values(template.findResources('AWS::StepFunctions::StateMachine'))[0] as any;
  expect(sm.Properties.StateMachineName).toBe('wristheat-escalation');
  const def = JSON.stringify(sm.Properties.DefinitionString);
  expect(def).toContain('waitForTaskToken');
  for (const state of ['Notify', 'WaitForAck', 'Escalate', 'WaitForAckAfterEscalation', 'MarkUnacknowledged',
    'WaitForRecovery', 'Close']) {
    expect(def).toContain(state);
  }
  template.hasResourceProperties('AWS::SNS::Topic', { TopicName: 'wristheat-supervisor' });
  template.hasResourceProperties('AWS::SNS::Topic', { TopicName: 'wristheat-backup' });
  template.resourceCountIs('AWS::SNS::Subscription', 2);
  template.hasResourceProperties('AWS::Lambda::Function', Match.objectLike({
    Handler: 'wristheat.handlers.ingest.handler',
    Environment: Match.objectLike({ Variables: Match.objectLike({ STATE_MACHINE_ARN: Match.anyValue() }) }),
  }));
});

test('default: dashboard served by the API $default route, no CloudFront', () => {
  template.resourceCountIs('AWS::CloudFront::Distribution', 0);
  template.hasResourceProperties('AWS::ApiGatewayV2::Route', { RouteKey: '$default', AuthorizationType: 'NONE' });
  template.hasResourceProperties('AWS::Lambda::Function', Match.objectLike({ Handler: 'wristheat.handlers.web.handler' }));
  template.hasOutput('DashboardUrl', {});
});

test('cloudFront=true: dashboard on CloudFront with SPA fallback and CORS for its domain', () => {
  const app = new App({ context: { cloudFront: 'true' } });
  const cf = Template.fromStack(new WristHeatStack(app, 'CfStack', {
    env: { account: '123456789012', region: 'ap-south-1' }, buildDir: fakeBuildDir(),
  }));
  cf.resourceCountIs('AWS::CloudFront::Distribution', 1);
  cf.hasResourceProperties('AWS::CloudFront::Distribution', {
    DistributionConfig: Match.objectLike({
      DefaultRootObject: 'index.html',
      CustomErrorResponses: Match.arrayWith([Match.objectLike({ ErrorCode: 404, ResponseCode: 200, ResponsePagePath: '/index.html' })]),
    }),
  });
  const api = Object.values(cf.findResources('AWS::ApiGatewayV2::Api'))[0] as any;
  const origins = JSON.stringify(api.Properties.CorsConfiguration.AllowOrigins);
  expect(origins).toContain('http://localhost:5173');
  expect(origins).toContain('DomainName');
});

test('CloudWatch dashboard named WristHeat', () => {
  template.hasResourceProperties('AWS::CloudWatch::Dashboard', { DashboardName: 'WristHeat' });
  template.hasOutput('CloudWatchDashboardUrl', {});
});
