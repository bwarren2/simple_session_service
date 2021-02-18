#!/usr/bin/env python3

from aws_cdk import core

from pipelines_webinar.pipelines_webinar_stack import PipelineWebinarStack
from pipelines_webinar.pipeline_stack import PipelineStack


app = core.App()
PipelineWebinarStack(app, "pipelines-webinar")
PipelineStack(
    app,
    "pipelines-webinar",
    env={
        "account": "871089662319",
        "region": "us-east-1",
    },
)

app.synth()
