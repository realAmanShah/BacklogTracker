<p align="center">
  <img src="assets/banner.png" width="100%" alt="Backlog Tracker Banner" />
</p>

<p align="center">
  <img src="assets/icon_300.png"  width=72 alt="Backlog Tracker Icon" />
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
## Screenshots
<p align="center">
  <img src="assets/1.png" width="100%" alt="Screenshot 1" />
    <img src="assets/2.png" width="100%" alt="Screenshot 2" />
</p>

## Installation

Android Version Code Here: [Android](https://github.com/debojitsantra/BacklogTracker-Android/)

Download the latest release for your platform:

| Platform | Download |
|----------|----------|
| Windows  | [BacklogTracker_Setup.exe](https://github.com/debojitsantra/BacklogTracker/releases/) |
| Linux    | [BacklogTracker_Linux.tar.gz](https://github.com/debojitsantra/BacklogTracker/releases/) |
| macOS    | [BacklogTracker_macOS.zip](https://github.com/debojitsantra/BacklogTracker/releases/) *(untested)* |
| Android | [BacklogTracker-{tag}.apk](https://github.com/debojitsantra/BacklogTracker-Android/releases)|
| Web Version *(unstable)*| [backlogtracker.debojitworkers.qzz.io](https://backlogtracker.debojitworkers.qzz.io/)|

All releases: [github.com/debojitsantra/BacklogTracker/releases](https://github.com/debojitsantra/BacklogTracker/releases/)

<a href="https://apps.microsoft.com/detail/9p112ngslvf0?referrer=appbadge&mode=full" target="_blank"  rel="noopener noreferrer">
	<img src="https://get.microsoft.com/images/en-us%20dark.svg" width="200"/>
</a>

### Linux — Emoji Support

If emojis appear as blank squares, install the Noto Color Emoji font:

```bash
sudo apt install fonts-noto-color-emoji -y
```

> Required on Ubuntu/Debian-based distros. Not needed on most modern distros that ship with it by default.

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


  ##  You can help me by Donating
[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/debojitsantra) 
[![Donate using Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/debojitsantra/donate)
<a href="https://chai4.me/debojitsantra" target="_blank" title="Support debojitsantra on Chai4Me" style="display:inline-flex;flex-direction:column;align-items:center;justify-content:center;background:#ffffff;padding:8px 32px;border-radius:16px;text-decoration:none;border:1px solid #e5e7eb;box-shadow:0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05);transition:transform 0.2s;"><img src="https://chai4.me/icons/wordmark.png" alt="Chai4Me" style="height:32px;object-fit:contain;"/></a>
