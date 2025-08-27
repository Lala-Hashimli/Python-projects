import pdfplumber
import os
import glob
import pandas as pd
import filter_data


pdf_folder = "pdf/"
output_folder = "excel_output/"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))

for pdf_file in pdf_files:
    all_data = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                all_data.extend(table)

    df = pd.DataFrame(all_data[1:], columns=all_data[0])
    df.index += 1

    base_name = os.path.basename(pdf_file).replace(".pdf", ".xlsx")
    excel_path = os.path.join(output_folder, base_name)

    df.to_excel(excel_path, index=True, header=True)

    asking = input("Dou you want to apply filter to excel file?(y/n): ")
    if asking.lower() == "y":
        excel_filename = "filtered_" + base_name
        filtered_excel_path = os.path.join(output_folder, excel_filename)
        filter_data.filter_excel(excel_path, filtered_excel_path)

    print(f"{pdf_file} -> {excel_path} converted")

print("All PDF files changed to Excel files")
