import click
from wilder.cli.argv import alias_arg
from wilder.cli.argv import artist_name_arg
from wilder.cli.argv import artist_option
from wilder.cli.argv import bio_option
from wilder.cli.argv import format_option
from wilder.cli.argv import new_name_arg
from wilder.cli.argv import wild_options
from wilder.cli.cmds.util import echo_formatted_list
from wilder.cli.output_formats import OutputFormat
from wilder.cli.util import abridge
from wilder.cli.util import convert_to_table_none_if_needed
from wilder.lib.constants import Constants
from wilder.lib.util import noop


@click.group()
def artist():
    """Tools for artist management."""
    pass


@artist.command(cls=click.Command)
@wild_options()
@artist_option
def show(state, artist):
    """The artist information."""
    _bio = convert_to_table_none_if_needed(artist.bio)
    also_known_as = artist.also_known_as
    click.echo(f"{Constants.NAME}: {artist.name}")
    click.echo(f"{Constants.BIO}: {_bio}")
    if also_known_as:
        also_known_as = ", ".join(also_known_as)
        click.echo(f"Also known as: '{also_known_as}'")


@artist.command(Constants.LIST)
@wild_options()
@format_option
def _list(state, format):
    """List all your artists."""
    _artists = state.wilder.get_artists()
    bio_func = abridge if format == OutputFormat.TABLE else noop
    artists_list = [
        {
            Constants.NAME.capitalize(): a.name,
            Constants.BIO.capitalize(): bio_func(a.bio),
        }
        for a in _artists
    ]
    echo_formatted_list(format, artists_list)


@artist.command()
@wild_options()
@artist_name_arg
@bio_option
def new(state, artist_name, bio):
    """Manage a new artist."""
    state.wilder.create_artist(artist_name, bio=bio)


@artist.command()
@wild_options()
@artist_name_arg
def remove(state, artist_name):
    """Stop managing an artist."""
    state.wilder.delete_artist(artist_name)


@artist.command(cls=click.Command)
@wild_options()
@artist_option
@bio_option
def update(state, artist, bio):
    """Update artist information."""
    state.wilder.update_artist(artist.name, bio)


@artist.command(cls=click.Command)
@wild_options()
@artist_name_arg
def focus(state, artist_name):
    """Change the focus artist."""
    state.wilder.focus_on_artist(artist_name)


@artist.command(cls=click.Command)
@wild_options()
@artist_option
@alias_arg
def add_alias(state, artist, alias):
    """Add an artist alias."""
    state.wilder.add_alias(alias, artist_name=artist.name)


@artist.command(cls=click.Command)
@wild_options()
@artist_option
@alias_arg
def remove_alias(state, artist, alias):
    """Remove an artist alias."""
    state.wilder.remove_alias(alias, artist_name=artist.name)


@artist.command()
@wild_options()
@new_name_arg
@artist_option
@click.option(
    "--forget-old-name", help="To not store in 'Also known as'.", default=False,
)
def rename(state, new_name, artist, forget_old_name):
    """Rename an artist."""
    state.wilder.rename_artist(
        new_name, artist_name=artist.name, forget_old_name=forget_old_name
    )
