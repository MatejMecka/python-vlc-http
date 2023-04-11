import logging
import requests

_LOGGER = logging.getLogger(__name__)

class InvalidCredentials(Exception):
    """Exception related to Invalid Credentials"""
    pass

class RequestFailed(Exception):
    """Exception related to an Invalid Request"""
    pass

class MissingHost(Exception):
    """Exception related when a host is missing"""
    pass

class HttpVLC:
    def __init__(self, host=None, username=None, password=None):
        self.host = host
        self.username = username or ""
        self.password = password or ""

        if self.host is None or self.host == "":
            raise MissingHost("Host is empty! Input host to proceed")

        self._data = {}
        self.parse_data()

    def status_code(self, request):
        if request.status_code == 200:
            return True
        elif request.status_code == 401:
             raise InvalidCredentials("Unathorized! The provided username or password were incorrect")
        else:
            raise RequestFailed(f"Query failed, response code: {request.status_code} Full message: {request.text}")

    def fetch_api(self, resource, param=""):
        try:
            url = f"{self.host}/requests/{resource}.json?{param}"
            response = requests.get(url, auth=(self.username, self.password))
            self.status_code(response)
            return response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
            raise RequestFailed(f"The VLC Server is unreachable. Error code: {error}")

    def fetch_browse(self, path):
        param = ""
        if path is not None:
            param = "dir=" + path
        return self.fetch_api("browse", param)
    
    def fetch_playlist(self, name=None):
        playlist = self.fetch_api("playlist")
        if name is not None:
            child = [element for element in playlist["children"] if element["name"] == name]
            return child
        return playlist

    def fetch_status(self, command=None):
        param = ""
        if command is not None:
            param = f"command={command}"
        return self.fetch_api("status", param)

    def fetch_data(self, command=None):
        return self.fetch_status(command)

    def parse_meta(self, option):
        return self.parse_data(option=option, in_information=True)

    def parse_data(self, command=None, option="state", in_information=False):
        response_data = self.fetch_data(command=command)
        if not in_information:
            return response_data.get(option) or None

        # Information Elements
        info = response_data.get("information")
        if info and info.get("category"):
            meta = info.get("category").get("meta")
            if meta and option in meta:
                return meta.get(option)

        return self._data

    def update_data(self):
        self.parse_data()

    def media_artist(self):
        """Return Current Artist playing"""
        return self.parse_meta(option="artist") or None

    def is_fullscreen(self):
        """Return if VLC is in fullscreen"""
        return True if self.parse_data(option="fullscreen") == 1 else False

    def aspect_ratio(self):
        """Return Aspect Ratio of media playing"""
        return self.parse_data(option="aspectratio")

    def current_playlist_id(self):
        """Return Current playlist id"""
        return self.parse_data(option="currentplid")

    def audio_delay(self):
        """Return Aspect Ratio of media playing"""
        return self.parse_data(option="audiodelay")

    def api_version(self):
        """Return API Version of VLC Server"""
        return self.parse_data(option="apiversion")

    def version(self):
        """Return Version of VLC Server"""
        return self.parse_data(option="version")

    def media_time(self):
        """Return how long the media file is"""
        return self.parse_data(option="time")

    def volume(self):
        """Return the volume of the media playing"""
        return self.parse_data(option="volume")

    def media_length(self):
        """Return the length of the media in seconds"""
        return self.parse_data(option="length")

    def is_random(self):
        """Return if shuffle is on or off"""
        return self.parse_data(option="random")

    def rate(self):
        """Return the rate"""
        return self.parse_data(option="rate")

    def state(self):
        """Return the state of the media file"""
        return self.parse_data(option="state")

    def is_looped(self):
        """Return if VLC is set on loop"""
        return self.parse_data(option="loop")

    def position(self):
        """Return the position of the playback """
        return self.parse_data(option="position")

    def is_on_repeat(self):
        """Return if playback is set on repeat """
        return self.parse_data(option="repeat")

    def album(self):
        """Get the album playing, if none it returns None """
        return self.parse_meta(option="album") or None

    def track_number(self):
        """Get the track_number playing, if none it returns None """
        return self.parse_meta(option="track_number") or None

    def filename(self):
        """Get the filename """
        return self.parse_meta(option="filename") or None

    def title(self):
        """Get the title playing, if none it returns None """
        return self.parse_meta(option="title") or None

    def subtitle_delay(self):
        """Return the set delay for subtitles """
        return self.parse_data(option="subtitledelay")

    def set_volume(self, volume):
        """Set volume level, range 0..1."""
        new_volume = str(int(volume * 320))
        return self.parse_data(command=f"volume&val={new_volume}")

    def stop(self):
        """Send stop command."""
        return self.parse_data(command="pl_stop")

    def previous_track(self):
        """Play previous media in queue """
        return self.parse_data(command="pl_previous")

    def next_track(self):
        """Play next media in queue """
        self.parse_data(command="pl_next")

    def clear_queue(self):
        """Clear media in queue """
        return self.parse_data(command="pl_empty")

    def shuffle(self):
        """Set shuffle mode """
        return self.parse_data(command="pl_random")

    def toggle_fullscreen(self):
        """Toggle Fullscreen"""
        return self.parse_data(command="fullscreen")

    def pause(self, force=False):
        """Pause playback"""
        return self.parse_data(command="pl_forcepause" if force else "pl_pause")

    def resume(self):
        """Resume playback"""
        return self.parse_data(command="pl_forceresume")

    def play(self):
        """Start playing media playback"""
        return self.parse_data(command="pl_play")

    def play_playlist_item(self, id=0):
        """Start playing a specific item from a playlist"""
        return self.parse_data(command=f"pl_play&id={id}")

    def delete_playlist_item(self, id=0):
        """Delete a specific item from a playlist"""
        return self.parse_data(command=f"pl_delete&id={id}")

    def seek(self, val):
        """Seek to a part of a video."""
        return self.parse_data(command=f"seek&val={val}")

    def sub_delay(self, val):
        """Select the subtitle delay for a video."""
        return self.parse_data(command=f"subdelay&val={val}")

    def subtitle_track(self, val):
        """Select the subtitle track for a video."""
        return self.parse_data(command=f"subtitle_track&val={val}")

    def video_track(self, val):
        """Select the video track for a particular media file."""
        return self.parse_data(command=f"video_track&val={val}")

    def set_rate(self, val):
        """Set the rate for a current media file"""
        if val > 0:
            return self.parse_data(command=f"rate&val={val}")
        raise Exception("The rate must be grater than zero.")

    def stats(self):
        """Return stats"""
        return self.parse_data(option="stats")    

    def audiofilters(self):
        """Return audiofilters"""
        return self.parse_data(option="audiofilters")    

    def videoeffects(self):
        """Return videoeffects"""
        return self.parse_data(option="videoeffects")

    def equalizer(self):
        """Return equalizer"""
        return self.parse_data(option="equalizer")
    
    def date(self):
        """Get the track date playing, if none it returns None """
        return self.parse_meta(option="date") or None

    def genre(self):
        """Get the track genre playing, if none it returns None """
        return self.parse_meta(option="genre") or None

    def publisher(self):
        """Get the track publisher playing, if none it returns None """
        return self.parse_meta(option="publisher") or None

    def artwork_url(self):
        """Get the track artwork_url playing, if none it returns None """
        return self.parse_meta(option="artwork_url") or None    
    
    def chapter(self):
        """Return chapter"""
        pass

    def chapters(self):
        """Return chapters"""
        pass