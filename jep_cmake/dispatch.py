"""Dispatch of requests and commands from frontend."""
from jep_py.backend import FrontendListener
from jep_py.schema import CompletionRequest, CompletionResponse, CompletionOption, SemanticType
from jep_cmake.project import Project


class Listener(FrontendListener):
    def __init__(self, *, cmake_version, builtin_commands, deprecated_commands, ctest_commands, project=None):
        self.project = project or Project(cmake_version=cmake_version,
                                          builtin_commands=builtin_commands,
                                          ctest_commands=ctest_commands,
                                          deprecated_commands=deprecated_commands)

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
