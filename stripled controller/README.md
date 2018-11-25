This a game where a raspberry will listen to udp packages and light a ledstrip of neopixels.

It will listen for:
- "(0)" to reset the game
- "(1)" player 1 moves
- "(2)" player 2 moves

To install the libraries in a raspberry pi from zero you need to follow this procedure:
1. Install last version of raspbian
2. Issue a `sudo apt-get update && sudo apt-get upgrade`
3. Install git 
4. Clone the neopixel driver repository : `https://github.com/jgarff/rpi_ws281x` and follow the install instruction and those of python wrapper.
5. Connect GND and GPIO18 to the GND and data input of the ledstrip.
6. Run the game !
```
sudo python androidgame.py
````
