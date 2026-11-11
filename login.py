import streamlit as st
from auth import login_user


# ============================================================
# Login Page
# ============================================================

def login_page():

    st.title("🔐 Login")

    st.write("Login to continue.")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if not username or not password:

            st.error("Please enter username and password.")

        else:

            if login_user(username, password):

                st.session_state.logged_in = True
                st.session_state.page = "home"

                st.success("Login successful!")

                st.rerun()

            else:

                st.error("Invalid username or password.")

    st.divider()

    if st.button("Create New Account"):

        st.session_state.page = "signup"

        st.rerun()