
import logging
import requests
import xmltodict

_LOGGER = logging.getLogger(__name__)

class HttpVLC():
    def __init__(self, host=None, username=None, password=None):
        self.host = host
        self.username = username or ''
        self.password = password or ''

        if self.host is None or self.host is '':
            raise("Host is empty! Input host to proceed")

        self._data = {}
        self.parse_data()

    def status_code(self, request):
        if request.status_code == 200:
            return True
        elif request.status_code == 401:
             raise('Unathorized! The provided username or password were incorrect')
        else:
            raise f"Query failed, response code: {req.status_code} Full message: {req.text}"

    def fetch_playlist(self):
        url = f"{self.host}/requests/playlist.xml"
        pass

    def fetch_status(self, command):
        url = f"{self.host}/requests/status.xml"
        if command is not None:
            url = f'{url}?command={command}'
        try:
            request = requests.get(url, auth=(self.username, self.password))
            data = xmltodict.parse(request.text, process_namespaces=True).get("root")
            return data
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
            raise f"The VLC Server is unreachable. Errorr code: {error}"

    def fetch_data(self, command=None):
        return self.fetch_status(command)


    def parse_data(self, command=None, option='state', in_information=False):
        response_data = self.fetch_data(command=command)
        if not in_information:
            return response_data.get(option) or None

        # Information Elements
        if 'information' in response_data:
            try:
                for info in response_data['information']['category']:
                    if info.get('@name') == 'meta':
                        for elem in info['info']:
                            if elem['@name'] == option:
                                return elem['#text']
            except:
                pass
        #self._data['album'] = response_data['information']['category'][''] or None

        return self._data

    def update_data(self):
        self.parse_data()

    def media_artist(self):
        """Return Current Artist playing"""
        return self.parse_data(option='artist', in_information=True) or None

    def is_fullscreen(self):
        """Return if VLC is in fullscreen"""
        return True if self.parse_data(option='fullscreen') == 'true' else False

    def aspect_ratio(self):
        """Return Aspect Ratio of media playing"""
        return self.parse_data(option='aspectratio')

    def current_playlist_id(self):
        """Return Current playlist id"""
        return self.parse_data(option='currentplid')

    def audio_delay(self):
        """Return Aspect Ratio of media playing"""
        return self.parse_data(option='audiodelay')

    def api_version(self):
        """Return API Version of VLC Server"""
        return self.parse_data(option='apiversion')

    def version(self):
        """Return Version of VLC Server"""
        return self.parse_data(option='version')

    def media_time(self):
        """Return how long the media file is"""
        return self.parse_data(option='time')

    def volume(self):
        """Return the volume of the media playing"""
        return self.parse_data(option='volume')

    def media_length(self):
        """Return the length of the media in seconds"""
        return self.parse_data(option='length')

    def is_random(self):
        """Return if shuffle is on or off"""
        return True if self.parse_data(option='random') == 'true' else False

    def rate(self):
        """Return the rate"""
        return self.parse_data(option='rate')

    def state(self):
        """Return the state of the media file"""
        return self.parse_data(option='state')

    def is_looped(self):
        """Return if VLC is set on loop"""
        return self.parse_data(option='loop')

    def position(self):
        """Return the position of the playback """
        return self.parse_data(option='position')

    def is_on_repeat(self):
        """Return if playback is set on repeat """
        return self.parse_data(option='repeat')

    def album(self):
        """Get the album playing, if none it returns None """
        return self.parse_data(option='album', in_information=True) or None

    def track_number(self):
        """Get the track_number playing, if none it returns None """
        return self.parse_data(option='track_number', in_information=True) or None

    def filename(self):
        """Get the filename """
        return self.parse_data(option='filename', in_information=True) or None

    def title(self):
        """Get the title playing, if none it returns None """
        return self._data.get('title') or None

    def subtitle_delay(self):
        """Return the set delay for subtitles """
        return self.parse_data(option='subtitledelay')

    def set_volume(self, volume):
        """Set volume level, range 0..1."""
        new_volume = str(int(volume * 256))
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

    def pause(self):
        """Pause playback"""
        return self.parse_data(command="pl_pause")

    def play(self):
        """Start playing media playback"""
        return self.parse_data(command="pl_play")