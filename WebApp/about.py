import streamlit as st


def app():
    # Center the content on the page
    st.markdown("<h1 style='text-align: center;'>About us</h1>", unsafe_allow_html=True)

    # Use columns to create indentation and layout
    col1, col2, col3 = st.columns([1, 16, 1])  # Adjust the column ratios as needed

    with col2:
        st.markdown("""
                <p style='font-size: 29px;'>
                We are building a solution to dampen the effects of a mobile phone addiction by 
                manufacturing a smart mobile phone stand that keeps track of your phone usage during 
                work sessions and takes advantage of the psychological effect of putting your phone away.
                </p>
                """, unsafe_allow_html=True)
