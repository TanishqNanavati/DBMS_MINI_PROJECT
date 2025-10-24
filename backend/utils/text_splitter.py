import re

def split_text(text, max_length=500, overlap=50):
    """
    Splits long text into smaller chunks while keeping sentences intact.
    
    Parameters:
        text (str): The input text.
        max_length (int): Maximum number of words per chunk.
        overlap (int): Number of words to overlap between chunks.
    
    Returns:
        List[str]: List of text chunks.
    """
    # Split text into sentences using simple regex
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        words_in_sentence = sentence.split()
        sentence_length = len(words_in_sentence)
        
        # If adding this sentence exceeds max_length, finalize current chunk
        if current_length + sentence_length > max_length:
            chunks.append(" ".join(current_chunk))
            # Keep overlap words from previous chunk
            current_chunk = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
            current_length = len(current_chunk)
        
        current_chunk.extend(words_in_sentence)
        current_length += sentence_length
    
    # Add remaining words as last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks
