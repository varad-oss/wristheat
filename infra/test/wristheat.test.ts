import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { App } from 'aws-cdk-lib';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { WristHeatStack } from '../lib/wristheat-stack';

function fakeBuildDir(): string {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'wh-build-'));
  for (const d of ['app/wristheat', 'layer-core/python', 'layer-sci/python', 'dashboard']) {
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
