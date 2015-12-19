"""Dispatch of requests and commands from frontend."""
import os

from jep.backend import FrontendListener
from jep.schema import CompletionRequest, CompletionResponse, CompletionOption, SemanticType
from jep_cmake.project import Project


class Listener(FrontendListener):
    def __init__(self, *, project=None):
        self.project = project or Project()

    def on_content_sync(self, content_sync, context):
        # backend has already synchronized latest content, so launch parse:
        self.project.update(content_sync.file, context.content_monitor[content_sync.file])

    def on_completion_request(self, completion_request: CompletionRequest, context):
        options = [CompletionOption(command, origin, semantics=SemanticType.identifier)
                   for command, origin in self.project.completion_option_iter(completion_request.file, completion_request.pos)]

        limit_exceeded = False
        if completion_request.limit and completion_request.limit < len(options):
            options = options[:completion_request.limit]
            limit_exceeded = True

        context.send_message(CompletionResponse(completion_request.pos, 0, limit_exceeded, options, completion_request.token))
