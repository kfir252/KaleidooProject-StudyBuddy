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


#starting here:
from sentence_transformers import SentenceTransformer

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