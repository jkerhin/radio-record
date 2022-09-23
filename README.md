# Background

My initial goal was to time-shift some radio mixes so I could listen to them without
commercials or signal issues. The idea would be to record a few hours' worth of radio,
cut into smaller chunks, and then burn to CD. I was going to then give the chunks
arbitrary names (like how gfycat generates media URLs) that would be easier to remember
than date strings (if I liked a "chunk")

Ultimately, I went with a solution that required a lot less code, but is also a lot less
generalize. In my (very) limited research, I only found two radio stations that use
the streaming API that I'm consuming from, so I didn't invest in making this more
user-friendly. That being said:

# Install Requirements

This project was developed using [Pipenv](https://pipenv.pypa.io/en/latest/). If you're
already set up with Pipenv, you can set up the project like so:

```bash
pipenv install
```

If you aren't using Pipenv, that's fine, just use venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Usage

As previously mentioned, this is not particularly generalize. I have successfully
tested this with exactly two radio stations (both owned by MediaCo Holding, Inc.):
`WQHT` (Hot 97.1) and `WBLS` (107.5)

With an active environment, simply run:

```bash
python main.py WQHT
```

Radio choices are `WQHT` and `WBLS`. Specify recording time with the `--duration` flag,
and any string that [`pytimeparse`](https://pypi.org/project/pytimeparse) can interpret
as a timedelta.

```
Usage: main.py [OPTIONS] [[WQHT|WBLS]]

Options:
  --duration TEXT  [default: 10 minutes]
  --help           Show this message and exit
```
