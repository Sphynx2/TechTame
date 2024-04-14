import pandas as pd
from pathlib import Path

def convert_csv_to_excel(csv_file_path):
    """
    Converts a CSV file to an Excel file.

    Parameters:
    csv_file_path (str): Path to the input CSV file.

    Returns:
    str: Path to the generated Excel file.
    """
    try:
        # Read CSV file into a DataFrame
        csv_data = pd.read_csv(csv_file_path)

        # Generate the output Excel file path based on the input CSV filename
        csv_file_name = Path(csv_file_path).stem
        output_excel_file = f'{csv_file_name}.xlsx'

        # Convert the DataFrame to Excel
        csv_data.to_excel(output_excel_file, index=False)

        print(f"CSV file '{csv_file_path}' has been converted and saved as '{output_excel_file}'.")

        return output_excel_file  # Return the path to the generated Excel file

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    # Specify the CSV file path
    input_csv_file = 'testDataFinal.csv'

    # Call the function to convert CSV to Excel and get the generated Excel file path
    generated_excel_file = convert_csv_to_excel(input_csv_file)
    print(f"Generated Excel file: {generated_excel_file}")
