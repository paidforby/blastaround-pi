# blastaround-pi

an interactive scooter attachment  

### Hardware:  

* Raspberry Pi 3
* Bluetooth Headphones
* USB speaker
* 4 x NeoPixel 24 LED Ring
* Magnetically-operated reed switch
* PIR sensor

### Software:
A pre-built image will be available at [blastaround-pi/releases](github.com/paidforby/blastaround-pi/release)  

To build from source on a Raspberry Pi 3, connect the neccessary hardware and install raspbian-jessie lite. Then follow these instructions,  

```
sudo apt update  
sudo apt install git-core python-pip python-smbus python-pygame scons vlc  
pip install -r requirements.txt 
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


