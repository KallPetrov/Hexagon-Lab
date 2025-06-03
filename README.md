# Hexagon-Lab
Hexagon-Lab Project
You must cite https://hexagon-lab.com as the source of the original application code, regardless of whether you have made changes or not.
````markdown
# TMX to JSON Converter - by HEXAGON-Lab

A graphical tool for converting translation data from TMX (Translation Memory eXchange) files into JSON format. Built using Python's `tkinter` library.

## 📦 Features

- Load a `.tmx` file for processing.
- Automatically detect available languages in the file(s).
- Select source and target languages from dropdown menus.
- Preview translation pairs (source → target).
- Limit the number of displayed translation pairs.
- Export translation pairs to a formatted `.json` file.

## 🖥️ GUI Overview

- **Upload File** – Choose a TMX file to load.
- **Source/Target Language** – Select the languages to extract translation pairs.
- **Number of Rows to Visualize** – Set how many rows to display in the preview.
- **Export to JSON** – Save the extracted translation pairs to a JSON file.

## 🧪 Output Format

Exported JSON file structure:
```json
[
  {
    "source": "Hello",
    "target": "Bonjour"
  },
  {
    "source": "Goodbye",
    "target": "Au revoir"
  }
]
````

## 🚀 Getting Started

1. Make sure you have Python 3 installed.
2. Save the script as `TMXtoJSON-1.0.py`.
3. Run the application:

   ```bash
   TMXtoJSON-1.0.py
   ```

## ⚠️ Requirements

* Python 3.x
* No external dependencies (uses only standard libraries: `tkinter`, `os`, `json`, `xml`, etc.)

## 📝 Notes

* The tool supports selecting a single `.tmx` file.
* Only language pairs that exist in the TMX entries will be shown/exported.
* Any errors during file parsing will be logged and displayed in the text area.

## 🧑‍💻 Author

Developed by **HEXAGON-Lab**

Version: `1.0`



