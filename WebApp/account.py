import streamlit as st
import hashlib

# Mock user database (for demonstration purposes)
user_database = {
    'user123': {
        'code': '123',
        'password_hash': hashlib.sha256('password123'.encode()).hexdigest(),
        'username': 'Baciu'
    }
}


class SessionState:
    def __init__(self):
        self.logged_in = False
        self.user = None


def authenticate_user(code, password):
    user = user_database.get(code)
    if not user:
        return None  # User not found
    if hashlib.sha256(password.encode()).hexdigest() == user['password_hash']:
        return user  # Authentication successful
    return None  # Incorrect password


def register_user(code, password, username):
    if code in user_database:
        return False  # Code already exists
    user_database[code] = {
        'code': code,
        'password_hash': hashlib.sha256(password.encode()).hexdigest(),
        'username': username
    }
    return True  # Registration successful


def app():
    st.title('Welcome to :violet[TechTame] 🎓')

    session_state = SessionState()

    if not session_state.logged_in:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

        if choice == 'Login':
            code = st.text_input('Serial Code')
            password = st.text_input('Password', type='password')
            if st.button('Login'):
                user = authenticate_user(code, password)
                if user:
                    session_state.logged_in = True
                    session_state.user = user
                    st.success(f'Logged in as {user["username"]}')
                else:
                    st.error('Invalid code or password')

        else:  # Sign up
            code = st.text_input('Serial Code')
            password = st.text_input('Password', type='password')
            username = st.text_input('Enter a unique username')

            if st.button('Create my account'):
                if register_user(code, password, username):
                    st.success('Account created successfully! Please log in.')
                else:
                    st.error('Serial code already exists. Please choose another.')
    else:
        st.write(f'Welcome back, {session_state.user["username"]}!')



