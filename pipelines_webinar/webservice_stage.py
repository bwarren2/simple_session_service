from aws_cdk import core
from .pipelines_webinar_stack import PipelineWebinarStack


class WebServiceStage(core.Stage):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        service = PipelineWebinarStack(self, "WebService")
        self.url_output = service.url_output
