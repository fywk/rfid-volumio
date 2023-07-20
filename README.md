# RFID Volumio

This application allows you to control [Volumio](https://volumio.com/en/) on Raspberry Pi using RFID tags. This is useful for having physical control when running Volumio [headlessly](https://en.wikipedia.org/wiki/Headless_computer).

You can assign several tags for basic playback controls such as _play_, _pause_, _stop_, _previous_ and _next_ in the `.env` file. For music playing, the app utilises Volumio's [replaceAndPlay](https://volumio.github.io/docs/API/REST_API.html#page_ADDING_ITEMS_TO_PLAYBACK) API to clear the content of the playback queue and play a new item when you scan a corresponding tag.

You can play from any sources that are supported by Volumio, such as Spotify, Music Library, Web Radio and many more, as long as a minimum of [valid URI](#valid-playback-uris) is provided. The RFID tag IDs and corresponding data are stored in a CSV file.

## Prerequisite

This repo assumes you already have Volumio OS installed on your Raspberry Pi and that you want to use the same Pi to scan RFID tags and play music.

You also have the following components ready:

- RFID RC522 Module
- RFID Cards/Fobs/Stickers (13.56 MHz)

### Connect the RFID Module to the Raspberry Pi

Follow this [section](https://pimylifeup.com/raspberry-pi-rfid-rc522/#wiring-the-rfid-rc522) of the tutorial by PiMyLifeUp to learn how to wire up the RFID module with your Pi.

## Installation

1. Activate the SPI interface.

   - Open the user's boot configuration file.

     ```bash
     nano /boot/userconfig.txt
     ```

   - Add the following line within the file:

     ```
     dtparam=spi=on
     ```

   - Save the changes to the configuration file. Then reboot the device.

     ```bash
     sudo reboot
     ```

   - Once rebooted, check if SPI has been successfully enabled by executing the following command:

     ```bash
      lsmod | grep spi
     ```

   - If **spi_bcm2835** is listed on the output, that means the SPI interface on your Raspberry Pi has been activated.

2. Install `python-dotenv`, `spidev` and `mfrc522` Python modules.

   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip
   sudo pip3 install python-dotenv spidev mfrc522
   ```

3. Run the `read.py` utility to get the ID of your RFID tag.

   ```bash
   cd rfid-volumio
   python3 utils/read.py
   ```

4. Create a `.env` file similar to [`.env.example`](https://github.com/fywk/rfid-volumio/blob/main/.env.example) and add RFID tag IDs for playback controls.

5. Create a CSV file named `playback.csv` that contains all the records of media you would like to play in the following format:

   ```csv
   ID,Service,URI,Name,Type
   000000000000,spop,spotify:playlist:37i9dQZF1DXcBWIGoYBM5M,Today's Top Hits,Playlist
   000000000000,webradio,http://stream.live.vc.bbcmedia.co.uk/bbc_radio_two,BBC Radio Two,Web Radio
   ```

   | :bulb: | You can use spreadsheet software like Google Sheets to maintain all your records and export them as CSV file. |
   | ------ | :------------------------------------------------------------------------------------------------------------ |

6. Run `main.py` to test if everything is working properly. You should hear music start playing when you scan a tag with a matching ID in `playback.csv`.

   ```bash
   python3 main.py
   ```

7. Change access permissions of `main.py` to become executable.

   ```bash
   chmod +x main.py
   ```

8. Copy the `rfid.service` file to `/etc/systemd/system/rfid.service` and enable the service to allow the main script run automatically at boot time and continuously in the background.

   ```bash
   sudo cp -v rfid.service /etc/systemd/system/rfid.service
   sudo systemctl enable rfid.service
   ```

   | :bulb: | Outputs from the script can be viewed by running `journalctl -f -u rfid.service` once the script is started automatically at boot time. |
   | ------ | --------------------------------------------------------------------------------------------------------------------------------------- |

## Valid Playback URIs

You can play music with a URI from your local Music Library and Web Radio without installing any additional plugins. If you want to play music from other sources, like Spotify, you must install the appropriate plugins.

Some examples of playback URIs that Volumio supports that can be inserted into `playback.csv` file:

| Service  | URI                                         | Notes                   |
| -------- | ------------------------------------------- | ----------------------- |
| mpd      | albums://C418/2%20years%20of%20failure      | -                       |
| spop     | spotify:track:4cOdK2wGLETKBW3PvgPWqT        | Require Spotify plugin. |
| webradio | https://somafm.com/nossl/groovesalad256.pls | -                       |

## Acknowledgements

Thanks to the [pimylifeup/MFRC522-python](https://github.com/pimylifeup/MFRC522-python) library for enabling the reading of RFID tags via the RC522 RFID module used in this project.

Also thanks to these projects that have inspired me on this project:

- [tinkerthon/volumio-rfid](https://github.com/tinkerthon/volumio-rfid)
- [talaexe/Spotify-RFID-Record-Player](https://github.com/talaexe/Spotify-RFID-Record-Player)
- [yuergen/phoniebox](https://github.com/yuergen/phoniebox)
