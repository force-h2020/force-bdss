import click
from subprocess import check_call

DEFAULT_PYTHON_VERSION = "3.6"
PYTHON_VERSIONS = ["3.6"]

CORE_DEPS = [
    "distribute_remove==1.0.0-4",
    "pip==18.1-1",
    "setuptools==38.2.5-1",
    "envisage==4.7.1-1",
    "click==6.7-1",
]

DOCS_DEPS = [
    "sphinx==1.5.5-5"
]

DEV_DEPS = [
    "flake8==3.3.0-2",
    "coverage==4.3.4-1",
    "testfixtures==4.10.0-1",
    "mock==2.0.0-1",
]

PIP_DEPS = [
    "stevedore==1.24.0"
]


@click.group()
def cli():
    pass


python_version_option = click.option(
    '--python-version',
    default=DEFAULT_PYTHON_VERSION,
    type=click.Choice(PYTHON_VERSIONS),
    show_default=True,
    help="Python version for the environment")


@cli.command(name="build-env", help="Creates the execution environment")
@python_version_option
def build_env(python_version):
    env_name = get_env_name(python_version)
    check_call([
        "edm", "environments", "remove", "--purge", "--force",
        "--yes", env_name])
    check_call(
        ["edm", "environments", "create", "--version", python_version,
         env_name])

    check_call([
        "edm", "install", "-e", env_name,
        "--yes"] + CORE_DEPS + DEV_DEPS + DOCS_DEPS)

    if len(PIP_DEPS):
        check_call([
            "edm", "run", "-e", env_name, "--",
            "pip", "install"] + PIP_DEPS)


@cli.command(help="Install the BDSS in the execution environment")
@python_version_option
def install(python_version):
    env_name = get_env_name(python_version)
    check_call([
        "edm", "run", "-e", env_name, "--",
        "pip", "install", "-e", "."])


@cli.command(help="Run the tests")
@python_version_option
def test(python_version):
    env_name = get_env_name(python_version)

    check_call([
        "edm", "run", "-e", env_name, "--", "python", "-m", "unittest",
        "discover"
    ])


@cli.command(help="Run flake")
@python_version_option
def flake8(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--", "flake8", "."])


@cli.command(help="Runs the coverage")
@python_version_option
def coverage(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--",
                "coverage", "run", "-m", "unittest", "discover"])


@cli.command(help="Builds the documentation")
@python_version_option
def docs(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--", "make", "html"], cwd="doc")


def get_env_name(python_version):
    return "force-py{}".format(remove_dot(python_version))


def remove_dot(python_version):
    return "".join(python_version.split('.'))


if __name__ == "__main__":
    cli()
