import click
from distutils.version import StrictVersion
from subprocess import check_call, check_output
import os

DEFAULT_PYTHON_VERSION = "3.6"
PYTHON_VERSIONS = ["3.6"]
PYTHON_NAMES = {"3.6": "py36"}
PLATFORMS = ["osx-x86_64", "rh6-x86_64", "win-x86_64"]

BUNDLE_PATH = os.path.join(os.path.dirname(__file__), "bundle")
BUNDLE_NAME_TPL = "force-{python_version}-{platform}.json"

EDM_DEPS = [
    # Run `ci generate-edm-bundles` to reflect the updates

    # core
    "envisage",
    "click",

    # doc
    "sphinx",

    # CI
    "flake8",
    "coverage",
    "testfixtures",
]

PIP_DEPS = [
    "stevedore==1.30.1"
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


@cli.command(name="generate-edm-bundles")
def generate_edm_bundles():
    """ Generate EDM bundles for all the target platforms. """

    # Requires EDM 1.11.0 or higher to work without authentication.
    min_edm = "1.11.0"
    edm_ver = check_output(
        ["edm", "--version"], universal_newlines=True).split()[1]
    if StrictVersion(edm_ver) < StrictVersion(min_edm):
        raise click.ClickException(
            "Bundles can only be generated with EDM >= {}. {} found."
            .format(min_edm, edm_ver))

    for platform in PLATFORMS:
        for python_version in PYTHON_VERSIONS:
            output_file = os.path.join(
                BUNDLE_PATH,
                BUNDLE_NAME_TPL.format(
                    python_version=PYTHON_NAMES[python_version],
                    platform=platform
                )
            )
            click.echo("Creating bundle: {}".format(output_file))
            check_call(
                [
                    "edm", "bundle", "generate", "--bundle-format", "2.0",
                    "--platform", platform, "--version", python_version,
                    "--output-file", output_file
                ] + EDM_DEPS
            )

    click.echo("Done.\n"
               "Remember to push significant updates to the repository.")


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
