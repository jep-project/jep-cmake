"""Setup script for jep-cmake."""

# need to guard script here due to reentrance while testing multiprocessing:
if __name__ == '__main__':

    from setuptools import setup, find_packages
    import sys

    if sys.version_info < (3, 3):
        print('This Python version is not supported, minimal version 3.3 is required.')
        sys.exit(1)

    enum34_opt = ['enum34'] if sys.version_info < (3, 4) else []

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner_opt = ['pytest-runner>=2.0,<3dev'] if needs_pytest else []

    setup(
            name='jep-cmake',
            version='0.0.3',
            packages=find_packages(),
            package_data={'jep_cmake': ['built-ins/*.txt']},
            entry_points={'console_scripts': ['jep-cmake = jep_cmake.main:main']},
            install_requires=[
                                 'antlr4-python3-runtime',
                                 'chardet',
                                 'jep-python'
                             ] + enum34_opt,
            tests_require=[
                'pytest'
            ],
            setup_requires=pytest_runner_opt,
            url='https://github.com/jep-project/jep-cmake',
            license='',
            author='Mike Pagel',
            author_email='mike@mpagel.de',
            description='CMake backend for JEP-enabled editors.',
            keywords='jep cmake language editor',
            classifiers=[
                'Development Status :: 3 - Alpha',
                'Intended Audience :: End Users/Desktop',
                'Topic :: Software Development',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
            ],
    )
