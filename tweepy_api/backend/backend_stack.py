from aws_cdk import (
    Stack,
    aws_iam,
    aws_lambda,
    aws_apigateway
)
from constructs import Construct


class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, cdk_env: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        region = cdk_env['region']
        account_id = cdk_env['account_id']

        # lambda_layer
        lambda_layer = aws_lambda.LayerVersion(
            self, 'LambdaLayer',
            code=aws_lambda.AssetCode('lambda_layer')
        )

        # lambda_role
        lambda_role = aws_iam.Role(
            self,
            "LambdaRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
        )
        secrets_manager_arn = f"arn:aws:secretsmanager:{region}:{account_id}:secret:TwitterApiKey-9OOnJz"
        secret_policy = aws_iam.PolicyStatement(
            actions=["secretsmanager:GetSecretValue"],
            resources=[secrets_manager_arn]
        )
        lambda_role.add_to_policy(secret_policy)

        # lambda
        lambda_function = aws_lambda.Function(
            self, 'LambdaFunction',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.AssetCode('lambda_src'),
            handler='app.handler',
            role=lambda_role,
            layers=[lambda_layer],
            environment={}
        )

        # api_gateway
        api = aws_apigateway.LambdaRestApi(
            self, 'Api',
            handler=lambda_function,
            proxy=False
        )
        api.root.add_method('GET', integration=aws_apigateway.LambdaIntegration(lambda_function))
