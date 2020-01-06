import click
import os
import shutil
import subprocess
from subprocess import check_call

DEFAULT_PYTHON_VERSION = "3.6"
PYTHON_VERSIONS = ["3.6"]

CORE_DEPS = ["envisage==4.7.2-1", "click==7.0-1"]

DOCS_DEPS = ["sphinx==1.8.5-3"]

DEV_DEPS = ["flake8==3.7.7-1", "coverage==4.3.4-1", "testfixtures==4.10.0-1"]

PIP_DEPS = ["stevedore==1.30.1"]

ADDITIONAL_CORE_DEPS = ["numpy==1.15.4-2"]


@click.group()
def cli():
    pass


python_version_option = click.option(
    "--python-version",
    default=DEFAULT_PYTHON_VERSION,
    type=click.Choice(PYTHON_VERSIONS),
    show_default=True,
    help="Python version for the environment",
)


@cli.command(name="build-env", help="Creates the execution environment")
@python_version_option
def build_env(python_version):
    env_name = get_env_name(python_version)
    check_call(
        [
            "edm",
            "environments",
            "remove",
            "--purge",
            "--force",
            "--yes",
            env_name,
        ]
    )
    check_call(
        [
            "edm",
            "environments",
            "create",
            "--version",
            python_version,
            env_name,
        ]
    )

    check_call(
        ["edm", "install", "-e", env_name, "--yes"]
        + CORE_DEPS
        + DEV_DEPS
        + DOCS_DEPS
        + ADDITIONAL_CORE_DEPS
    )

    if len(PIP_DEPS):
        check_call(
            ["edm", "run", "-e", env_name, "--", "pip", "install"] + PIP_DEPS
        )


@cli.command(help="Install the BDSS in the execution environment")
@python_version_option
def install(python_version):
    env_name = get_env_name(python_version)
    check_call(
        ["edm", "run", "-e", env_name, "--", "pip", "install", "-e", "."]
    )


@cli.command(help="Run the tests")
@python_version_option
@click.option(
    "--verbose/--quiet",
    default=True,
    help="Run tests in verbose mode? [default: --verbose]",
)
def test(python_version, verbose):
    env_name = get_env_name(python_version)

    verbosity_args = ["--verbose"] if verbose else []

    returncode = edm_run(
        env_name, ["python", "-m", "unittest", "discover"] + verbosity_args
    )

    if returncode:
        raise click.ClickException("There were test failures.")


@cli.command(help="Run flake")
@python_version_option
def flake8(python_version):
    env_name = get_env_name(python_version)

    returncode = edm_run(env_name, ["flake8", "."])
    if returncode:
        raise click.ClickException(
            "Flake8 exited with exit status {}".format(returncode)
        )


@cli.command(help="Runs the coverage")
@python_version_option
def coverage(python_version):
    env_name = get_env_name(python_version)

    returncode = edm_run(
        env_name, ["coverage", "run", "-m", "unittest", "discover"]
    )
    if returncode:
        raise click.ClickException("There were test failures.")

    returncode = edm_run(env_name, ["pip", "install", "codecov"])
    if not returncode:
        returncode = edm_run(env_name, ["codecov"])

    if returncode:
        raise click.ClickException(
            "There were errors while installing and running codecov."
        )


@cli.command(help="Builds the documentation")
@python_version_option
@click.option("--apidoc-only", is_flag=True, help="Only generate API docs.")
@click.option(
    "--html-only",
    is_flag=True,
    help="Only generate HTML documentation (requires API docs in source/api).",
)
def docs(python_version, apidoc_only, html_only):
    if apidoc_only and html_only:
        raise click.ClickException("Conflicting request in the invocation.")

    env_name = get_env_name(python_version)
    doc_api = os.path.abspath(os.path.join("doc", "source", "api"))
    package = os.path.abspath("force_bdss")

    if not html_only:
        click.echo("Generating API doc")
        if os.path.exists(doc_api):
            shutil.rmtree(doc_api)
        returncode = edm_run(
            env_name, ["sphinx-apidoc", "-o", doc_api, package, "*tests*"]
        )
        if returncode:
            raise click.ClickException(
                "There were errors while building the API doc."
            )

    if not apidoc_only:
        click.echo("Generating HTML")
        returncode = edm_run(env_name, ["make", "html"], cwd="doc")
        if returncode:
            raise click.ClickException(
                "There were errors while building HTML documentation."
            )


def get_env_name(python_version):
    return "force-py{}".format(remove_dot(python_version))


def remove_dot(python_version):
    return "".join(python_version.split("."))


def edm_run(env_name, cmd, cwd=None):
    return subprocess.call(["edm", "run", "-e", env_name, "--"] + cmd, cwd=cwd)


if __name__ == "__main__":
    cli()
