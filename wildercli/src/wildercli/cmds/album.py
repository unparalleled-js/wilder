import click
from wilder.errors import ArtistNotFoundError
from wildercli.options import artist_option
from wildercli.options import album_option
from wildercli.util import get_wilder_mgmt


@click.group()
def album():
    """Tools for creating albums."""
    pass


@click.command()
@artist_option()
@album_option()
def init(artist, album):
    """Start a new album."""
    mgmt = get_wilder_mgmt()
    try:
        mgmt.start_new_album(artist, album)
    except ArtistNotFoundError:
        click.echo(f"Artist '{artist}' not found.")


album.add_command(init)
