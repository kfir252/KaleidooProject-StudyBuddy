from flask import Flask, request, jsonify
from GeminiHandler import chat_session, NOT_ENOUGH_DATA_ERROR_MESSAGE, OUTPUT_LOOK
import uuid

def create_app(db):
    """
    Factory function to create Flask app.
    Takes FAISS database as a parameter and sets it up in the Flask app.
    """
    app = Flask(__name__)

    # API to handle queries
    @app.route('/query', methods=['POST'])
    def handle_query():
        data = request.json
        query = data.get('query', '')

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Search the FAISS database
        relevant_texts = db.search(query, 5)

        if not relevant_texts:
            return jsonify({"error": NOT_ENOUGH_DATA_ERROR_MESSAGE}), 404

        combined_context = " ".join(relevant_texts)

        try:
            response = chat_session.send_message(
                'I\'m using your answer in my program. '
                'Answer this question: ' + query + ', '
                'with only this data, this data can be wrong but it\'s ok, '
                'use only this data: ' + combined_context + '. '
                'The answer should be: ' + OUTPUT_LOOK + '. '
                'Don\'t speak to me, just give me information from the given data, '
                'and don\'t judge the data, please!'
            )

            return jsonify({"response": response.text})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

# No need for the main entry point in this file
# The app will be created and run from main.py



app = Flask(__name__)

# In-memory storage for answers (In production, use a database)
query_results = {}

def process_query(query, db):
    """
    Process the query with FAISS database and Whisper, and return the result.
    """
    # Search the FAISS database for relevant texts
    relevant_texts = db.search(query, 5)

    if not relevant_texts:
        return NOT_ENOUGH_DATA_ERROR_MESSAGE

    # Combine relevant texts
    combined_context = " ".join(relevant_texts)

    try:
        # Send the query to the chat model
        response = chat_session.send_message(
            'Answer this question: ' + query + ', with only this data: ' + combined_context + '. '
            'The answer should be: ' + OUTPUT_LOOK + '. '
            'Don’t judge the data, please!'
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# API to submit a query
@app.route('/query', methods=['POST'])
def submit_query():
    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Generate a unique query ID
    query_id = str(uuid.uuid4())

    # Process the query asynchronously (this is just simulated here)
    db = request.app.config['db']
    result = process_query(query, db)

    # Store the result
    query_results[query_id] = result

    return jsonify({"query_id": query_id})


