import threading
from FaissDatabase import FAISSDatabase
from GeminiHandler import run, chat_session
from flask_API import create_app  # Now using the updated create_app

DATA_FOLDER_PATH = 'testing_database'


def start_flask_server(db):
    """
    Starts the Flask server in a separate thread.
    """
    app = create_app(db)  # Passing db to Flask app
    app.run(host='0.0.0.0', port=5000, use_reloader=False)  # Disable reloader for multithreading


if __name__ == "__main__":
    # Initialize FAISS database
    db = FAISSDatabase()
    FAISSDatabase.initDB(DATA_FOLDER_PATH,db)
    #db.add_vector("test vector say hello")
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask_server, args=(db,))
    flask_thread.start()

    # Run the main logic with the initialized database
    run(db)
