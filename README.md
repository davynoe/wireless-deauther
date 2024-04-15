# wireless-deauther
A python script for wireless deauthentication attacks with target management.<br>

### Disclaimer
This script is not intended for unauthorized use on public Wi-Fi networks. 
It is capable of malicious activity and is intended solely for educational purposes or for use with explicit permission from network owners.<br>
I am not responsible for any actions taken with this script. Usage is at your own discretion and responsibility.<br>

## Project Summary
Goal of this script is target management while doing a deauthentication attack on a wireless network.
It should provide the functionality to target specific devices or exclude certain ones, as well as the option to target all devices on the same network.

## Prerequisites
### A linux based operating system
This script is made for Linux machines. It uses Linux system calls, commands and utilities; it is not intended to work on other operating systems.<br>
Even though I'm testing this script on Kali Linux, any major Linux distribution shall work fine with needed tools installed.

### Having a wifi interface that is capable of packet injection/monitor mode
This script utilizes Monitor mode and packet injection on routers for deauthentication attacks. Make sure your wireless card or wireless adapter is capable of Monitor mode.

Run ```iwconfig``` to see if you have a wireless interface.

You can google your wireless device's brand to see if it supports monitor mode.<br>
If a wireless device supports Monitor mode, it is highly likely that it also supports packet injection.

### Network and Wireless tools
You should be able to run these two commands without errors:
```sh
# List network interfaces
ifconfig

# List wireless interfaces
iwconfig
```

If you're unable to run the commands above, install networking tools:
```sh
# On Debian/Ubuntu/Kali
sudo apt install net-tools wireless-tools

# On Arch Linux
sudo pacman -S net-tools wireless-tools

# On Fedora
sudo dnf install net-tools wireless-tools
```

### Python3 and Pandas
Make sure you have python above version 3 and it's pandas library installed on your system.

If you don't have them, install like this:
```sh
# On Debian/Ubuntu/Kali
sudo apt install python3 python3-pandas

# On Arch Linux
sudo pacman -S python python-pandas

# On Fedora
sudo dnf install python3 python3-pandas
```

## Installation and Usage
Make sure you meet the **Prerequisites** before installing.

Clone the repo and cd into it.
```sh
git clone https://github.com/davynoe/wireless-deauther
cd wireless-deauther
```

Mark the script as executable.
```sh
chmod +x deauther.py
```

Run the script as root and with your wireless interface as an argument.
```sh
# Example
sudo ./deauther.py wlan0
```

## Testing
The testing is done in a Kali Linux virtual machine. It is ready out of the box to run this script, without needing any external tools installed.

## TODO
### Main Procedure
- [x] Check if script is ran as root and with requested arguments
- [x] Set the wireless interface to monitor mode if it isn't in monitor mode
- [x] Scan nearby networks with airodump-ng and wait for a keyboard interrupt (CTRL+C)
- [x] Store the data to a CSV file to read it with pandas
- [x] Print found networks to the user and ask the user to select a network
- [x] Get the BSSID and Channel of the selected network to scan the network
- [x] Scan the selected network and it's channel with airodump-ng and store targets to a CSV file
- [x] Print found targets and let user select targets 
- [x] Deauthenticate targets with aireplay-ng until given time or keyboard interrupt
- [x] Set the wireless interface to it's default mode if it was changed
- [x] Exit

### Issues to fix
- [x] Bad presentation and handling of target results lower than 2.
- [x] Record repeating when giving scan results
- [ ] Deauthentication is timeless, no option to add time
- [ ] No menu for reusability of the program
- [ ] Lack of notification at times where keyboard interruption is needed 
