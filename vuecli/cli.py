import sys
import argparse

from vuecli.provider import RegisteredProvider
from vue import __version__


def deploy(provider_class, arguments):
    if provider_class is None:
        print(
            f"'pip install vuepy[{arguments.deploy}]' to use this provider",
            file=sys.stderr
        )
        sys.exit(1)

    deploy_arguments = {
        name: getattr(arguments, name) for name in provider_class.Arguments
    }

    provider = provider_class(arguments.src)
    provider.setup()
    provider.deploy(**deploy_arguments)


def main():
    cli = argparse.ArgumentParser(description='vue.py command line interface')
    cli.add_argument(
        '--version', action='version', version=f"vue.py {__version__}"
    )

    command = cli.add_subparsers()

    deploy_cmd = command.add_parser("deploy", help="deploy application")
    cli.set_defaults(cmd="deploy")

    provider_cmd = deploy_cmd.add_subparsers(help='Provider')

    for name, provider in RegisteredProvider.items():
        sp = provider_cmd.add_parser(name)
        sp.set_defaults(deploy=name)
        if provider is not None:
            for arg_name, arg_help in provider.Arguments.items():
                sp.add_argument(arg_name, help=arg_help)

    deploy_cmd.add_argument(
        "--src", default=".", nargs="?",
        help="Path of the application to deploy (default: '.')"
    )

    args = cli.parse_args()
    if args.cmd == "deploy":
        deploy(RegisteredProvider[args.deploy], args)


if __name__ == "__main__":
    main()
