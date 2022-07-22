# RFID Volumio

Control Volumio via RFID on Raspberry Pi. You can play from any sources supported by Volumio as long as you provide a valid URI. The RFID tag IDs and corresponding URIs are stored and read from the CSV file.

## Prerequisite

This repo assumed you already have Volumio installed on your Raspberry Pi and that the same Raspberry Pi is used for both scanning of RFID and media playing.

You also have the necessary components listed below:

- RFID RC522 Module
- RFID Stickers/Cards/Tokens (13.56 MHz)

## Installation

- Ensure the SPI interface is activated, by adding the following line to `/boot/userconfig.txt`.

```
dtparam=spi=on
```

- Ensure that both `spidev` and `mfrc522` Python modules are installed.

```bash
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install spidev
sudo pip3 install mfrc522
```

- Enter your records into the `playback.csv` file. You may remove the sample records.

- Copy the `rfid.service` file to `/etc/systemd/system/rfid.service` to continuously runs at boot time and keeps on running in the background.

## Example Playback URIs

Some example URIs that Volumio supports that can be inserted into CSV file:

**Spotify**

| Type     | Service | URI                                     |
| -------- | ------- | --------------------------------------- |
| Album    | spot    | spotify:album:1bx7sNUpVB9fQ7QhcVZsUV    |
| Playlist | spot    | spotify:playlist:37i9dQZEVXbMDoHDwVN2tF |
| Track    | spot    | spotify:track:4cOdK2wGLETKBW3PvgPWqT    |

**Web Radio**

| Name                   | Service  | URI                                                |
| ---------------------- | -------- | -------------------------------------------------- |
| BBC Radio One          | webradio | http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one |
| Radio Paradise (FLAC+) | webradio | http://stream.radioparadise.com/flacm              |

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
