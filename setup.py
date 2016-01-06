"""Setup script for jep.python."""


def main():
    """Wrapper around imports to prevent them being executed immediately upon this module being only imported (Sublime plugin workaround)."""
    from setuptools import setup, find_packages
    from setuptools.command.test import test as TestCommand
    import sys

    class PyTestCommand(TestCommand):
        user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

        def initialize_options(self):
            TestCommand.initialize_options(self)
            self.pytest_args = []

        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            #import here, cause outside the eggs aren't loaded
            import pytest

            errno = pytest.main(self.pytest_args)
            sys.exit(errno)

    # configure dependencies corresponding to interpreter version:
    install_requires = [
        'antlr4-python3-runtime',
        'jep-python'
    ]

    if sys.version_info < (3, 3):
        print('This Python version is not supported, minimal version 3.3 is required.')
        sys.exit(1)
    if sys.version_info < (3, 4):
        install_requires.append('enum34')

    setup(
            name='jep-cmake',
            version='0.0.1',
            packages=find_packages(),
            entry_points={'console_scripts': ['jep-cmake = jep_cmake.main:main']},
            install_requires=install_requires,
            tests_require=[
                'pytest'
            ],
            cmdclass={'test': PyTestCommand},
            url='https://github.com/jep-project/jep-cmake',
            license='',
            author='Mike Pagel',
            author_email='mike@mpagel.de',
            description='CMake backend for JEP-enabled editors.',
            keywords='jep cmake language editor',
            classifiers=[
                'Development Status :: 4 - Beta',
                'Intended Audience :: End Users/Desktop',
                'Topic :: Software Development',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
            ],
    )


if __name__ == '__main__':
    main()
