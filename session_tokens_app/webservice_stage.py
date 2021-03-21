from aws_cdk import core
from .session_crud_stack import SessionCrudStack


class WebServiceStage(core.Stage):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        service = SessionCrudStack(self, "WebService")
        self.url_output = service.url_output
