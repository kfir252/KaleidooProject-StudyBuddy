import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

from StringToVector_mod import string_to_vectors
from PDFToString import extract_text_from_file
from VideoToString import video_to_string
from SoundToString import SoundToString

from transformers import pipeline

# Load a pre-trained question-answering model
qa_model = pipeline('question-answering', model='deepset/roberta-base-squad2')






class setup:
    ''' Hide The warnings:
            Windows (Command Prompt):
                cmd: set TF_ENABLE_ONEDNN_OPTS=0

            Linux/macOS:
                export TF_ENABLE_ONEDNN_OPTS=0
    '''
    import os
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)  # Suppress TensorFlow warnings
    warnings.filterwarnings('ignore', category=FutureWarning)  # Suppress Hugging Face warnings
    warnings.filterwarnings("ignore", message="Failed to launch Triton kernels")
    warnings.filterwarnings("ignore", message=".*Torch was not compiled with flash attention.*")
    warnings.filterwarnings("ignore", message=".*Found Intel OpenMP.*")
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# Load a pre-trained model once (global for efficiency)
model = SentenceTransformer('all-MiniLM-L6-v2')


def string_to_vectors(text):
    """
    Convert a string or a list of strings to vector embeddings using Sentence-Transformers.

    Args:
    - text (str or list of str): A string or list of strings to be converted to embeddings.

    Returns:
    - numpy.ndarray:
        For a single string: Shape will be (1, 384) (where 384 is the dimensionality of the embeddings).
        For a list of strings: Shape will be (N, 384), where N is the number of strings.
    """
    # Check if input is a single string, if so convert it to a list
    if isinstance(text, str):
        text = [text]

    # Generate embeddings
    embeddings = model.encode(text)
    return embeddings


class FAISSDatabase:
    def __init__(self, dimension=384):
        """
        Initialize a FAISS database for vector similarity search.

        Args:
        - dimension (int): The dimensionality of the embeddings (default is 384 for 'all-MiniLM-L6-v2').
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(self.dimension)  # Using L2 distance for search
        self.text_data = []  # Store the original text corresponding to each vector

    def add_vector(self, text):
        """
        Add a new text/vector to the FAISS index.

        Args:
        - text (str or list of str): A string or list of strings to be added to the database.
        """
        vectors = string_to_vectors(text)
        self.index.add(np.array(vectors))

        # Store the original text corresponding to each vector
        if isinstance(text, str):
            self.text_data.append(text)
        else:
            self.text_data.extend(text)  # If text is a list of strings

    def search(self, query_text, top_k=3):
        """
        Search the FAISS index for the most similar vectors to a given query.

        Args:
        - query_text (str): The query string to search for.
        - top_k (int): The number of nearest neighbors to return (default is 3).

        Returns:
        - list of relevant texts (corresponding to the nearest neighbors).
        """
        query_vector = string_to_vectors(query_text)
        distances, indices = self.index.search(np.array(query_vector), top_k)

        relevant_texts = [self.retrieve_text_by_index(index) for index in indices[0]]

        return relevant_texts

    def retrieve_text_by_index(self, index):
        """
        Retrieve the text corresponding to a specific FAISS index.

        Args:
        - index (int): The index of the vector in the FAISS database.

        Returns:
        - str: The original text corresponding to the vector.
        """
        if index < len(self.text_data):
            return self.text_data[index]
        else:
            return "No text found for this index"

    def answer_question(self, user_question, context):
        """
        Use the question-answering model to provide an answer based on the context.

        Args:
        - user_question (str): The question asked by the user.
        - context (str): The context in which the question should be answered (retrieved text).

        Returns:
        - str: The answer to the user's question.
        """
        answer = qa_model(question=user_question, context=context)
        return answer['answer']

    def save(self, file_path):
        """
        Save the FAISS index to a file.

        Args:
        - file_path (str): The file path to save the index to.
        """
        faiss.write_index(self.index, file_path)
        print(f"Database saved to {file_path}")

    def load(self, file_path):
        """
        Load the FAISS index from a file.

        Args:
        - file_path (str): The file path to load the index from.
        """
        self.index = faiss.read_index(file_path)
        print(f"Database loaded from {file_path}")

    @staticmethod
    def initDB(path,db):
        # Initialize the FAISSDatabase class
        os.system('cls')

        # Add vectors to the database
        load_all_files(path, db)

        return db


def load_all_files(path, DB):
    """
    Walk through the directory and process text files.

    Args:
    - path (str): The directory path to scan.
    - DB (FAISSDatabase): The FAISS database instance to store the vectors.
    """
    for root, dirs, files in os.walk(path):
        for file_name in files:
            full_path = os.path.join(root, file_name)  # Get the full path

            print(f"Processing {file_name} - Please wait.")
            if file_name.endswith('.wav') or file_name.endswith('.mp3'):
                content = SoundToString(full_path)
                DB.add_vector('\n'.join(content))
                print(content)

            elif file_name.endswith('.pdf'):
                content = extract_text_from_file(full_path)  # This now returns a list of paragraphs

                if content and isinstance(content, list):
                    for paragraph in content:
                        DB.add_vector(paragraph)
                    # prints the first paragraph
                    print('First line:', content[0] if content else 'No content')

                else:
                    print('Error or no content in PDF file.')

            elif file_name.endswith('.mp4'):
                visual_content, sound_path = video_to_string(full_path)
                DB.add_vector(visual_content)
                print(visual_content)

            print('\n')
