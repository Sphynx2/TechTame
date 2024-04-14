import streamlit as st

def app():


    # Create space to center text
    col1, col2, col3 = st.columns([1, 4, 1])  # Create three columns with width ratio 1:4:1

    # Display "TechTame" centered in the middle column (col2)
    with col2:
        # Center-align the text and adjust size and position using markdown
        st.markdown("<h1 style='text-align: center; font-size: 6em; margin-top: 50px;'>TechTame</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: right; font-size: 2em; margin-top: 50px;'>-by Singurii4Neuroni</h2>",unsafe_allow_html=True)
# Call the app() function to run the Streamlit app
if __name__ == "__main__":
    app()
