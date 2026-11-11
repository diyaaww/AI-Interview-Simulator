import streamlit as st
from auth import register_user


# ============================================================
# Sign Up Page
# ============================================================

def signup_page():

    st.title("📝 Create Account")

    st.write("Create your account to continue.")

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Create Account"):

        if (
            not name or
            not email or
            not username or
            not password or
            not confirm_password
        ):

            st.error("Please fill all fields.")

        elif password != confirm_password:

            st.error("Passwords do not match.")

        else:

            success = register_user(
                name,
                email,
                username,
                password
            )

            if success:

                st.success("Account created successfully!")

                st.session_state.page = "login"

                st.rerun()

            else:

                st.error("Username already exists.")

    st.divider()

    if st.button("Already have an account? Login"):

        st.session_state.page = "login"

        st.rerun()