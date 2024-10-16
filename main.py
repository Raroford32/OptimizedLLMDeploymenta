import multiprocessing
import os
from app import app
import streamlit as st
from flask import request, jsonify
from llm_integration import generate_code

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

def run_streamlit():
    os.system("streamlit run streamlit_app.py --server.port 8501")

if __name__ == "__main__":
    # Initialize the LLM model
    from llm_integration import load_model
    load_model()

    # Start Flask and Streamlit servers
    flask_process = multiprocessing.Process(target=run_flask)
    streamlit_process = multiprocessing.Process(target=run_streamlit)

    flask_process.start()
    streamlit_process.start()

    print("Flask server running on http://0.0.0.0:5000")
    print("Streamlit server running on http://0.0.0.0:8501")

    flask_process.join()
    streamlit_process.join()
