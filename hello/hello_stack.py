from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
from cdk_dynamo_table_viewer import TableViewer

from hitcounter import HitCounter

class MyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        hello = _lambda.Function(
            self, 'HelloHandler',
            runtime = _lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler = 'hello.handler',
        )

        hello_with_counter = HitCounter(
            self, 'HitCounter',
            downstream=hello,
        )
        apigw.LambdaRestApi(self, 'EndPoint',handler=hello_with_counter.handler)

        TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
            sort_by='path'
        ) 

