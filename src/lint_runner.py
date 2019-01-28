import sys

from pylint.lint import Run


def main():
    arguments = [
        '--rcfile=.pylintrc',
        'domain',
        'filesystem',
        'lint_runner',
        'main',
        'shell',
        'test',
        'test_runner',
        'util'
    ]

    if '-e' in sys.argv:
        arguments.append('--errors-only')

    error_code = Run(arguments)
    sys.exit(error_code)


if __name__ == '__main__':
    main()
