#!/usr/bin/python3
import sys
import os
import pandas as pd
import subprocess

def initial_check():
    if os.geteuid() != 0:
        print("Run as root.")
        sys.exit(1)

    arg_count = len(sys.argv)
    if arg_count != 2:
        err_text = "No interface given!" if arg_count < 2 else "Too many arguments!"
        print(err_text+"\nUsage: deauther.py <interface>")
        sys.exit(1)

def set_monitor():
    result = subprocess.run(["iwconfig", sys.argv[1]], capture_output=True, text=True)
    if result.returncode != 0:
        if "no wireless extensions" in result.stderr:
            print(f"{sys.argv[1]} is not a wireless interface.")
        else:
            print("Error:", result.stderr)
        sys.exit(1)

    mode = None
    for line in result.stdout.splitlines():
        if "Mode:" in line:
            mode = line.split(":")[1].split()[0]
            break
    if mode == "Monitor":
        return
    elif mode == "Managed":
        subprocess.run(["ifconfig", sys.argv[1], "down"])
        subprocess.run(["iwconfig", sys.argv[1], "mode", "monitor"])
        subprocess.run(["ifconfig", sys.argv[1], "up"])
    else:
        print("Unknown mode error:", mode)
        sys.exit(1)

def scan_networks():
    try:
        result = subprocess.run(["airodump-ng", sys.argv[1], "-w", "output", "--output-format", "csv"])
        if result.returncode != 0:
            print("Error:", result.stderr)
            sys.exit(1)
    except KeyboardInterrupt:
        os.system("clear")
        print("Scan complete. Cleaning up.")

    with open("output-01.csv", "r") as file:
        for idx, line in enumerate(file):
            if line.startswith("Station MAC"):
                start_row_station = idx
                break

    df_wifi = pd.read_csv("output-01.csv", nrows=start_row_station, skipinitialspace=True)
    # df_station = pd.read_csv("output-01.csv", skiprows=start_row_station, skipinitialspace=True)
    os.remove("output-01.csv")
    df_wifi_filtered = df_wifi.dropna(subset=["BSSID", "ESSID"])
    return df_wifi_filtered

def select_network(df):
    print(f'ID - {"BSSID".ljust(17)} - {"ESSID".ljust(20)}', end="\t\t")
    print(f'ID - {"BSSID".ljust(17)} - {"ESSID".ljust(20)}')
    print("="*100)
    
    half_len = len(df) // 2
    for i in range(half_len + len(df) % 2):
        bssid1 = str(df.iloc[i]["BSSID"])
        essid1 = str(df.iloc[i]["ESSID"])
        
        bssid2 = str(df.iloc[i + half_len]["BSSID"]) if i + half_len < len(df) else ""
        essid2 = str(df.iloc[i + half_len]["ESSID"]) if i + half_len < len(df) else ""
        
        print(f'{str(i).ljust(2)} - {bssid1.ljust(17)} - {essid1.ljust(20)}', end='')
        if i + half_len < len(df):
            print('\t\t', end='')
            print(f'{str(i + half_len).ljust(2)} - {bssid2.ljust(17)} - {essid2.ljust(20)}')
        else:
            print()
    print("="*100)
    
    id = int(input("Select a network by ID:"))
    target_bssid = df.iloc[id].BSSID
    return target_bssid

if __name__ == "__main__":
    initial_check()
    set_monitor()
    df_wifi = scan_networks()
    target_bssid = select_network(df_wifi)
    print(target_bssid)