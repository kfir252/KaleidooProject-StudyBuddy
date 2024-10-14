# Tel-Hai Study Buddy

Tel-Hai Study Buddy is an AI-driven application designed to assist students in transforming study materials into accessible, searchable content. By converting audio, video, and PDF files into text, we empower students to ask questions and receive answers in real-time using the **Gemini chatbot**.

## Features

- **File Input Support**: Upload and process audio, video, and PDF files.
- **Text Transformation**: Automatically converts input files to text.
- **Vectorization**: Transforms text into vectors for efficient searching and retrieval.
- **FAISS Database**: Stores vectors in a FAISS (Facebook AI Similarity Search) database for fast and scalable search.
- **Gemini Chatbot Integration**: Use the chatbot to interact with the stored data and receive accurate answers from your study materials.
- **User-Friendly UI**: An intuitive chat interface that allows users to ask questions and receive answers quickly.

## How It Works

1. **File Upload**: Users can upload audio, video, or PDF files to the system.
2. **Text Extraction**: Audio and video files are processed for speech-to-text conversion, while PDF files are parsed for text content.
3. **Vectorization**: The extracted text is transformed into vectors using state-of-the-art natural language processing models.
4. **FAISS Database**: The vectors are stored in a FAISS database for fast similarity search.
5. **Chatbot Querying**: The **Gemini chatbot** processes user queries and fetches relevant answers from the FAISS database, delivering responses in a chat format.
6. **Real-Time Interaction**: Users can communicate with the chatbot through a clean and responsive UI designed for seamless question-and-answer interactions.

## Tech Stack

- **Backend**: Python for text extraction, vectorization, and FAISS database management.
- **AI**: all-MiniLM-L6-v2 model for vector transformation,openai-Whisper for audio to text transformation.
- **Chatbot**: Gemini chatbot for interacting with the FAISS database and answering questions.
- **Database**: FAISS (Facebook AI Similarity Search) for vector-based searching.
- **Frontend**: A simple and intuitive chat-based user interface (UI) for user interaction.

## Example Use
An example demonstration of the project in action can be viewed [here](https://youtu.be/EFOT5z9LMwI).

![image](https://github.com/user-attachments/assets/a3a413f2-655d-421a-829e-cc316d772255)
