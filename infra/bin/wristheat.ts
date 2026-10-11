#!/usr/bin/env node
import * as path from 'path';
import { App } from 'aws-cdk-lib';
import { WristHeatStack } from '../lib/wristheat-stack';

const app = new App();
new WristHeatStack(app, 'WristHeat', {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: 'ap-south-1' },
  buildDir: path.join(__dirname, '..', '..', 'build'),
  description: 'WristHeat: heat-strain early warning (AWS Environmental Hacks)',
});
