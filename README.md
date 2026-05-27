<p align="center">
  <img src="assets/banner.png" width="90%" alt="Backlog Tracker Banner" />
</p>

<p align="center">
  <img src="assets/icon_300.png" width="72" alt="Backlog Tracker Icon" />
</p>

<h1 align="center">Backlog Tracker</h1>

<p align="center">A lightweight cross-platform application that helps students calculate, track, and systematically clear academic backlogs.</p>

---

## Features

- Smart backlog clearance calculations
- CPD (Classes Per Day) tracking
- Sunday-aware ETA prediction
- Native analytics visualization
- Motivational productivity prompts
- Time Simulator ( Fast-forward days, weeks, or months )
---

## Installation

Android Version Code Here: [Android](https://github.com/debojitsantra/BacklogTracker-Android/)

Download the latest release for your platform:

| Platform | Download |
|----------|----------|
| Windows  | [BacklogTracker_Setup.exe](https://github.com/debojitsantra/BacklogTracker/releases/download/v1.0.1/BacklogTracker_Setup.exe) |
| Linux    | [BacklogTracker_Linux.tar.gz](https://github.com/debojitsantra/BacklogTracker/releases/download/v1.0.1/BacklogTracker_Linux.tar.gz) |
| macOS    | [BacklogTracker_macOS.zip](https://github.com/debojitsantra/BacklogTracker/releases/download/v1.0.1/BacklogTracker_macOS.zip) *(untested)* |
| Android | [BacklogTracker-v1.0.1-Debug.apk](https://github.com/debojitsantra/BacklogTracker-Android/releases)|
| Web Version *(unstable)*| [backlogtracker.debojitworkers.qzz.io](https://backlogtracker.debojitworkers.qzz.io/)|

All releases: [github.com/debojitsantra/BacklogTracker/releases](https://github.com/debojitsantra/BacklogTracker/releases/)

<a href="https://apps.microsoft.com/detail/9p112ngslvf0?referrer=appbadge&mode=full" target="_blank"  rel="noopener noreferrer">
	<img src="https://get.microsoft.com/images/en-us%20dark.svg" width="200"/>
</a>


## Local Development

**Install dependencies**
```bash
pip install customtkinter pillow pyinstaller
```

**Run locally**
```bash
python backlog_tracker.py
```

**Build executable**
```bash
pyinstaller --noconfirm --onefile --windowed --add-data "icon.ico;." --icon=icon.ico --name "BacklogTracker" backlog_tracker.py
```

---

## Releases via CI/CD

```bash
git tag v1.0.2
git push origin v1.0.2
```

---

## Author

[github.com/debojitsantra](https://github.com/debojitsantra)
