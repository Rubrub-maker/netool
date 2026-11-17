# DASH — Network Technician Tool

A Python network dashboard for computer technicians, usable **in the terminal** (CLI) or via a **graphical interface** (Tkinter, dark theme).

```
╔══════════════════════════════════════════╗
║  ██████╗  █████╗ ███████╗██╗  ██╗        ║
║  ██╔══██╗██╔══██╗██╔════╝██║  ██║        ║
║  ██║  ██║███████║███████╗███████║        ║
║  ██║  ██║██╔══██║╚════██║██╔══██║        ║
║  ██████╔╝██║  ██║███████║██║  ██║        ║
║  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝        ║
║         Network Technician Tool          ║
╚══════════════════════════════════════════╝
``

## Features

| Tool | Description |
|----------------------
| **Ping** | Tests connectivity to an IP (4 packets) |
| **Port Scan** | Searches for open ports on a given range |
| **Traceroute** | Shows the path taken by packets to the target |
| **DNS Lookup** | Translates a domain name into an IP address |
| **IP Info** | Country, city, and IP provider (via [ip-api.com](https://ip-api.com)) |
| **Speed / Latency** | Measures latency to Google, Cloudflare, and OpenDNS, and detects a network down |
| **Local scan** | Finds devices that are responding on a local network (e.g., `192.168.1.x`) |
| **Logs** | Timestamped history of all actions in `historique.txt` |

The IP addresses entered are validated before each test (4 numbers between 0 and 255).

## Installation

**Prerequisites:** Python 3.9 or later.

``bash
git clone https://github.com/rubrub-maker/netool.git
cd netool
pip install -r requirements.txt
``

### Tkinter on macOS (Homebrew)

If the graphical window does not open, install the Tkinter module corresponding to your version of Python:

``bash
brew install python-tk@3.11
``

## Usage

### Terminal Mode

``bash
python3 dashboard.py
``

A menu appears: type the number of the desired tool. The **9** option opens the graphical interface.

### Graphics Mode

``bash
python3 dashboard_tk.py
``

Each tool opens in its own window with an input field and a result area. Long operations (scans, traceroute) run in the background without blocking the interface.

### Launch with a system command (optional)

To launch `netool` from anywhere in the terminal:

``bash
sudo cp dashboard.py /usr/local/bin/netool
sudo cp dashboard_tk.py /usr/local/bin/dashboard_tk.py
sudo chmod +x /usr/local/bin/netool
``

Then, just type `netool`.

## Project Structure

``
netool/
├── dashboard.py   # CLI menu and tool functions
├── dashboard_tk.py   # Tkinter GUI
├── requirements.txt   # Python dependencies
└── historique.txt # Created automatically (ignored by Git)
``

## Compatibility

Developed and tested on **macOS**. The `ping` command options differ depending on the system:

- macOS: `-t` for the timeout
- Linux: `-W` for the timeout
- Windows: `-n` instead of `-c` for the number of packages

On Linux or Windows, you will need to adapt these options in the code.

## Warning

The port scan and network scan are to be used **only on your own machines and networks**, or with explicit authorization from their owner. Scanning a network without authorization may be illegal.

## Ideas for Improvement

- Progress bar for scans
- Export results to a file
- Linux and Windows compatibility
- Multi-threaded port scanning for more speed

## Author

Project carried out by **Rubrub-maker** as part of a Python and network training.
