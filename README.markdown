# Web Browsing Obfuscation Docker Container

This Docker container uses Selenium and ChromeDriver to simulate random web browsing, creating background noise to obfuscate actual browsing activity.

## Prerequisites
- Docker and Docker Compose
- 2GB RAM and 2 CPU cores recommended

## Files
- `requirements.txt`: Python dependencies (`selenium`)
- `Dockerfile`: Builds image with Chromium and ChromeDriver
- `docker-compose.yml`: Configures container service
- `obfuscate_browsing.py`: Script for random browsing
- `websites.txt`: List of URLs to visit
- `randomised-schedule.sh`: Bash script to start/stop the container at random times
- `pull-from-pihole.sh`: Script to fetch DNS queries from Pi-hole for `websites.txt`

## Setup
1. Place all files in a directory.
2. *(Optional)* Edit `websites.txt` with desired URLs.
3. Build and run:
   ```
   docker-compose up --build
   ```
4. Stop:
   ```
   docker-compose down
   ```

## Optional
- **Random Scheduling**:
  - File: `randomised-schedule.sh`
  - Purpose: Starts/stops the container at random times to mimic unpredictable user patterns.
  - Usage:
    ```
    chmod +x randomised-schedule.sh
    ./randomised-schedule.sh
    ```
  - Behaviour: Starts after a random delay (0-5 hours), runs 3-6 cycles of 15-60 min uptime and 5-15 min downtime, stops between 23:00 and 03:00.

- **Pi-hole Integration**:
  - File: `pull-from-pihole.sh`
  - Purpose: Fetches DNS queries from a Pi-hole to populate `websites.txt` with sites you actually visit.
  - Prerequisites: Pi-hole with SSH access and SQLite3 installed.
  - Usage:
    ```
    chmod +x pull-from-pihole.sh
    ./pull-from-pihole.sh
    ```
    Update `<pi_usr>`, `<pi_local_ip>`, and `</path/to>` in the script to match your Pi-hole setup.

## Configuration
- **Concurrency**: Adjust in `obfuscate_browsing.py` (`concurrency=3`).
- **Logging**: Logs saved in `./logs` (max 10MB, 3 files).
- **Network**: Uses `bridge` mode; uncomment `network_mode: container:gluetun` for VPN use.

## Usage
The container runs `obfuscate_browsing.py`, visiting URLs from `websites.txt`, clicking links, and pausing (1-15s). Logs are output to console and `./logs`.

## Troubleshooting
- **Startup Issues**: Verify Docker setup and `chromium`/`chromedriver` compatibility.
- **Website Errors**: Check `websites.txt` for valid URLs; review logs in `./logs`.
- **Resource Usage**: Lower concurrency if performance is impacted.

## Maintenance
- Update `selenium`, `chromium`, and `chromedriver` as needed.
- Clear logs in `./logs` to save space.

## License
Provided as-is, no warranty.