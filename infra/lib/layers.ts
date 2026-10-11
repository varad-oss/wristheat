import * as path from 'path';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

/** Dependency layers built by scripts/build_lambdas.sh (pip --platform manylinux2014_aarch64, no Docker). */
export class Layers extends Construct {
  readonly core: lambda.LayerVersion;
  readonly sci: lambda.LayerVersion;

  constructor(scope: Construct, id: string, buildDir: string) {
    super(scope, id);
    const layer = (name: string, dir: string, description: string) => new lambda.LayerVersion(this, name, {
      code: lambda.Code.fromAsset(path.join(buildDir, dir)),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_12],
      compatibleArchitectures: [lambda.Architecture.ARM_64],
      description,
    });
    this.core = layer('Core', 'layer-core', 'aws-lambda-powertools');
    this.sci = layer('Sci', 'layer-sci', 'numpy + thermofeel 2.3.0');
  }
}
