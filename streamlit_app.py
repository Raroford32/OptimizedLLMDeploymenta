import streamlit as st
import requests

st.title("C++ Code Generator")

project_description = st.text_area("Enter your project description:")
if st.button("Generate Code"):
    if project_description:
        response = requests.post("http://localhost:5000/generate", json={"project_description": project_description})
        if response.status_code == 200:
            st.code(response.json()["code"], language="cpp")
        else:
            st.error("An error occurred while generating code. Please try again.")
    else:
        st.warning("Please enter a project description.")
