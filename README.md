# Backlog Tracker

Backlog Tracker is a lightweight cross-platform desktop application designed to help students calculate, track, and systematically clear academic backlogs.

## Features

- Smart backlog clearance calculations
- CPD (Classes Per Day) tracking
- Sunday-aware ETA prediction
- Native analytics visualization
- Motivational productivity prompts

---

## Installation & Downloads

### Releases

https://github.com/debojitsantra/BacklogTracker/releases/

### Windows

https://github.com/debojitsantra/BacklogTracker/releases/download/v1.0.0/BacklogTracker_Setup.exe

### Linux

https://github.com/debojitsantra/BacklogTracker/releases/download/v1.0.0/BacklogTracker_Linux.tar.gz

### macOS (I haven't tested)

https://github.com/debojitsantra/BacklogTracker/releases/download/v1.0.0/BacklogTracker_macOS.zip

---

## Local Development

### Install Dependencies

```bash
pip install customtkinter pillow pyinstaller
```

### Run Locally

```bash
python backlog_tracker.py
```

### Build Executable

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "icon.ico;." --icon=icon.ico --name "BacklogTracker" backlog_tracker.py
```

---

## CI/CD Releases

```bash
git tag v1.0.1
git push origin v1.0.1
```
## Author

https://github.com/debojitsantra
