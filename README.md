# Backlog Tracker 


Backlog Tracker is a simple cross-platform desktop application designed to help students calculate, track, and systematically defeat academic backlogs. Designed with modern CustomTkinter layouts, the app calculates active clearing rates (CPD), provides smart Sunday lookahead ETAs, and visualizes curriculum weight distribution natively.

Key Features

-  Recognizes Sunday rest patterns. Live class growth skips Sundays, while your study clearance (CPD) remains active to clear your backlog faster.

-  Native Analytics: Clean weight distribution bar charts rendered directly on canvas to help you visualize which subjects need immediate priority.

- Quick Configuration

- Motivational Qoutes


## Installation & Downloads

To run the pre-compiled installer instantly on your PC (Built by github actions) , click the Download below, or head directly to the [Releases](https://github.com/debojitsantra/BacklogTracker/releases/) section of this repository and download the appropriate bundle:

Windows: [Download (BacklogTracker_Setup.exe)](https://github.com/debojitsantra/BacklogTracker/releases/download/v1.1.0/BacklogTracker_Setup.exe) (run the setup wizard to install desktop/start menu shortcuts).

Linux: [Download BacklogTracker_Linux.tar.gz](https://github.com/debojitsantra/BacklogTracker/releases/download/v1.1.0/BacklogTracker_Linux.tar.gz) (extract and run portable binary).

macOS: [Download BacklogTracker_macOS.zip](https://github.com/debojitsantra/BacklogTracker/releases/download/v1.1.0/BacklogTracker_macOS.zip) (unzip and run the standard App bundle).

## Local Development & Build

If you want to run or build the application from source code:




### Prerequisites

Make sure you have Python 3.10+ installed along with the required libraries:

```bash
pip install customtkinter pillow pyinstaller
```

Running Locally
```python
python backlog_tracker.py
```

### Packaging Locally

To bundle into a single standalone executable locally:

```python
pyinstaller --noconfirm --onefile --windowed --add-data "icon.ico;." --icon=icon.ico --name "BacklogTracker" backlog_tracker.py
```

### Releases (CI/CD)

Releases are built automatically via GitHub Actions on every version tag push:

```bash
git tag v1.0.1
git push origin v1.0.1
```

This triggers automated Windows (.exe) and Linux binary builds, published to GitHub Releases.
