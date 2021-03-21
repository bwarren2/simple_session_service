from aws_cdk import core
from session_tokens_app.session_crud_stack import SessionCrudStack


def test_lambda_handler():

    app = core.App()

    SessionCrudStack(app, "Stack")

    template = app.synth().get_stack_by_name("Stack").template
    functions = [
        resource
        for resource in template["Resources"].values()
        if resource["Type"] == "AWS::Lambda::Function"
    ]
    assert len(functions) == 5
    assert functions[0]["Properties"]["Handler"] == "handlers.hello"
    assert functions[1]["Properties"]["Handler"] == "handlers.create"
    assert functions[2]["Properties"]["Handler"] == "handlers.listing"
    assert functions[3]["Properties"]["Handler"] == "handlers.retrieve"
    assert functions[4]["Properties"]["Handler"] == "handlers.delete"
