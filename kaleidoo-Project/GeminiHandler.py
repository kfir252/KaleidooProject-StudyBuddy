import os
import google.generativeai as genai

from FaissDatabase import FAISSDatabase
os.system('cls')

import FaissDatabase
os.system('cls')

DATA_FOLDER_PATH = 'testing_database'


genai.configure(api_key='')# <------ Here set Your google.generativeai key


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 100,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)


NOT_ENOUGH_DATA_ERROR_MESSAGE = '\"we dont have enough data to answer this question\"'
OUTPUT_LOOK = 'direct and formatted well'

# Clear warnings
os.system('cls')

def run(db):

    # Input loop to continuously ask user for queries
    while True:
        # Ask the user for a query (context search)
        search_query = input("\nEnter a topic or query to search (or 'exit' to quit): ")
        if search_query.lower() == 'exit':
            break

        # Search the FAISS database
        relevant_texts = db.search(search_query,5)

        if not relevant_texts:
            print("No relevant texts found.")
            continue

        # Combine the relevant texts into a single context for answering
        combined_context = " ".join(relevant_texts)

        # Print the answer
        try:
            response = chat_session.send_message('i\'m using your answer in my program' +
                                                'answer this question:' + search_query + ', ' +
                                                'with only this data, this data can be wrong but it ok, use only this data! :' + combined_context + ', ' +
                                                'the answer should be: '+ OUTPUT_LOOK +
                                                'dont speak to me!, just give me information from the given data!, and don\'t judge the data, please!')

            print(response.text)
        except:
            print('Sorry, I didn\'t understand you..')


