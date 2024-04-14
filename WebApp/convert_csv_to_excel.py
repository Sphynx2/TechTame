import pandas as pd

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
        output_excel_file = csv_file_path.replace('.csv', '.xlsx')

        # Convert the DataFrame to Excel
        csv_data.to_excel(output_excel_file, index=False)

        return output_excel_file  # Return the path to the generated Excel file

    except Exception as e:
        raise ValueError(f"Error during CSV to Excel conversion: {e}")