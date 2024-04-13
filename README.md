# wireless-deauther
A python script for wireless deauthentication attacks with target management.

### Disclaimer
This script is not intended for unauthorized use on public Wi-Fi networks. 
It is capable of malicious activity and is intended solely for educational purposes or for use with explicit permission from network owners.<br>
I am not responsible for any actions taken with this script. Usage is at your own discretion and responsibility.<br>

## A Brief Explanation
Goal of this script is target management while deauthanticating a wireless network.
It should provide the functionality to target specific devices or exclude certain ones, as well as the option to target all devices on the same network.

## Prerequisites
### A linux based operating system
This script is made for Linux machines. It uses Linux system calls, commands and utilities; it is not intended to work on other operating systems.<br>
Even though I'm testing this script on Kali Linux, any major Linux distribution shall work fine with needed tools installed.

### Having a wifi interface that is capable of packet injection/monitor mode
This script utilizes packet injection on routers for deauthentication attacks. Make sure your wireless card or wireless adapter is capable of Monitor mode.

### Network and Wireless tools
You should be able to run these two commands without errors:<br>
```ifconfig```<br>
```iwconfig```<br>

If you're unable to run these commands you don't have these packages installed on your system.<br>
Installation is simple:<br>
- On Debian/Ubuntu/Kali
```sudo apt install net-tools wireless-tools```
- On Arch Linux
```sudo pacman -S net-tools wireless-tools```
- On Fedora
```sudo dnf install net-tools wireless-tools```

### Python3 and Pandas
Make sure you have python and it's pandas library installed on your system.<br>
If you dont have them, install like this:<br>
- On Debian/Ubuntu/Kali
```sudo apt install python3 python3-pandas```
- On Arch Linux
```sudo pacman -S python python-pandas```
- On Fedora
```sudo dnf install python3 python3-pandas```

## Testing
The testing is done on a Kali Linux virtual machine. It is ready out of the box to run this script, without needing any external tools installed.

## TODO
- [x] Check if script is ran as root and with requested arguments
- [x] Set the wireless interface to monitor mode if it isn't in monitor mode
- [x] Scan nearby networks with airodump-ng and wait for a keyboard interrupt (CTRL+C)
- [x] Store the data to a temporary csv file to read it with pandas
- [x] Print found networks to the user and ask the user to select a network
- [x] Get the BSSID and Channel of the selected network to scan the network
- [ ] Scan the selected network and it's channel with airodump-ng and store targets to a csv file
- [ ] Print found targets and let user manage targets like: everyone except (x,y,z), only x, targets (x,y,z), everyone
- [ ] Deauthenticate targets until given time or keyboard interrupt
- [ ] Set the wireless interface to it's default (managed mode)
- [ ] Exit
