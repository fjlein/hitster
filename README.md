# Hitster Card Generator

This project generates printable [Hitster](https://hitstergame.com) cards from a Spotify playlist. It retrieves song information from Spotify, generates QR codes linking to the songs, and creates a duplex printable PDF with cards using [Typst](https://typst.app).

If you find this DIY Hitster project useful, consider giving it a star :) !

| Page Front | Page Back |
| ------------- | ------------- |
| ![Hitster Front](hitster_front.jpg) | ![Hitster Back](hitster_back.jpg)  |

## ✨ Features

-   Spotify Integration: Fetches song details directly from a Spotify playlist.  
-   QR Code Generation: Creates QR codes for each song, linking to its Spotify URL.  
-   Printable Cards: Generates a PDF with formatted cards, ready for printing.  
-   Configurable Layout: Allows customization of card size and page layout.

## ⚙️ Prerequisites

-   Python ^3.12 
-   Poetry (for dependency management)  
-   Spotify Developer Account (to obtain client credentials)

## 🛠️ Setup

1.  Clone the repository:  
2.  Install dependencies using Poetry:  
    ```bash
    poetry install
    ```  
3.  Set up Spotify API credentials:  
    -   Create a Spotify Developer account and create an app to get your `CLIENT_ID` and `CLIENT_SECRET`.  
    -   Set the following environment variables:  
        ```bash
        export CLIENT_ID="your_client_id"
        export CLIENT_SECRET="your_client_secret"
        export PLAYLIST_ID="your_playlist_id"
        ```
    -   If your playlist is private/collaborative, use user auth mode:
        ```bash
        export SPOTIFY_AUTH_MODE="user"
        export SPOTIFY_REDIRECT_URI="http://127.0.0.1:8888/callback"
        ```
        Then add that redirect URI in your Spotify app settings.

## ▶️ Usage

1.  Run the `main.py` script (put the exports into a .env fie first):  
    ```bash
    source .env && poetry run python main.py
    ```  
2.  Print the `hitster.pdf` file:  
    -   Open the `hitster.pdf` file and duplex print it.  
    -   Cut along the provided markings to create the Hitster cards.

## 🎲 How to Play

1.  Open your camera app and scan the QR code.  
2.  Spotify will launch and the song will start playing.  
3.  After scanning, quickly look away to keep things fair!  
    - Since the song title and artist will be visible, the person scanning should not be the one guessing.  
    - Since the release year might be visible on the cover, the person scanning should scan and look away.  
4.  Have fun!

## 🎨 Customization

-   Card Layout: Modify the `hitster.typ` file to customize the card layout, size, and appearance.  
-   Spotify Playlist: Change the `PLAYLIST_ID` environment variable to use a different Spotify playlist.  
-   Card Dimensions: Change the `card_size`, `rows`, and `cols` variables in `hitster.typ` to adjust the card dimensions and page layout.  
-   Marking Size: Change the `marking_padding` to adjust the space for cutting.

## Troubleshooting

- `403 Forbidden` while reading a playlist usually means your playlist is not publicly accessible to client-credentials auth.
- Fix options:
  - make the playlist public, or
  - use `SPOTIFY_AUTH_MODE="user"` with `SPOTIFY_REDIRECT_URI` and log in once in the browser.
