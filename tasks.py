import dataclasses
import pathlib

import invoke

#############
# CONSTANTS #
#############

PACKAGE = "pod"

###################
# GETTING STARTED #
###################


@invoke.task
def help(ctx):
    """
    Displays help text
    """
    ctx.run("inv -l", pty=True)


@invoke.task()
def install(ctx, skip_install_playwright: bool = False):
    """
    Install system dependencies necessary for the pod project.

    This task optionally skips the installation of Playwright dependencies,
    which is useful for CI pipelines where Playwright is not needed,
    thereby improving the build performance.
    """
    _title("Installing Dependencies")
    ctx.run("uv sync")

    if not skip_install_playwright:
        _title("Installing Playwright Dependencies")
        ctx.run("uv run playwright install --with-deps")


#####################
# QUALITY ASSURANCE #
#####################


@invoke.task
def format(ctx, check: bool = False) -> None:  # noqa: A001
    """
    Apply automatic code formatting tools

    By default, this modifies files to match coding style guidelines.
    When `check` is True, it performs a dry-run to identify non-compliant
    files without applying changes.
    """
    suffix = " (check only)" if check else ""
    _title(f"Applying code formatters{suffix}")
    ctx.run(f"uv run ruff format src{' --check' if check else ''}")
    ctx.run(f"uv run ruff check --select I{' --fix' if not check else ''} src")


@invoke.task
def typing(ctx):
    """
    Check type annotations
    """
    _title("Type checking")
    # PYTHONPATH must include the `src` folder for django-stubs to find the settings
    # module
    src_path = str((pathlib.Path() / "src").absolute())
    with ctx.prefix(f"export PYTHONPATH=${{PYTHONPATH}}:{src_path}"):
        try:
            ctx.run(f"uv run dmypy run -- src/{PACKAGE}")
        except invoke.exceptions.UnexpectedExit:
            print(
                "\n"
                "NOTE: mypy was run in daemon mode, which can lead to spurious\n"
                "errors when changing branches.\n"
                "If the errors observed do not make sense, or errors are occuring\n"
                "on known-good code run `inv typing-daemon-stop` to stop the\n"
                "dmypy daemon and run type checking again."
            )
            raise


@invoke.task
def typing_daemon_stop(ctx):
    """
    Stop the mypy typing daemon

    Sometimes dmypy gets itself confused and needs to be stopped
    """
    _title("Terminating type checking Daemon")
    ctx.run("uv run dmypy stop")


@invoke.task
def lint(ctx, fix=False):
    """
    Check linting in the src folder
    """
    _title(f"Linting code {'' if fix else '(check only)'}")
    ctx.run(f"uv run ruff check{' --fix ' if fix else ''} src")


@invoke.task
def check_migrations(ctx):
    """
    Check for potential vulnerabilities in packages
    """
    _title("Checking for missing migrations")
    try:
        ctx.run(
            f"uv run ./src/{PACKAGE}/manage.py makemigrations --dry-run --check",
            pty=True,
        )
    except invoke.exceptions.UnexpectedExit:
        print(
            "\n"
            "There are model changes with no migrations generated for them. "
            f"Run `./src/{PACKAGE}/manage.py makemigrations` to generate migrations, "
            "and don't forget to commit the new migration files!"
        )
        raise


@invoke.task(typing, lint, check_migrations)
def check(ctx):
    """
    Runs all the code checking tools
    """
    print("All checks completed successfully 🕺")


############
# BUILDING #
############


@invoke.task
def build_presentation(ctx):
    """
    Build the pod presentation
    """
    _title("Building presentation")
    ctx.run("mkdir -p dist")
    ctx.run(
        "typst compile"
        " --font-path=src/presentation/fonts"
        " --ignore-system-fonts"
        " src/presentation/main.typ dist/presentation.pdf",
    )


###########
# HELPERS #
###########
def _title(text):
    print(f"== {text.upper()} ==")
