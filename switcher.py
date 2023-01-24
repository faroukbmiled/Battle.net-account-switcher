import os
import json
import psutil
import subprocess

BATTLE_NET = "C:\\Program Files (x86)\\Battle.net\\Battle.net Launcher.exe"

os.chdir(os.path.expandvars(r"%APPDATA%\Battle.net"))
with open("Battle.net.config", "r") as f:
    config = json.load(f)
accounts = config["Client"]["SavedAccountNames"].split(",")

print("Accounts: ")
for i, account in enumerate(accounts):
    print(f"{i+1}. {account}")

while True:
    choice = input("Selection (1-{}): ".format(len(accounts)))
    if not choice.isnumeric() or int(choice) < 1 or int(choice) > len(accounts):
        continue
    break

choice = int(choice) - 1
new_accounts = [accounts[choice]]
for i, account in enumerate(accounts):
    if i == choice:
        continue
    new_accounts.append(account)
config["Client"]["SavedAccountNames"] = ",".join(new_accounts)

if "Battle.net.exe" not in (p.name() for p in psutil.process_iter()):
    print("Battle.net is not running.")
else:
    print("Stopping Battle.net...")
    os.system("taskkill /IM Battle.net.exe /F")

print("Updating configuration file...")

os.system(f"copy Battle.net.config Battle.net.config.switcher-backup")
with open("Battle.net.config", "w") as f:
    json.dump(config, f)

print("Launching Battle.net...")
subprocess.run([BATTLE_NET])
