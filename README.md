# python-vlc-http
Pip module for sending http requests to a VLC Server

# Installation

`pip install python-vlc-http`

# How to use

```python
from python_vlc_http import HttpVLC

vlc_client = HttpVLC('host', 'username', 'password')

fullscreen_status = vlc_client.is_fullscreen()

if(fullscreen_status):
   print('VLC is running on fullscreen!')

```

**NOTE:** Host follows the format of http://thisissomeaddrress.com:[PORT NUMBER HERE] else it will raise an exception!


# Methods
 
 
* `album()`

    Get the album playing, if none it returns None

* `api_version()`

    Return API Version of VLC Server

* `artist()`

    Get the artist playing, if none it returns None

* `aspect_ratio()`

    Return Aspect Ratio of media playing

* `audio_delay()`

    Return Aspect Ratio of media playing

* `clear_queue()`

    Clear media in queue

* `filename()`

    Get the filename

* `is_fullscreen()`

    Return if VLC is in fullscreen

* `is_looped()`

    Return if VLC is set on loop
    
* `is_on_repeat()`

    Return if playback is set on repeat

* `is_random()`

    Return if shuffle is on or off

* `media_artist()`

    Return Current Artist playing

* `media_length()`

    Return the length of the media in seconds

* `media_time()`

    Return how long the media file is

* `next_track()`

    Play next media in queue

* `position()`

    Return the position of the playback

* `previous_track()`

    Play previous media in queue

* `rate()`

    Return the rate

* `set_volume(volume)`

    Set volume level, range 0..1.

* `shuffle()`

    Set shuffle mode

* `state()`

    Return the state of the media file

* `stop()`

    Send stop command.

* `subtitle_delay()`

    Return the set delay for subtitles

* `title()`

    Get the title playing, if none it returns None
    
* `toggle_fullscreen()`

    Toggle Fullscreen

* `track_number()`

    Get the track_number playing, if none it returns None

* `volume()`

    Return the volume of the media playing
    
* `play()`

    Start playing media playback

* `pause()`

    Pause playback
