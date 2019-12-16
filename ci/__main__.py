import click
import subprocess
from subprocess import check_call

DEFAULT_PYTHON_VERSION = "3.6"
PYTHON_VERSIONS = ["3.6"]

CORE_DEPS = [
    "envisage==4.7.2-1",
    "click==7.0-1",
]

DOCS_DEPS = [
    "sphinx==1.8.5-3"
]

DEV_DEPS = [
    "flake8==3.7.7-1",
    "coverage==4.3.4-1",
    "testfixtures==4.10.0-1",
]

_nevergrad_stable_commit = "ba2c0217a043178adf9fe9f4bd52bbbfce97bfaa"
PIP_DEPS = [
    "stevedore==1.30.1",
    "git+https://github.com/facebookresearch/nevergrad.git@" +
    _nevergrad_stable_commit
]

ADDITIONAL_CORE_DEPS = [
    "numpy==1.15.4-2",
    "scipy>=1.2.1"
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
        "--yes"] + CORE_DEPS + DEV_DEPS + DOCS_DEPS + ADDITIONAL_CORE_DEPS)

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
@click.option(
    "--verbose/--quiet", default=True,
    help="Run tests in verbose mode? [default: --verbose]",
)
def test(python_version, verbose):
    env_name = get_env_name(python_version)

    verbosity_args = ["--verbose"] if verbose else []

    check_call(
        ["edm", "run", "-e", env_name, "--", "python", "-m", "unittest",
         "discover"] + verbosity_args
    )


@cli.command(help="Run flake")
@python_version_option
def flake8(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--", "flake8", "."])


@cli.command(help="Runs the coverage")
@python_version_option
def coverage(python_version):
    env_name = get_env_name(python_version)

    returncode = edm_run(
        env_name, ["coverage", "run", "-m", "unittest", "discover"])
    if returncode:
        raise click.ClickException("There were test failures.")

    returncode = edm_run(env_name, ["pip", "install", "codecov"])
    if not returncode:
        returncode = edm_run(env_name, ["codecov"])

    if returncode:
        raise click.ClickException(
            "There were errors while installing and running codecov.")


@cli.command(help="Builds the documentation")
@python_version_option
def docs(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--", "make", "html"], cwd="doc")


def get_env_name(python_version):
    return "force-py{}".format(remove_dot(python_version))


def remove_dot(python_version):
    return "".join(python_version.split('.'))


def edm_run(env_name, cmd, cwd=None):
    return subprocess.call(["edm", "run", "-e", env_name, "--"]+cmd, cwd=cwd)


if __name__ == "__main__":
    cli()
