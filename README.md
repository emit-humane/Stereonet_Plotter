# Stereonet Plotter

Stereonet Plotter is a small Flask web app for plotting geological lines and planes on a stereonet and exporting the result.

## Features

- Plot **lines** using trend and plunge
- Plot **planes** using strike, dip direction, and dip angle
- Keep a running table of all plotted entries
- Delete individual plotted entries
- Export plots as **PNG**, **PDF**, or **SVG**

## Tech Stack

- Python
- Flask
- Matplotlib
- mplstereonet
- HTML/CSS/JavaScript (jQuery)

## Project Structure

- `./app.py` – Flask app and routes
- `./stereonet_calculations.py` – stereonet plotting logic
- `./templates/index.html` – main UI template
- `./static/css/styles.css` – styles
- `./static/js/script.js` – client-side logic

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install flask matplotlib mplstereonet
   ```

## Run

From the repository root:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## How to Use

1. Choose **Line** or **Plane**.
2. Enter the required values.
3. Click **Add to Plot**.
4. Review entries in the **Current Plots** table.
5. Remove entries with **Delete** if needed.
6. Select an export format and click **Download**.

## Export Formats

- PNG
- PDF
- SVG

## Notes

- Plot data is stored in the Flask session while using the app.
- The app currently runs with `debug=True` in `app.py`; use `debug=False` for production deployments.
