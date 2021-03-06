import click
from wilder.cli.clickext.options import incompatible_with
from wilder.cli.clickext.types import FileOrString
from wilder.cli.output_formats import OutputFormat
from wilder.cli.select import get_user_selected_resource
from wilder.cli.wild_factory import get_wilder
from wilder.lib.config import create_config_object
from wilder.lib.constants import Constants
from wilder.lib.enum import AlbumStatus
from wilder.lib.enum import AlbumType
from wilder.lib.enum import AudioType


yes_option = click.option(
    "-y",
    "--assume-yes",
    is_flag=True,
    expose_value=False,
    callback=lambda ctx, param, value: ctx.obj.set_assume_yes(value),
    help='Assume "yes" as the answer to all prompts and run non-interactively.',
)
song_option = click.option(
    "-s", "--song", help="A path to a song.", type=FileOrString()
)
format_option = click.option(
    "-f",
    "--format",
    type=click.Choice(OutputFormat(), case_sensitive=False),
    help="The output format of the result. Defaults to table format.",
    default=OutputFormat.TABLE,
)
bio_option = click.option("--bio", "--biography", help="The artist biography.")
artist_option = click.option(
    "--artist",
    help="The name of an artist.",
    callback=lambda ctx, param, arg: _get_artist(ctx.obj.wilder, arg),
)
track_num_option = click.option(
    "--track-number", "--track-num", help="The number the track is on the album."
)
collaborator_option = click.option(
    "--collaborator", help="Additional artists on the track", multiple=True
)
hard_option = click.option(
    "--hard", help="To permanently delete associated files.", is_flag=True
)
audio_type_option = click.option(
    "--audio-type",
    help="The audio file extension of the track to play.",
    type=click.Choice(AudioType.choices(), case_sensitive=False),
)


def _get_artist(wilder, artist):
    _artist = wilder.get_artist(artist)
    if _artist:
        return _artist
    artists = wilder.get_artist_names()
    artist_name_chosen = get_user_selected_resource(Constants.ARTIST, artists)
    return wilder.get_artist(artist_name_chosen)


class CLIState:
    def __init__(self):
        self._sdk = None
        self._config = None
        self.assume_yes = False

    @property
    def wilder(self):
        if self._sdk is None:
            self._sdk = get_wilder()
        return self._sdk

    @property
    def config(self):
        if self._config is None:
            self._config = create_config_object()
        return self._config

    def set_assume_yes(self, param):
        self.assume_yes = param


pass_state = click.make_pass_decorator(CLIState, ensure=True)


def album_option(required=False):
    return click.option("--album", help="The name of an album.", required=required)


def track_option(required=False):
    return click.option("--track", "-t", help="The name of a track.", required=required)


def all_option(item_type):
    return click.option(
        "--all",
        help=f"To get all {item_type}s across all artists.",
        is_flag=True,
        cls=incompatible_with([item_type]),
    )


def new_name_option(required=False):
    return click.option(
        "--new-name",
        help="The name that will replace the current name.",
        required=required,
    )


def description_option(_help):
    return click.option("--description", "--desc", help=_help)


def wild_options():
    def decorator(f):
        f = pass_state(f)
        return f

    return decorator


def update_album_options():
    def decorator(f):
        f = description_option(_help="A description for the album.")(f)
        f = click.option(
            "--album-type",
            help="The type of album.",
            type=click.Choice(AlbumType.choices()),
        )(f)
        f = click.option(
            "--status",
            help="The current status of the album.",
            type=click.Choice(AlbumStatus.choices()),
        )(f)
        f = wild_options()(f)
        f = artist_option(f)
        return f

    return decorator


artist_name_arg = click.argument("artist-name")
album_name_arg = click.argument("album-name")
track_name_arg = click.argument("track-name")
alias_arg = click.argument("alias")
new_name_arg = click.argument("new_name")
