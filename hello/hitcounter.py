from aws_cdk import (
    core,
    aws_dynamodb as ddb,
    aws_lambda as _lambda
)

class HitCounter(core.Construct):

    @property
    def handler(self):
        return self._handler

    @property
    def table(self):
        return self._table

    def __init__(self, scope: core.Construct, id: str, downstream : _lambda.Function, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(
            self, 'Hits',
            partition_key = {'name' : 'path', 'type' : ddb.AttributeType.STRING}
        )

        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            runtime = _lambda.Runtime.PYTHON_3_7,
            handler='hitcount.handler',
            code = _lambda.Code.asset('lambda'),
            environment = {
                'DOWNSTREAM_FUNCTION_NAME' : downstream.function_name,
                'HITS_TABLE_NAME': self.table.table_name
            }

        )
        self.table.grant_read_write_data(self.handler)
        downstream.grant_invoke(self.handler)
