import json
import os
import subprocess

ALERT_FILE = "alerts/dlp_alerts.json"
GPG_PASSWORD = "safe"

def load_alerts():
    with open(ALERT_FILE, "r") as file:
        return json.load(file)

def encrypt_file(file_path):
    encrypted_file = file_path + ".gpg"

    if os.path.exists(encrypted_file):
        print(f"Already encrypted: {encrypted_file}")
        return

    command = [
        "gpg",
        "--batch",
        "--yes",
        "--passphrase",
        GPG_PASSWORD,
        "--symmetric",
        "--cipher-algo",
        "AES256",
        "-o",
        encrypted_file,
        file_path
    ]

    subprocess.run(command, check=True)
    print(f"Encrypted: {file_path} -> {encrypted_file}")

def main():
    alerts = load_alerts()

    sensitive_files = set()

    for alert in alerts:
        if alert.get("severity") in ["medium", "high"]:
            sensitive_files.add(alert["file_path"])

    if not sensitive_files:
        print("No sensitive files found.")
        return

    for file_path in sensitive_files:
        if os.path.exists(file_path):
            encrypt_file(file_path)
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()
