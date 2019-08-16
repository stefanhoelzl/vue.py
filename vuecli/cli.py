import sys
import argparse
from tempfile import TemporaryDirectory as TempDir
from pathlib import Path

from vuecli.provider import RegisteredProvider
from vuecli.provider.static import Static as StaticProvider
from vue import __version__


def deploy(provider_class, arguments):
    if provider_class is None:
        print(
            f"'pip install vuepy[{arguments.deploy}]' to use this provider",
            file=sys.stderr
        )
        sys.exit(1)

    deploy_arguments = {
        name.strip("-"): getattr(arguments, name.strip("-"), False)
        for name in provider_class.Arguments
    }

    provider = provider_class(arguments.src)
    provider.setup()
    provider.deploy(**deploy_arguments)


def package(destination, app):
    with TempDir() as apptemp, TempDir() as deploytemp:
        appdir = Path(app if app else apptemp)
        deploydir = Path(deploytemp)

        provider = StaticProvider(appdir)
        provider.setup()
        provider.deploy(deploydir, package=True)

        Path(destination, "vuepy.js").write_text(
            (deploydir / "vuepy.js").read_text(encoding="utf-8")
        )


def main():
    cli = argparse.ArgumentParser(description='vue.py command line interface')
    cli.add_argument(
        '--version', action='version', version=f"vue.py {__version__}"
    )

    command = cli.add_subparsers(title="commands", dest="cmd")

    deploy_cmd = command.add_parser("deploy", help="deploy application")
    provider_cmd = deploy_cmd.add_subparsers(help='Provider')
    for name, provider in RegisteredProvider.items():
        sp = provider_cmd.add_parser(name)
        sp.set_defaults(deploy=name)
        if provider is not None:
            for arg_name, config in provider.Arguments.items():
                if isinstance(config, str):
                    config = {"help": config}
                sp.add_argument(arg_name, **config)
    deploy_cmd.add_argument(
        "--src", default=".", nargs="?",
        help="Path of the application to deploy (default: '.')"
    )

    package_cmd = command.add_parser("package", help="create vuepy.js")
    package_cmd.add_argument(
        "destination", default=".", nargs="?",
        help="(default: current directory)"
    )
    package_cmd.add_argument(
        "--app", nargs="?", default=False,
        help="include application in package"
    )

    args = cli.parse_args()
    if args.cmd == "deploy":
        deploy(RegisteredProvider[args.deploy], args)
    elif args.cmd == "package":
        package(args.destination, "." if args.app is None else args.app)
    else:
        cli.print_help()


if __name__ == "__main__":
    main()
