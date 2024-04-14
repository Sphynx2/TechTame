import streamlit as st
from streamlit_option_menu import option_menu
from statistics import show_statistics
import home, about, account
from convert_csv_to_excel import convert_csv_to_excel  # Import your conversion function

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        with st.sidebar:
            app_title = option_menu(
                menu_title='TechTame',
                options=['Home', 'Statistics', 'About', 'Account'],
                icons=['house-fill', 'person-circle', 'info-circle-fill', 'chat-text-fill'],
                default_index=0,
                styles={
                    "container": {"padding": "5px !important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px",
                                 "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Retrieve the selected app based on the option chosen
        selected_app_title = app_title
        selected_app = next((app['function'] for app in self.apps if app['title'] == selected_app_title), None)

        if selected_app:
            selected_app()  # Run the selected app function

def main():
    st.set_page_config(
        page_title="TechTame"
    )

    # Specify the CSV file path
    input_csv_file = 'testDataFinal.csv'

    try:
        # Convert CSV to Excel upon application startup
        convert_csv_to_excel(input_csv_file)

    except Exception as e:
        st.error(f"Error occurred during CSV to Excel conversion: {e}")

    # Create an instance of MultiApp
    multi_app = MultiApp()

    # Add each app with its title and corresponding function
    multi_app.add_app("Home", home.app)
    multi_app.add_app("Statistics", show_statistics)  # Use the show_statistics function from statistics.py
    # multi_app.add_app("Add Work", add_work.app)
    multi_app.add_app("About", about.app)
    multi_app.add_app("Account", account.app)

    # Run the selected app
    multi_app.run()

if __name__ == "__main__":
    main()
