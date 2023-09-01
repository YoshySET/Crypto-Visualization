import os
import aws_cdk as cdk

from backend.backend_stack import BackendStack

app = cdk.App()
env_name = os.environ.get('SYSTEM_ENV')
system_env = app.node.try_get_context(env_name)

system_env["account_id"] = os.environ.get('ACCOUNT_ID')
system_env["region"] = os.environ.get('REGION')

BackendStack(app, "BackendStack", cdk_env=system_env)

app.synth()
