from constructs import Construct
from aws_cdk import Stack, aws_lambda as lambda_, aws_apigateway as apigw

from .hitcounter import HitCounter

from cdk_dynamo_table_view import TableViewer


class CdkWorkshopStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # defines a Lambda resource

        my_lambda = lambda_.Function(
            self,
            "HelloHandler",
            runtime=lambda_.Runtime.PYTHON_3_7,
            code=lambda_.Code.from_asset("lambda"),
            handler="hello.handler",
        )

        hello_with_counter = HitCounter(self, "HelloHitCounter", downstream=my_lambda)

        apigw.LambdaRestApi(self, "Endpoint", handler=hello_with_counter._handler)

        TableViewer(
            self, "ViewHitCounter", title="HelloHits", table=hello_with_counter.table
        )
