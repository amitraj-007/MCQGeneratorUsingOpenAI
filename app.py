from flask import Flask, request, jsonify
import os
import json
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Loading JSON file
with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

@app.route('/generate_mcqs', methods=['POST'])
def generate_mcqs():
    try:
        data = request.json

        uploaded_file = data.get("file")
        mcq_count = data.get("mcq_count")
        subject = data.get("subject")
        tone = data.get("tone")

        # Read file contents
        text = read_file(uploaded_file)

        # Count tokens and the cost of API call
        with get_openai_callback() as cb:
            response = generate_evaluate_chain(
                {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                }
            )

        # Return response to Flutter
        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
