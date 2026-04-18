import json
import os
import random
import shutil
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import qrcode
import requests
import spotipy
import typst
from spotipy import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import qrcode.image.svg
import logging
import calendar

logging.basicConfig(level=logging.INFO)
random.seed("hitster")


def get_env_var(key):
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Environment variable {key} is required but not set.")
    return value


def get_env_var_optional(key):
    return os.getenv(key)


def create_spotify_client():
    auth_mode = get_env_var_optional("SPOTIFY_AUTH_MODE") or "client_credentials"

    if auth_mode == "user":
        # User auth can access private/collaborative playlists.
        client_id = get_env_var("CLIENT_ID")
        client_secret = get_env_var("CLIENT_SECRET")
        redirect_uri = get_env_var("SPOTIFY_REDIRECT_URI")
        scope = (
            get_env_var_optional("SPOTIFY_SCOPE")
            or "playlist-read-private playlist-read-collaborative"
        )

        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
                cache_path=".spotify_token_cache",
                open_browser=True,
            )
        )

    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=get_env_var("CLIENT_ID"),
            client_secret=get_env_var("CLIENT_SECRET"),
        )
    )


def resolve_date(date_str):
    date_parts = date_str.split("-")[::-1]
    parts = [""] * (3 - len(date_parts)) + date_parts

    day = f"{int(parts[0])}." if parts[0] else ""
    month = calendar.month_name[int(parts[1])] if parts[1] else ""
    year = parts[2]

    return day, month, year


def get_playlist_songs(sp, playlist_id):
    songs = []
    next_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/items?limit=100&additional_types=track"

    while next_url:
        token = sp.auth_manager.get_access_token(as_dict=False)
        response = requests.get(
            next_url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        response.raise_for_status()
        results = response.json()

        for item in results.get("items", []):
            track = item.get("track") or item.get("item")
            if track and track.get("type") == "track":
                day, month, year = resolve_date(track["album"]["release_date"])
                songs.append(
                    {
                        "name": track["name"],
                        "artists": [artist["name"] for artist in track["artists"]],
                        "day": day,
                        "month": month,
                        "year": year,
                        "release_date": track["album"]["release_date"],
                        "url": track["external_urls"]["spotify"],
                        "id": track["id"],
                    }
                )

        next_url = results.get("next")

    random.shuffle(songs)
    return songs


def generate_qr_codes(songs):
    if os.path.isdir("qr_codes"):
        shutil.rmtree("qr_codes")
    os.mkdir("qr_codes")

    for song in songs:
        img = qrcode.make(song["url"], image_factory=qrcode.image.svg.SvgPathImage)
        img.save(f"qr_codes/{song["id"]}.svg")


def generate_overview_pdf(songs, output_pdf):
    year_counts = Counter(int(song["year"]) for song in songs if "year" in song)

    min_year = min(year_counts.keys())
    max_year = max(year_counts.keys())
    all_years = list(range(min_year, max_year + 1))
    counts = [year_counts.get(year, 0) for year in all_years]

    plt.figure()
    plt.bar(all_years, counts, color="black")
    plt.ylabel("number of songs released")
    plt.xticks()

    with PdfPages(output_pdf) as pdf:
        pdf.savefig()
        plt.close()


def main():
    sp = create_spotify_client()

    logging.info("Starting Spotify song retrieval")
    songs = get_playlist_songs(sp, get_env_var("PLAYLIST_ID"))

    logging.info("Writing songs to file")
    with open("songs.json", "w") as file:
        json.dump(songs, file, indent=4)

    logging.info("Generating QR codes")
    generate_qr_codes(songs)

    logging.info("Compiling Cards PDF")
    typst.compile("hitster.typ", output="hitster.pdf")

    logging.info("Compiling Year Overview PDF")
    generate_overview_pdf(songs, "overview.pdf")

    logging.info("Done")


if __name__ == "__main__":
    main()
