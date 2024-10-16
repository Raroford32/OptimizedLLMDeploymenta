import multiprocessing
import os
import logging
from app import app
import streamlit as st
from flask import request, jsonify
from llm_integration import load_model, generate_code

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

def run_streamlit():
    os.system("streamlit run streamlit_app.py --server.port 8501")

if __name__ == "__main__":
    try:
        # Initialize the LLM model
        logging.info("Initializing LLM model...")
        model = load_model()
        logging.info("LLM model initialized successfully")

        # Update the Flask app's generate_code function to use the optimized version
        @app.route('/generate', methods=['POST'])
        def generate():
            data = request.json
            project_description = data.get('project_description')
            
            if not project_description:
                return jsonify({'error': 'Project description is required'}), 400

            try:
                generated_code = generate_code(project_description)
                return jsonify({'code': generated_code})
            except Exception as e:
                logging.error(f"Error generating code: {str(e)}")
                return jsonify({'error': str(e)}), 500

        # Start Flask and Streamlit servers
        logging.info("Starting Flask and Streamlit servers...")
        flask_process = multiprocessing.Process(target=run_flask)
        streamlit_process = multiprocessing.Process(target=run_streamlit)

        flask_process.start()
        streamlit_process.start()

        logging.info("Flask server running on http://0.0.0.0:5000")
        logging.info("Streamlit server running on http://0.0.0.0:8501")

        flask_process.join()
        streamlit_process.join()
    except Exception as e:
        logging.error(f"Error starting servers: {str(e)}")
        raise
