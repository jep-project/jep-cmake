"""jep-cmake entry point."""
import argparse
import logging
import logging.config
import sys

from jep.backend import Backend
from jep_cmake.dispatch import Listener

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(name)s %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'stream': sys.stdout,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'jep_cmake': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG'
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    }
})

_logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='JEP backend providing CMake editing support.')
    parser.add_argument('--version', help='CMake version to be supported, mainly used for completion of built-in commands.', choices=['2.8.12', '3.4'], default='3.4')
    parser.add_argument('--builtin-cmake', help='If specified, built-in CMake commands are part of code completion.', action='store_true')
    parser.add_argument('--builtin-ctest', help='If specified, built-in ctest commands are part of code completion.', action='store_true')
    parser.add_argument('--builtin-deprecated', help='If specified, built-in CMake commands that have been deprecated are part of code completion.', action='store_true')
    args = parser.parse_args()

    backend = Backend([Listener(cmake_version=args.version,
                                builtin_commands=args.builtin_cmake,
                                ctest_commands=args.builtin_ctest,
                                deprecated_commands=args.builtin_deprecated)])
    _logger.info('CMake backend starting up.')
    backend.start()


if __name__ == '__main__':
    main()
