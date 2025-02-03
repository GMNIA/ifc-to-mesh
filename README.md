# IFC to Mesh Converter

## Overview
The **IFC to Mesh Converter** is a command-line tool designed to extract mesh data from **Industry Foundation Classes (IFC)** files and convert them into **MCT format** for use with **Midas software**. It supports extracting geometry from IFC elements and storing them as **OBJ files** before converting them into the **MCT format**.

## Features
- Extracts **3D mesh data** from IFC files.
- Saves extracted geometry as **OBJ files**.
- Converts **OBJ files** into **MCT format** for Midas software.
- Supports **batch processing** of multiple OBJ files.

## Requirements

**Ensure you have the following installed:**
- **Python 3.x**
- `ifcopenshell` library for handling IFC files
- `numpy` for numerical operations

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/ifc-to-mesh.git
   cd ifc-to-mesh
   ```
2. **Install dependencies:**
   ```sh
   pip install ifcopenshell numpy
   ```

## Usage

### 🛠 Extracting Mesh Data from IFC
To extract mesh data from an **IFC file** and save the results as **OBJ files**, use the command:

```sh
python extractmesh.py <path-to-ifc-file> <output-directory>
```

#### Example:
```sh
python extractmesh.py examplestructure_test.ifc midas
```

### Converting OBJ Files to MCT Format
To convert all extracted **OBJ files** in a directory into a single **MCT file**, use:

```sh
python converter_cli.py <output-mct-file>
```

#### Example:
```sh
python converter_cli.py merged_output.mct
```

---

## File Structure
```sh
ifc-to-mesh/
│── extractmesh.py      # Extracts mesh data from IFC to OBJ
│── converter_cli.py    # Converts OBJ files to MCT format
│── midas_converter.py  # Main conversion logic
│── header.mct          # MCT header template
│── between.mct         # MCT intermediate template
│── back.mct            # MCT footer template
│── README.md           # Project documentation
```

## Example Output
After running the **extraction** and **conversion**, the output will include:
- **OBJ files** in the output directory (`midas/`)
- **MCT file** ready for import into **Midas software** (`merged_output.mct`)

## License
This project is licensed under the **MIT License**.

## Author
[Your Name]

## Contributions
Feel free to open **issues** or submit **pull requests** for improvements! 🚀