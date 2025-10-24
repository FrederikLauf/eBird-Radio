# eBird-Radio
Python command line application for listening to random bird songs from ebird.org by means of selenium browser automation.
## Instructions

Selenium specific parameters can be configured in eBirdRadio_config.yml.

Start the radio session with
```
python eBirdRadio.py
```
In a radio session, a configured number of random bird species pages on ebird.org is opened and the audio player is opened with a configured timing.
The script accepts three non-mandatory positional arguments:
- number of birds (default 5)
- time between opening and closing the audio player for each song (default 10s)
- time before opening and after closing the audio player for each song (default 2s)
```
python eBirdRadio.py 5 10 2  # default values
python eBirdRadio.py 50  # 50 birds with default timing
```
