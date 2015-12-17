"""jep-cmake entry point."""
import argparse

import jep.backend
import jep.schema


class Listener(jep.backend.FrontendListener):
    def on_completion_request(self, completion_request: jep.schema.CompletionRequest, context):
        context.send_message(jep.schema.CompletionResponse(completion_request.pos,
                                                           0,
                                                           False,
                                                           [jep.schema.CompletionOption('cmake_completion', 'Something', 'Something to complete')],
                                                           completion_request.token))


def main():
    parser = argparse.ArgumentParser(description='JEP backend providing CMake editing support.')
    args = parser.parse_args()

    backend = jep.backend.Backend([Listener()])
    backend.start()


if __name__ == '__main__':
    main()
