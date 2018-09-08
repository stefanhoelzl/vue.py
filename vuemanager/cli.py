"""vuemanager

Usage:
    vuemanager deploy live [<app-path>]
    vuemanager deploy static <destination> [<app-path>]

Options:
    <app-path>              Path of the application to deplay (default: current path)
    <destination>           Path where the application should be deployed to
"""
from docopt import docopt
from vuemanager.provider import Static, Flask


def deploy(arguments):
    if arguments.get("live", False):
        provider_class = Flask
        deploy_arguments = ()
    else:
        provider_class = Static
        deploy_arguments = (arguments["<destination>"],)

    provider = provider_class(arguments.get("<app-path>"))
    provider.setup()
    provider.deploy(*deploy_arguments)


def main():
    arguments = docopt(__doc__)
    if arguments.pop("deploy"):
        deploy(arguments)


if __name__ == "__main__":
    main()
