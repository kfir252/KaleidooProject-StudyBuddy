import textract

# Function to extract text from a file using textract and return it in chunks of paragraphs
def extract_text_from_file(file_path):
    try:
        # Use textract to extract text from the file
        text = textract.process(file_path).decode('utf-8')  # Ensure the text is decoded to UTF-8 format

        # Split the text by paragraphs (assuming paragraphs are separated by double newlines)
        paragraphs = text.split('\n\n')

        # Create a list to hold the chunks of text
        chunks = []

        # Iterate over paragraphs and further split them into chunks of max 5 lines
        for paragraph in paragraphs:
            lines = paragraph.splitlines()

            # Split paragraph into chunks of at most 5 lines
            for i in range(0, len(lines), 5):
                chunk = '\n'.join(lines[i:i+5])  # Join at most 5 lines per chunk
                if chunk.strip():  # Avoid adding empty chunks
                    chunks.append(chunk)

        return chunks

    except Exception as e:
        return [f"Error extracting text: {str(e)}"]
