import aws_cdk as core
import aws_cdk.assertions as assertions

from tweepy_api.backend_stack import BackendStack

# example tests. To run these tests, uncomment this file along with the example
# resource in tweepy_api/backend_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BackendStack(app, "tweepy_api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
