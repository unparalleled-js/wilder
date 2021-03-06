import os

from wilder.lib.constants import Constants
from wilder.lib.enum import AudioType
from wilder.lib.errors import AudioTypeNotFoundError
from wilder.lib.errors import NoAudioFoundError
from wilder.lib.errors import UnsupportedAudioTypeError
from wilder.lib.mgmt.album_dir import get_track_dir_json
from wilder.lib.mgmt.album_dir import get_track_json_path
from wilder.lib.mgmt.album_dir import get_track_path
from wilder.lib.mgmt.album_dir import init_track_dir
from wilder.lib.util.conversion import to_int
from wilder.lib.util.sh import remove_file_if_exists
from wilder.lib.util.sh import rename_directory
from wilder.lib.util.sh import save_json_as


class Track:
    def __init__(
        self,
        path,
        name,
        track_number,
        artist,
        album,
        description=None,
        collaborators=None,
    ):
        self.path = path
        self.name = name
        self._track_number = track_number
        self.artist = artist
        self.album = album
        self.description = description
        self.collaborators = collaborators

    @property
    def track_number(self):
        return to_int(self._track_number)

    @track_number.setter
    def track_number(self, track_number):
        self._track_number = to_int(track_number)

    @property
    def dir_json_path(self):
        """The path to the track JSON file."""
        return get_track_json_path(self.path)

    @property
    def mp3_path(self):
        """The path to the mp3 file for this track, if it exists."""
        return self._get_audio_file_path("mp3")

    @property
    def wav_path(self):
        """The path to the mp3 file for this track, if it exists."""
        return self._get_audio_file_path("wav")

    @property
    def flac_path(self):
        """The path to the FLAC file for this track, if it exists."""
        return self._get_audio_file_path("flac")

    def get_file(self, audio_type=None):
        """Returns the path to the file for the given audio type extension."""
        if not audio_type:
            return self._try_get_first_audio_file_found()
        else:
            return self._get_file(audio_type)

    def _try_get_first_audio_file_found(self):
        audio_types = AudioType.choices()
        for ext in audio_types:
            try:
                return self._get_file(ext)
            except AudioTypeNotFoundError:
                pass
        raise NoAudioFoundError(self.name)

    def _get_file(self, audio_type):
        audio_type = audio_type.lower()
        try:
            if audio_type == AudioType.MP3:
                return _get_path_if_exists(self.mp3_path)
            elif audio_type == AudioType.WAV:
                return _get_path_if_exists(self.wav_path)
            elif audio_type == AudioType.FLAC:
                return _get_path_if_exists(self.flac_path)
            raise UnsupportedAudioTypeError(audio_type)
        except FileNotFoundError:
            raise AudioTypeNotFoundError(self.name, audio_type)

    def _get_audio_file_path(self, ext):
        return os.path.join(self.path, f"{self.name}.{ext}")

    @classmethod
    def from_json(cls, album_json, track_name):
        """Creates a Track from JSON stored in the album dir."""
        album_path = album_json.get(Constants.PATH)
        album_name = album_json.get(Constants.NAME)
        artist_name = album_json.get(Constants.ARTIST)
        track_path = get_track_path(album_path, track_name)
        track_json = get_track_dir_json(track_path, track_name, artist_name, album_name)
        track_number = track_json.get(Constants.TRACK_NUMBER) or 1
        description = track_json.get(Constants.DESCRIPTION)
        collaborators = track_json.get(Constants.COLLABORATORS)
        return cls(
            track_path,
            track_name,
            track_number,
            artist_name,
            album_name,
            description=description,
            collaborators=collaborators,
        )

    def init_dir(self):
        """Initialize the track directory with the default files."""
        init_track_dir(self.path, self.name, self.artist, self.album)

    def to_json_for_track_dir(self):
        """Convert this object to JSON for the file in the track directory."""
        return {
            Constants.ARTIST: self.artist,
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.TRACK_NUMBER: self.track_number,
            Constants.COLLABORATORS: self.collaborators,
        }

    def update(self, track_number=None, description=None, collaborators=None):
        """Update track metadata."""
        self.track_number = track_number or self.track_number
        self.description = description or self.description
        self.collaborators = collaborators or self.collaborators
        self.save_track_metadata()

    def rename(self, new_name):
        """Renames the track. Warning: use album.rename_track() to update album metadata."""
        self.name = new_name
        self.path = rename_directory(self.path, new_name)
        self.save_track_metadata()

    def save_track_metadata(self):
        """Save this instance's data to the file in the track directory."""
        remove_file_if_exists(self.dir_json_path)
        full_json = self.to_json_for_track_dir()
        save_json_as(self.dir_json_path, full_json)
        return self


def _get_path_if_exists(path):
    if os.path.isfile(path):
        return path
    raise FileNotFoundError(path)
