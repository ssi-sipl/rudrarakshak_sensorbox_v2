import os
import subprocess
import sys

# CONFIGURATION
USER = "rudra"
WORKING_DIR = "/home/rudra/rudrarakshak_sensorbox_v2"
BINARY_NAME = "radar_ultrasonic"
BINARY_PATH = os.path.join(WORKING_DIR, BINARY_NAME)
SERVICE_NAME = "radar.service"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}"
LOG_FILE = os.path.join(WORKING_DIR, "radar.log")

def run_command(command, description):
    try:
        subprocess.run(command, check=True)
        print(f"{description} succeeded.")
    except subprocess.CalledProcessError as e:
        print(f"{description} failed with error: {e}")
        sys.exit(1)

def create_service():
    service_content = f"""[Unit]
Description=Radar-Ultrasonic Server Auto Start
After=network.target

[Service]
User={USER}
WorkingDirectory={WORKING_DIR}
ExecStart={BINARY_PATH} >> {LOG_FILE} 2>&1
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
"""
    print("Creating systemd service...")

    temp_service = "temp_service.service"
    with open(temp_service, "w") as f:
        f.write(service_content)

    run_command(["sudo", "mv", temp_service, SERVICE_PATH], "Moving service file to system directory")
    run_command(["sudo", "chmod", "644", SERVICE_PATH], "Setting permissions on service file")
    run_command(["sudo", "systemctl", "daemon-reload"], "Reloading systemd")
    run_command(["sudo", "systemctl", "enable", SERVICE_NAME], "Enabling service to run at boot")
    run_command(["sudo", "systemctl", "restart", SERVICE_NAME], "Starting service now")

def main():
    if not os.path.isfile(BINARY_PATH):
        print(f"❌ Error: Binary not found at {BINARY_PATH}")
        sys.exit(1)

    create_service()

    print("\n✅ Setup complete. Your binary will now auto-start on reboot.")
    print(f"🚀 Binary path: {BINARY_PATH}")
    print(f"📜 Service file: {SERVICE_PATH}")
    print(f"🪵 Log file: {LOG_FILE}")

if __name__ == "__main__":
    main()
