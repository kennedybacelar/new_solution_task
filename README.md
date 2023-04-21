# Project Title

Brief project description.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.

```bash 
pip install -r requirements.txt
``` 

### Usage
The program works dynamically by grabbing every file inside the folder data/input, applying the required transformations, and placing the output files inside the folder data/output.

### Input File Requirements
To run the program, you need to add an Excel-like file with the sheet name of **input_refresh_template** to the data/input folder. Please make sure that the file is well-formatted to avoid errors during the transformation process.

### Running the Program
Once the input file is added, you can run the program using the following command in your terminal:

```bash
python main.py
``` 