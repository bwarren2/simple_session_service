#!/usr/bin/env python3

from aws_cdk import core

from cdkpipe_2.cdkpipe_2_stack import Cdkpipe2Stack


app = core.App()
Cdkpipe2Stack(app, "cdkpipe-2")

app.synth()
