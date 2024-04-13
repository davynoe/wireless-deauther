# wireless-deauther
A python script for wireless deauthentication attacks with target management.

## A Brief Explanation
Goal of this script is target management while attacking a wireless network.
Being able to attack spesific targets or attack every other target excluding spesific targets with also having option to attack every target.

## Prerequisites
- ### A linux based operating system
This script is written for Linux machines. The script uses Linux system calls, commands and utilities.<br>
I am testing this script on Kali Linux, it is ready out of the box to run this script. But any major Linux distribution shall work fine with needed tools installed.

- ### Having a wifi interface that is capable of packet injection/monitor mode
This script utilizes packet injection on routers for deauthentication attacks. Make sure your wireless card or wireless adapter is capable of Monitor mode.

- ### Python3 and Pandas
Make sure you have python and it's pandas library
```sudo apt install python3 python3-pandas```

## Testing
The testing is done on a Kali Linux virtual machine. 
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
