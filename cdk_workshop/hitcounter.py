from constructs import Construct

from aws_cdk import RemovalPolicy, aws_lambda as lambda_, aws_dynamodb as ddb


class HitCounter(Construct):
    @property
    def handler(self):
        return self._handler

    @property
    def table(self):
        return self._table

    def __init__(
        self, scope: Construct, id: str, downstream: lambda_.IFunction, **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # keyword parameter downstream of type lambda.IFunction.
        # This is where we are going to “plug in” the Lambda function we created in the previous chapter so it can be hit-counted

        self._table = ddb.Table(
            self,
            "Hits",
            partition_key={"name": "path", "type": ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY,
        )

        self._handler = lambda_.Function(
            self,
            "HitCounterHandler",
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler="hitcount.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DOWNSTREAM_FUNCTION_NAME": downstream.function_name,
                "HITS_TABLE_NAME": self._table.table_name,
            },
        )

        self._table.grant_read_write_data(self._handler)
        downstream.grant_invoke(self._handler)
