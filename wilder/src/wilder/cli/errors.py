import click
from click._compat import get_text_stderr
from wilder.cli.logger import get_view_error_details_message


class WilderCLIError(click.ClickException):
    """Base CLI exception. The `message` param automatically gets logged to error file and printed
    to stderr in red text. If `help` param is provided, it will also be printed to stderr after the
    message but not logged to file.
    """

    def __init__(self, message, help_func=None):
        self.help = help_func
        super().__init__(message)

    def show(self, file=None):
        """Override default `show` to print CLI errors in red text."""
        if file is None:
            file = get_text_stderr()
        click.secho(f"Error: {self.format_message()}", file=file, fg="red")
        if self.help:
            click.echo(self.help, err=True)


class LoggedCLIError(WilderCLIError):
    """Exception to be raised when wanting to point users to error logs for error details.

    If `message` param is provided it will be printed to screen along with message on where to
    find error details in the log.
    """

    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

    def format_message(self):
        locations_message = get_view_error_details_message()
        return (
            "{}\n{}".format(self.message, locations_message)
            if self.message
            else locations_message
        )


class WildServerConnectionError(WilderCLIError):
    """Exception raised when unable to connect to the Wild server."""

    def __init__(self, base_err):
        super().__init__(f"Unable to connect. Reason: {str(base_err)}")
