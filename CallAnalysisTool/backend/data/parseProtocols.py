#!/usr/bin/env python3
"""
Nat 

parseProtocols.py

Reads only the first sheet and only columns A through S (first 19 columns)
from protocolsEMSQA.xlsx, then saves as EMSQA.csv.
"""

import pandas as pd
from pathlib import Path

def main():
    # input protocol questions and output csv
    input_file = Path("protocolsEMSQA.xlsx")
    output_file = Path("EMSQA.csv")

    if not input_file.exists():
        raise FileNotFoundError(f"Input Excel file not found: {input_file}")

    # Reading from filled up rows
    print(f"Reading only first sheet and columns A–S from: {input_file.name}")
    xls = pd.ExcelFile(input_file)
    first_sheet = xls.sheet_names[0]

    # read only first 19 columns (A:S)
    df = pd.read_excel(xls, sheet_name=first_sheet, usecols="A:S")

    # clean up column names
    df.columns = [str(c).strip().replace("\n", " ") for c in df.columns]

    # drop empty rows
    df.dropna(how="all", inplace=True)

    # trimm whitespace
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # save to CSV
    df.to_csv(output_file, index=False)
    print(f"Saved cleaned CSV as: {output_file.name}")

if __name__ == "__main__":
    main()
