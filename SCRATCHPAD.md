# Goals

## Completed

 - [x] Find the right media server, connect
 - [x] Record streaming media to file

 ## Dropped
 - [ ] Tag the recorded AAC file with date/time info
    - Will be putting these on my phone, not burning to a CD, so "day-of" recording is good enough
 - [ ] Use wordlist to give distinct names to files/sessions/tracks
    - Same as above, phone has much better UI than car stereo
 - [ ] Strip out commercials (stretch goal)
    - Solved by just... recording commercial-free mixes. There doesn't appear to be an obvious off-the-shelf "remove commercials from an audio stream" solution like there is for web ad blocking or text-to-speech

# API Query

Returns a big ass XML document... I'm guessing this lists the open servers

```
https://playerservices.streamtheworld.com/api/livestream?station=WQHTFM&transports=http%2Chls%2Chlsts&version=1.9&request.preventCache=1663430139639
```

There are three different mount points... let's see how the media-format differs...

```xml
<!-- This one looks to be mono MP3, low bitrate. Don't want -->
<media-format container="flv" cuepoints="stwcue" trackScheme="audio">
    <audio index="0" samplerate="22050" codec="mp3" bitrate="32000" channels="1" />
</media-format>
<!-- This is the one Firefox grabbed for me -->
<media-format container="flv" cuepoints="stwcue" trackScheme="audio">
    <audio index="0" samplerate="44100" codec="heaacv2" bitrate="32000" channels="2" />
</media-format>
<!-- Not sure how this one differs from above? -->
<media-format container="flv" cuepoints="stwcue" trackScheme="audio">
    <audio index="0" samplerate="44100" codec="heaacv2" bitrate="32000" channels="2" />
</media-format>
```

Xpath in words:
1. Get the `mountpoint` by finding the parent, parent node of an `audio` node with `samplerate=44100`
2. Find all `ip.text` within said mount point

```python
xmlns = {'ns': 'http://provisioning.streamtheworld.com/player/livestream-1.9'}
hq_mountpoint = root.find(".//*[@samplerate='44100']/../..")
urls = [
  node.text for node in hq_mountpoint.findall(".//ns:ip", xmlns)
]
```

From some playing with cURL, it looks like all of the servers on "mountpoint 2" return
the same stream. So now it's time to do my favorite thing in the world... XML parsing \s.

OK, not too bad, thankfully. Also looks like I don't need to worry about `request.preventCache` param...

# The request itself

```
https://24283.live.streamtheworld.com/WQHTFMAAC.aac?dist=triton-widget&tdsdk=js-2.9&swm=false&pname=tdwidgets&pversion=2.9&banners=728x90%2C300x250&burst-time=15&sbmid=96cf8196-acd8-4f4e-941c-c88c7297fbeb
```

Broken out:

```
Host:   24283.live.streamtheworld.com
Path:   /WQHTFMAAC.aac # WQHT is HOT 97.1 callsign
Query Params:
              dist: triton-widget
             tdsdk: js-2.9
               swm: false
             pname: tdwidgets
          pversion: 2.9
           banners: 728x90,300x250
        burst-time: 15
             sbmid: 96cf8196-acd8-4f4e-941c-c88c7297fbeb
```

# Thoughts

I'm 99% certain I can pull the host from the API XML document

Things that may make this effort more complicated:
  * If cookies/sessions are required (e.g. must run some javascript on the page)
  * If the `smbid` thing is actually mandatory (would have to figure out where it's generated)

Well just did a quick `curl https://24283.live.streamtheworld.com/WQHTFMAAC.aac`, and I got a completely successful response.

So it looks like it's not really going to be a problem at all to set up the connection,
the challenge will just be the process of tagging the files (and, ideally, removing commercials)
