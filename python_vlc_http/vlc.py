
import logging
import requests
import xmltodict

_LOGGER = logging.getLogger(__name__)

class HttpVLC():
    def __init__(self, host=None, username=None, password=None):
        self.host = host
        self.username = username or ''
        self.password = password or ''
        self._data = {}
        self.parse_data()

        if self.host is None or self.host is '':
            raise("Host is empty! Input host to proceed")

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


    def parse_data(self):
        response_data = self.fetch_data(command=None)
        # Root Elements
        self._data['fullscreen'] = True if response_data['fullscreen'] == 'true' else False
        self._data['aspectratio'] = response_data.get('aspectratio') or None
        self._data['audiodelay'] = response_data['audiodelay']
        self._data['apiversion'] = response_data['apiversion']
        self._data['currentplid'] = response_data['currentplid']
        self._data['time'] = response_data['time']
        self._data['volume'] = response_data['volume']
        self._data['length'] = response_data['length']
        self._data['random'] = True if response_data['random'] == 'true' else False
        self._data['state'] = response_data['state']
        self._data['version'] = response_data['version']
        self._data['position'] = response_data['position']
        self._data['repeat'] = response_data['repeat']
        self._data['subtitledelay'] = response_data['subtitledelay']
        self._data['rate'] = response_data['rate']
        self._data['loop'] = response_data['loop']
        self._data['track_number'] = response_data['loop']
        self._data['loop'] = response_data['loop']
        self._data['loop'] = response_data['loop']

        # Information Elements
        if 'information' in response_data:
            try:
                for info in response_data['information']['category']:
                    if info.get('@name') == 'meta':
                        for elem in info['info']:
                            self._data[elem['@name']] = elem['#text']
            except:
                pass
        #self._data['album'] = response_data['information']['category'][''] or None

        return self._data

    def media_artist(self):
        """Return Current Artist playing"""
        return self._data.get('artist') or None

    def is_fullscreen(self):
        """Return if VLC is in fullscreen"""
        return self._data['fullscreen']

    def aspect_ratio(self):
        """Return Aspect Ratio of media playing"""
        return self._data['aspectratio']

    def audio_delay(self):
        """Return Aspect Ratio of media playing"""
        return self._data['audiodelay']

    def api_version(self):
        """Return API Version of VLC Server"""
        return self._data['apiversion']

    def media_time(self):
        """Return how long the media file is"""
        return self._data['time']

    def volume(self):
        """Return the volume of the media playing"""
        return self._data['volume']

    def media_length(self):
        """Return the length of the media in seconds"""
        return self._data['length']

    def is_random(self):
        """Return if shuffle is on or off"""
        return self._data['random']

    def rate(self):
        """Return the rate"""
        return self._data['rate']

    def state(self):
        """Return the state of the media file"""
        return self._data['state']

    def is_looped(self):
        """Return if VLC is set on loop"""
        return self._data['loop']

    def position(self):
        """Return the position of the playback """
        return self._data['position']

    def is_on_repeat(self):
        """Return if playback is set on repeat """
        return self._data['repeat']

    def album(self):
        """Get the album playing, if none it returns None """
        return self._data.get('album') or None

    def track_number(self):
        """Get the track_number playing, if none it returns None """
        return self._data.get('track_number') or None

    def filename(self):
        """Get the filename """
        return self._data.get('filename') or None

    def title(self):
        """Get the title playing, if none it returns None """
        return self._data.get('title') or None

    def subtitle_delay(self):
        """Return the set delay for subtitles """
        return self._data['subtitledelay']

    def set_volume(self, volume):
        """Set volume level, range 0..1."""
        new_volume = str(int(volume * 256))
        return self.fetch_data(command=f"volume&val={new_volume}")

    def stop(self):
        """Send stop command."""
        return self.fetch_data(command="pl_stop")

    def previous_track(self):
        """Play previous media in queue """
        return self.fetch_data(command="pl_previous")

    def next_track(self):
        """Play next media in queue """
        return self.fetch_data(command="pl_next")

    def clear_queue(self):
        """Clear media in queue """
        return self.fetch_data(command="pl_empty")

    def shuffle(self):
        """Set shuffle mode """
        return self.fetch_data(command="pl_random")

    def toggle_fullscreen(self):
        """Toggle Fullscreen"""
        return self.fetch_data(command="fullscreen")

    def pause(self):
        """Pause playback"""
        return self.fetch_data(command="pl_pause")

    def play(self):
        """Start playing media playback"""
        return self.fetch_data(command="pl_play")