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
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    }
})

_logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='JEP backend providing CMake editing support.')
    args = parser.parse_args()

    backend = Backend([Listener()])
    _logger.info('CMake backend starting up.')
    backend.start()


if __name__ == '__main__':
    main()
