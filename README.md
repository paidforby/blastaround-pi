# blastaround-pi

an interactive scooter attachment  

### Hardware:  

* Raspberry Pi 3
* 4 x NeoPixel 24 LED Ring
* Magnetically-operated reed switch
* PIR sensor

### Software:
`
To run on Raspberry Pi 3, connect the neccessary hardware and install raspbian-jessie lite. Then follow these instructions,  

```
sudo apt update  
sudo apt install git-core python-pip python-smbus scons vlc  
pip install python-vlc
```

If using NeoPixels via PWM(the default), add the line `blacklist snd_bcm2835` to /etc/modprobe.d/snd-blacklist.conf amd continue with the following steps,
```
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_w281x
scons
cd python
python setup.py
```

Now return to the home directory and,
```
git clone https://github.com/paidforby/blastaround-pi
cd blastaround-pi
sudo python main.py
```


