"""jep-cmake entry point."""
import argparse

from jep.backend import Backend, FrontendListener
from jep.schema import CompletionRequest, CompletionOption, CompletionResponse


class Listener(FrontendListener):
    def on_completion_request(self, completion_request: CompletionRequest, context):
        context.send_message(CompletionResponse(completion_request.pos,
                                                           0,
                                                           False,
                                                           [CompletionOption('cmake_completion', 'Something', 'Something to complete')],
                                                           completion_request.token))


def main():
    parser = argparse.ArgumentParser(description='JEP backend providing CMake editing support.')
    args = parser.parse_args()

    backend = Backend([Listener()])
    backend.start()


if __name__ == '__main__':
    main()
