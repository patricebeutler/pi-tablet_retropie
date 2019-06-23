# pi-tablet_retropie
Required ressources to install retropie on the pi-tablet.

## Functions
This repository contains the install-script and all required files to make retropie work perfectly on the pi-tablet.

* Overlay for brightness
* Overlay for volume
* Switch between lcd and hdmi
* Custom splashscreen (clean bootup-look)
* Soft-shutdown by pressing power-button
* Battery-management

## Installation
* Install RetroPie on your SD-card
* Connect a keyboard to your Pi
* Start your Pi
* When prompted by RetroPie to configure the keyboard, press F4 (to get to the console)
* Simply execute the lines below (this will download this repository and do the complete installation).

```
sudo git clone https://github.com/patricebeutler/pi-tablet_retropie.git
sudo bash pi-tablet_retropi/install.sh
```
