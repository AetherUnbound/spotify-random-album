# Spotify Random Album Picker

## Cross-platform app

**This cross-platform app was generated by** [`Briefcase`](https://github.com/beeware/briefcase) **- part of**
[`The BeeWare Project`](https://beeware.org/). **If you want to see more tools like Briefcase, please
consider** [`becoming a financial member of BeeWare`](https://beeware.org/contributing/membership).

A small app which chooses a random album to play from your liked album library.

For conda on linux, you may need to run:
```bash
conda install -c conda-forge gtk3 pygobject
```

### How to build and run

1. Populate the `.env` file
2. Plug in an Android phone with debugging enabled
3. Set Android USB to "File Transfer"
4. Run the app locally once (via `briefcase dev`) so it generates a `.cache-spotipy` or `cache-spotipy.py` file
5. Run `briefcase create android`
6. Run `briefcase build android -u`
7. Run `briefcase run android`

## Original script

The original script ([spotify-random.py](./spotify-random.py)) can be run in an environment with spotipy installed.
It also needs the following environment variables in order to run:

```dotenv
SPOTIPY_REDIRECT_URI=http://127.0.0.1:9090
SPOTIPY_CLIENT_ID=[redacted]
SPOTIPY_CLIENT_SECRET=[redacted]
```
