# Local LLM-Powered Code Generator Chatbot

This project is a C++ code generator chatbot powered by a local Large Language Model (LLM). It uses Flask for the backend API and Streamlit for the user interface.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root directory
   - Add the following variables:
     ```
     FLASK_SECRET_KEY=<your-secret-key>
     DATABASE_URL=<your-database-url>
     ```

4. Run the application:
   ```
   python main.py
   ```

## Usage Guide

1. Open your web browser and navigate to `http://localhost:8501` for the Streamlit interface.
2. Enter your project description in the text area.
3. Click the "Generate Code" button to generate C++ code based on your description.
4. The generated code will be displayed below the input area.

## API Endpoints

- POST `/generate`: Generate C++ code
  - Request body: `{"project_description": "Your project description here"}`
  - Response: `{"code": "Generated C++ code here"}`

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
