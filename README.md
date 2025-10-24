# eBird-Radio
Python command line application for listening to random bird songs from ebird.org by means of selenium browser automation.
## Instructions

Selenium specific parameters can be configured in eBirdRadio_config.yml. (See below.)

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
During the session, informations about bird species and recordings are printed in the command line.
## Hints for selenium specific configuration
Tested example configurations of eBirdRadio_config.yml:

### Brave browser under Windows 11
```
browser:
  type: 'Chrome'
  binary_location: "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
  driver_location: null
```
### Edge under Windows 11
```
browser:
  type: 'Edge'
  binary_location: null
  driver_location: null
```
### Firefox under Ubuntu
```
browser:
  type: 'Firefox'
  binary_location: null
  driver_location: /snap/bin/geckodriver
```
