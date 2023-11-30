import pandas as pd
from tabulate import tabulate
from tkinter import Tk, filedialog

def markdown_to_excel(markdown_text):
    # Split Markdown text into lines
    lines = markdown_text.split('\n')

    # Identify the lines containing the table
    table_lines = [line for line in lines if '|' in line]

    # Extract headers and data
    headers = table_lines[0].split('|')[1:-1]
    data = [line.split('|')[1:-1] for line in table_lines[2:]]  # Skip the header separator line

    # Create a DataFrame using pandas
    df = pd.DataFrame(data, columns=headers)

    # Save DataFrame to Excel
    excel_file = 'output.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Excel file '{excel_file}' created successfully.")

def choose_markdown_file():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title="Choose a Markdown file", filetypes=[("Markdown files", "*.md")])

    if file_path:
        with open(file_path, 'r') as file:
            markdown_text = file.read()
        markdown_to_excel(markdown_text)
    else:
        print("No file selected. Exiting.")

if __name__ == "__main__":
    choose_markdown_file()
