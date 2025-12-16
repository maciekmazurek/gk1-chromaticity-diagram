# GK1 Project 3: Chromaticity diagram

Interactive PySide6 application for color science visualization, made for the university's "Computer Graphics 1" classes.

## Features

- Editing a spectral power distribution via a Bézier curve and computing resulting CIE XYZ values
    - Draggable Bézier control points
    - Add/delete via context menu

- Displaying chromaticity on a CIE diagram with spectral locus and sRGB gamut overlays

![Demo](docs/assets/demo.apng)

## Quickstart

### Prerequisites
- Python 3.10+

### Setup & run
Windows

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\src\main.py
```

Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

## Technologies

- Python 3.10.4
- PySide 6.10.1
- NumPy 2.2.6
- SciPy 1.15.3
