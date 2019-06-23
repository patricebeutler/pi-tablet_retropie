#!/bin/sh

# apt-get update
sudo apt-get update

# Install screen
sudo apt-get install -y screen 

# Permissions 
sudo chmod -R 755 /home/pi/pi-tablet_retropie/assets/*
sudo chown pi:pi /home/pi/pi-tablet_retropie
sudo chown pi:pi /home/pi/pi-tablet_retropie/*

# boot-config
sudo sh -c "echo 'avoid_warnings=1' >> /boot/config.txt"
sudo sh -c "echo 'disable_splash=1' >> /boot/config.txt"
sudo sh -c "echo 'dwc_otg.lpm_enable=0 console=serial0,115200 console=tty3 root=PARTUUID=f2d3cb4f-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait loglevel=3 consoleblank=0 plymouth.enable=0 quiet splash loglevel=3 logo.nologo vt.global_cursor_default=0' > /boot/cmdline.txt"
sudo sed -i 's/tty1/tty3/g' /boot/cmdline.txt

echo "gpu_mem=128
audio_pwm_mode=2
display_default_lcd=1" | sudo tee -a /boot/config.txt

sudo touch /home/pi/.hushlogin

cd /home/pi/pi-tablet_retropie/assets/
sudo mv "/home/pi/pi-tablet_retropie/assets/autologin@.service" "/etc/systemd/system/autologin@.service"
sudo mv "/home/pi/pi-tablet_retropie/assets/autostart.sh" "/opt/retropie/configs/all/autostart.sh"
sudo chmod 644 /opt/retropie/configs/all/autostart.sh

# Screens (additional functionality)
cd /home/pi/pi-tablet_retropie/assets/
sudo mv 00-startup.sh /etc/init.d/00-startup.sh
sudo mv 01-screenHandlerDisplayModeRunner.sh /etc/init.d/01-screenHandlerDisplayModeRunner.sh
sudo mv 02-screenHandlerPowerStateOnIndicatorRunner.sh /etc/init.d/02-screenHandlerPowerStateOnIndicatorRunner.sh
sudo mv 03-screenHandlerShutdownListenerRunner.sh /etc/init.d/03-screenHandlerShutdownListenerRunner.sh
sudo mv 04-screenHandlerTouchRunner.sh /etc/init.d/04-screenHandlerTouchRunner.sh
sudo update-rc.d 00-startup.sh defaults
sudo update-rc.d 01-screenHandlerDisplayModeRunner.sh defaults
sudo update-rc.d 02-screenHandlerPowerStateOnIndicatorRunner.sh defaults
sudo update-rc.d 03-screenHandlerShutdownListenerRunner.sh defaults
sudo update-rc.d 04-screenHandlerTouchRunner.sh defaults

# Python
sudo apt-get install -y python-setuptools python-dev
sudo apt-get install -y python3 python3-pip
sudo easy_install rpi.gpio
cd github-repos/pimoroni/python-multitouch/python-multitouch-master/library
sudo python3 setup.py install
sudo pip3 install python-uinput pyudev rpi_backlight

# Reboot
sudo reboot
