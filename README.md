# RFID Volumio

Control [Volumio](https://volumio.com/en/) via RFID on Raspberry Pi. You can play from any sources supported by Volumio as long as you provide a valid URI. The RFID tag IDs and corresponding URIs are stored and read from the CSV file.

## Prerequisite

This repo assumed you already have Volumio installed on your Raspberry Pi and that the same Raspberry Pi is used for both scanning of RFID and media playing.

You also have the necessary components listed below:

- RFID RC522 Module
- RFID Stickers/Cards/Tokens (13.56 MHz)

## Installation

1. Ensure the SPI interface is activated, by adding the following line to `/boot/userconfig.txt`.

```
dtparam=spi=on
```

2. Install `python-dotenv`, `spidev` and `mfrc522` Python modules.

```bash
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install python-dotenv spidev mfrc522
```

3. Run the `read.py` utility to get the ID of RFID tags that you've acquired.

```bash
cd rfid-volumio
python3 utils/read.py
```

4. Create a `.env` file similar to [`.env.example`](https://github.com/fywk/rfid-volumio/blob/main/.env.example) and add RFID tag IDs for playback controls.

5. Create a CSV file named `playback.csv` that contains all the records of media you would like to play in the following format:

```csv
ID,Service,URI,Name,Type
000000000000,spot,spotify:playlist:37i9dQZF1DXcBWIGoYBM5M,Today's Top Hits,Playlist
000000000000,webradio,http://stream.live.vc.bbcmedia.co.uk/bbc_radio_two,BBC Radio Two,Web Radio
```

> You can use spreadsheet software like Google Sheets to maintain all your records and export them as CSV file.

6. Run `main.py` to test if everything is working properly. You should hear music start playing when you scan a tag with a matching ID in `playback.csv`.

```bash
python3 main.py
```

7. Copy the `rfid.service` file to `/etc/systemd/system/rfid.service` to have this program start running automatically at boot time and continuously in the background.

> Outputs from the program can be viewed by running `journalctl -f -u rfid.service`, once the program is started automatically at boot time.

## Example Playback URIs

Some example URIs that Volumio supports that can be inserted into CSV file:

**Spotify**

| Type     | Service | URI                                     |
| -------- | ------- | --------------------------------------- |
| Album    | spot    | spotify:album:1bx7sNUpVB9fQ7QhcVZsUV    |
| Playlist | spot    | spotify:playlist:37i9dQZEVXbMDoHDwVN2tF |
| Track    | spot    | spotify:track:4cOdK2wGLETKBW3PvgPWqT    |

**Web Radio**

| Name                   | Service  | URI                                                  |
| ---------------------- | -------- | ---------------------------------------------------- |
| BBC Radio Three        | webradio | http://stream.live.vc.bbcmedia.co.uk/bbc_radio_three |
| Radio Paradise (FLAC+) | webradio | http://stream.radioparadise.com/flacm                |

**Music Library**

| Type  | Service | URI                                    |
| ----- | ------- | -------------------------------------- |
| Album | mpd     | albums://C418/2%20years%20of%20failure |

**And many more...**

Checkout Volumio REST API [documentation](https://volumio.github.io/docs/API/REST_API.htm) for more information.

## Acknowledgements

Special thanks to these projects for inspired me on this project:

- [tinkerthon/volumio-rfid](https://github.com/tinkerthon/volumio-rfid)
- [talaexe/Spotify-RFID-Record-Player](https://github.com/talaexe/Spotify-RFID-Record-Player)
- [yuergen/phoniebox](https://github.com/yuergen/phoniebox)
