from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

app = LambdaFunctionUrlResolver()


@app.get("/")
def root():
    return {"message": "This is a no-op endpoint. It does nothing."}


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
