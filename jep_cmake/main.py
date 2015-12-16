"""jep-cmake entry point."""
import argparse


def main():
    parser = argparse.ArgumentParser(description='JEP backend providing CMake editing support.')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
