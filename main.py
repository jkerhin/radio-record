"""Record a live radio stream to file

TODO: Handle ctrl+c even inside the thread
"""
import datetime
import logging
import threading
import time
from pathlib import Path
from typing import List
from xml.etree import ElementTree

import click
import requests
from dateutil.parser import parse as dparse

API_URL = "https://playerservices.streamtheworld.com/api/livestream"


logging.basicConfig(
    level="INFO",
    format="%(asctime)s [%(name)s]: [%(levelname)s]: %(message)s",
)


@click.command()
@click.option(
    "--duration",
    default="10 minutes",
    show_default=True,
)
@click.argument("station", nargs=1, default="WQHTFM")
def main(station, duration):

    dur = parse_duration(duration)
    logging.debug(f"{duration} parsed as {dur}")

    params = {
        "station": station,
        "transports": "http,hls,hlsts",
        "version": "1.9",
    }

    logging.info("Fetching hosts")
    r = requests.get(API_URL, params=params)
    r.raise_for_status()

    hosts = hq_server_hosts(r.content)

    date_str = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    out_pth = Path(f"{date_str}_{station}_{duration}.aac")
    stream_url = f"https://{hosts[0]}/{station}AAC.aac"
    stop_recording = threading.Event()

    logging.info(f"Listening to {station} for {duration}. Will write to {out_pth}")
    download_thread = threading.Thread(
        target=stream_to_file,
        args=(stream_url, out_pth),
        kwargs={"event": stop_recording},
    )

    # TODO - need to handle SIGINT, etc.
    download_thread.start()
    time.sleep(dur.total_seconds())
    stop_recording.set()
    download_thread.join()

    logging.info("Recording complete")


def parse_duration(duration_str: str) -> datetime.timedelta:
    """Turn a human duration string (e.g. '4 hours') into a timedelta

    TODO: Surely there is a better way to do this? In pandas it would be
    `to_timedelta()`, but pandas is way overkill for this project

    """
    midnight = dparse("00:00:00")
    return dparse(duration_str) - midnight


def stream_to_file(url: str, out_pth: Path, event: threading.Event = None):
    """Iteritavely write the bytes returned by a URL to a file"""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with out_pth.open("wb") as file_hdl:
            for chunk in r.iter_content(chunk_size=8192):
                file_hdl.write(chunk)
                if event.is_set():
                    return


def hq_server_hosts(document: str) -> List[str]:
    """Extract the URLs for the 44100 Hz streaming servers"""
    xmlns = {"ns": "http://provisioning.streamtheworld.com/player/livestream-1.9"}

    root = ElementTree.fromstring(document)

    # Find the `mountpoint` node with an `audio` tag at 44 KHz
    hq_mountpoint = root.find(".//*[@samplerate='44100']/../..")

    # The text for each `ip` node has the full server hostname
    return [node.text for node in hq_mountpoint.findall(".//ns:ip", xmlns)]


if __name__ == "__main__":
    main()
