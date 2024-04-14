import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def show_statistics():
    st.title('Productivity Percentage by Session')  # Set the title of the page

    # Load the Excel file into a DataFrame
    file_path = 'testDataFinal.xlsx'

    try:
        df = pd.read_excel(file_path, engine='openpyxl')  # Read the Excel file
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        return
    except Exception as e:
        st.error(f"Error occurred while reading the Excel file: {e}")
        return

    # Check if the required columns exist
    required_columns = ["SessionLenght", "SessionWithoutPhone", "seq"]
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Error: Column '{col}' not found in the Excel file.")
            return

    # Create a multi-select widget to choose sessions (seq)
    session_options = sorted(df['seq'].unique())
    selected_sessions = st.multiselect('Select Sessions (seq)', session_options)

    if not selected_sessions:
        st.warning("Please select at least one session (seq).")
        return

    # Filter DataFrame based on the selected sessions
    df_selected = df[df['seq'].isin(selected_sessions)]

    if df_selected.empty:
        st.warning("No data found for the selected sessions.")
        return

    # Calculate productivity percentage for the selected sessions
    df_selected['ProductivityPercentage'] = (df_selected['SessionWithoutPhone'] / df_selected['SessionLenght']) * 100

    # Plotting the graph using matplotlib
    st.write("Productivity Percentage Plot for Selected Sessions:")
    fig, ax = plt.subplots(figsize=(10, 6))  # Set the figure size (width, height)

    # Generate a color map based on number of selected sessions
    color_map = plt.get_cmap('tab10')  # You can use any colormap (e.g., 'viridis', 'plasma', 'tab10')

    # Iterate over selected sessions to plot each session's data
    for i, session in enumerate(selected_sessions):
        session_data = df_selected[df_selected['seq'] == session]

        # Sort session data by SessionLength
        session_data_sorted = session_data.sort_values(by='SessionLenght')

        # Extract sorted SessionLength and corresponding ProductivityPercentage
        x_sorted = session_data_sorted['SessionLenght']
        y_sorted = session_data_sorted['ProductivityPercentage']

        # Plot sorted data with scatter, assigning a unique color to each session
        ax.scatter(x_sorted, y_sorted, marker='x', color=color_map(i), label=f'Session {session}')

    # Set plot title, labels, limits, legend, grid, and display options
    ax.set_title('Productivity Percentage - Selected Sessions')
    ax.set_xlabel('Session Length (minutes)')
    ax.set_ylabel('Productivity Percentage (%)')
    ax.set_ylim(0, 100)  # Set y-axis limit from 0 to 100 for percentage
    ax.legend()  # Show legend with session labels
    ax.grid(True)  # Show grid
    ax.set_xlim(left=0)  # Set x-axis minimum limit to 0

    # Display the plot in Streamlit
    st.pyplot(fig)

# Run the Streamlit app
if __name__ == '__main__':
    show_statistics()
