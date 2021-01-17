import json
import signal
import sys

import click
from wilder.cli.argv import wild_options
from wilder.cli.clickext.groups import ExceptionHandlingGroup
from wilder.cli.cmds.album import album
from wilder.cli.cmds.artist import artist
from wilder.cli.cmds.config import config
from wilder.cli.cmds.dev import dev
from wilder.cli.cmds.track import track
from wilder.cli.logger import get_cli_error_log_path
from wilder.lib.config import get_config_json
from wilder.lib.constants import Constants
from wilder.server.main import run


BANNER = """\b
 |#  ^^  |#  ^#  ^#      |#~~~~#   |#~~~~  ^#~~~~~#
 |#  |#  |#  |#  |#      |#    *#  |#      |#    *#
 |#  |#  |#  |#  |#      |#    *#  |#~~~   |#~~~~#
 |#  |#  |#  |#  |#      |#    *#  |#      |#    *#
 |#~~# #~~#  |#  |#~~~~  |#~~~~#   |#~~~~  |#     #~
"""


def exit_on_interrupt(signal, frame):
    """Handle KeyboardInterrupts by just exiting instead of printing out a stack."""
    click.echo(err=True)
    sys.exit(1)


signal.signal(signal.SIGINT, exit_on_interrupt)
CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 200,
}


@click.group(cls=ExceptionHandlingGroup, context_settings=CONTEXT_SETTINGS, help=BANNER)
@wild_options()
def cli(state):
    """The Wild CLI."""
    pass


@click.command()
@wild_options()
def mgmt(state):
    """Show the full MGMT JSON blob."""
    _json = state.wilder.get_mgmt()
    _json = json.dumps(_json, indent=2)
    click.echo(_json)


@click.command()
@click.option(
    "--last-n-lines", "-l", help="The last number of lines to show.", default=10
)
def logs(last_n_lines):
    """Show the last n lines of the CLI error logs."""
    logs_path = get_cli_error_log_path()
    try:
        with open(logs_path) as log_file:
            lines = log_file.readlines()
            length = len(lines)
            for line in lines[length - last_n_lines :]:
                line_data = line.strip()
                if line_data:
                    click.echo(f"- {line_data}")
    except FileNotFoundError:
        return []


@click.command()
def start_server():
    """Start the wilder server."""
    import os

    os.chdir("..")
    exit(1)
    _config = get_config_json().get(Constants.CLIENT)
    host = _config.get(Constants.HOST, Constants.DEFAULT_HOST)
    port = _config.get(Constants.PORT, Constants.DEFAULT_PORT)
    run(host, port)


cli.add_command(album)
cli.add_command(artist)
cli.add_command(track)
cli.add_command(config)
cli.add_command(mgmt)
cli.add_command(dev)
cli.add_command(logs)
cli.add_command(start_server)
