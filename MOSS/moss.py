import sys
import re

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

def replace_variable_names(content):
    """
    Helper function that replaces variable names with placeholder ascii characters

    Parameters: 
    - Semi-preprocessed text with unique variables included

    Returns:
    - Text with all the variable names replaced with an ASCII character

    Note: May break with large amounts of code. This tool should only be used as proof of concept 
          and doesn't expect large project sized files.
    """
    # Define a function to generate unique placeholder names
    def generate_placeholder(index):
        return f'var{index}'

    # Use a dictionary to store the mapping between original and placeholder names
    variable_mapping = {}

    # Regular expression pattern to match variable names
    variable_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')

    # Replace variable names with placeholders
    placeholder_index = 1
    def replace(match):
        nonlocal placeholder_index
        variable_name = match.group(1)
        placeholder_name = generate_placeholder(placeholder_index)
        variable_mapping[placeholder_name] = variable_name
        placeholder_index += 1
        return placeholder_name

    processed_code = variable_pattern.sub(replace, content)
    print(f"Variable Mapping: {variable_mapping}")

    return processed_code

def submission_preprocessing(content):
    """
    Submission Preprocessing removes python literals, keywords, and white space and uses placeholders for variables

    Parameters: 
    - Raw text from the source file

    Returns:
    - Cleaned string that can be used for tokenization

    Example: 
        A do run run run, a do run run -> var1var2var3var3var3,var1var2var3var3

    Unlike the original stanford paper example, this code is 
    tailored to python code and replaces unique words with placeholders in the same order
    """
    content = content.lower()

    # Remove Python literals (strings, numbers, and booleans)
    content = re.sub(r'\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"|\'[^\']*\'|\"[^\"]*\"|\b(?:True|False|None|\d+\.\d+|\d+|\.\d+)\b', '', content)

    # Remove Python keywords
    keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield']
    keyword_pattern = r'\b(?:' + '|'.join(keywords) + r')\b'
    content = re.sub(keyword_pattern, '', content)

    # Remove comments
    content = re.sub(r'#.*', '', content)
    content = re.sub(r'(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\")', '', content)  

    # Replace variable names with placeholders 
    content = replace_variable_names(content)

    # Remove new lines and white spaces
    content = re.sub(r'\n', '', content)
    content = re.sub(r'\s+', '', content)

    return content

def tokenization(content, k=5):
    """
    Generate k-grams from a given input string.

    Parameters:
    - input_string: The input string.
    - k: The size of each k-gram.

    Returns:
    - A list containing the k-grams.
    
    Example:
    adorunrunrunadorunrun  ->    adoru dorun orunr runru unrun nrunr runru
                                    unrun nruna runad unado nador adoru dorun
                                    orunr runru unrun
    """
    k_grams = []
    
    # Ensure the input string is long enough for k-grams
    if len(content) < k:
        return k_grams
    
    for i in range(len(content) - k + 1):
        k_gram = content[i:i + k]
        k_grams.append(k_gram)
    
    return k_grams

def hash_tokens(tokenization_array):
    """
    Hashing the tokenized array is done using the python built in hashing function. Stanfords MOSS tool uses proprietary hashing functions. 

    Parameters:
    - Array of k-gram tokens

    Returns:
    - Array of hashed token values
    """
    # Create an empty list to store hashed values
    for i in range(len(tokenization_array)):
        tokenization_array[i] = hash(tokenization_array[i])
    return tokenization_array
    
def subset(hashed_tokens, p=4, w=10):
    """
    Note: This fingerprint method is inferior to the next one and isn't used. 
    Subset subsets the hashed tokens based on the 0 mod p condition. 
    This is what we'll use as a fingerprint. We use a window of size w,
    such that at least one hash from every w hashes is used to prevent gaps. 

    Parameters:
    - Array of hashed tokens
    - p to computed mod with 
    Returns:
    - Subsetted array where each element is divisible by p
    Ex: 
    - Input:
    - 77 72 42 17 98 50 17 98 8 88 67 39 77 72 42 17 98 
    - Output:
    - 72 8 88 72
    """
    hashed_values = []
    count = 0
    # Iterate through each token in the array
    for token in hashed_tokens:

        # Check if the hashed value is divisible by p
        if token % p == 0 or count % w == 0:
            hashed_values.append([token])
        count += 1
    return (hashed_values)

def winnowing(hashed_tokens,k=5, t=8):
    """
    Winnowing creates windows where the minimum hash is selected. 
    If a hash h is selected already in another window it is not selected again.
    Different hashes can have the same value. 

    Parameters:
    - Array of hashed tokens
    - p to computed mod with 
    Returns:
    - Fingerprint array selected using winnowing. 
    Ex: 
    - Input:
    - 77 72 42 17 98 50 17 98 8 88 67 39 77 72 42 17 98 
    - Output:
    - [[17,3] [17,6] [8,8] [39,11] [17,15]]
    """
    w = t - k + 1
    w = 8

    fingerprints = []

    # Apply a sliding window
    for i in range(len(hashed_tokens) - w + 1):
        window = hashed_tokens[i:i + w]

        # Select the rightmost occurrence of the minimum hash value
        min_hash = min(window)
        min_index_in_window = window[::-1].index(min_hash)
        min_index = i + w - 1 - min_index_in_window

        # Record the position of the minimum hash value
        fingerprints.append([min_hash,min_index])
    
    temp_set = set()
    unique_fingerprints = [elem for elem in fingerprints if tuple(elem) not in temp_set and not temp_set.add(tuple(elem))]

    return unique_fingerprints

def count_similar(fingerprints_1, fingerprints_2):
    """
    Moss measures similarity by count of fingerprints that 
    show up in both arrays rather than standard similarity
      metrics (like euclidean distance orcossine)

    Parameters:
    - Two arrays of fingerprints
    Returns:
    - Similarity metric between the fingerprints
    Ex: 
    - Input:
    - [[17,3] [17,6] [8,8] [39,11] [17,15]] 
    - [[17,3] [17,6] [8,8] [39,11] [17,15]]
    - Output:
    - 1.0
    """
    common_fingerprint_count = 0
    for fingerprint in fingerprints_1:
        if fingerprint in fingerprints_2:
            common_fingerprint_count += 1
    # print(common_fingerprint_count)
    # print(len(fingerprints_1))
    # print(len(fingerprints_2))
    s1 = common_fingerprint_count/len(fingerprints_1)
    s2 = common_fingerprint_count/len(fingerprints_2)
    # print(s1)
    # print(s2)

    return [s1,s2]


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <file1_path> <file2_path>")
        sys.exit(1)


    file1_path = sys.argv[1]
    file2_path = sys.argv[2]


    file1_content = read_file(file1_path)
    file2_content = read_file(file2_path)

    if file1_content is not None and file2_content is not None:
        print(f"File 1 Content ({file1_path}):")
        print(file1_content)
        print(f"\nFile 2 Content ({file2_path}):")
        print(file2_content)

    print("--------------------------------------------------------------")

    if file1_content is not None and file2_content is not None:
        file1_stripped = submission_preprocessing(file1_content)
        file2_stripped = submission_preprocessing(file2_content)

        file1_tokenized = tokenization(file1_stripped,k=4)
        file2_tokenized = tokenization(file2_stripped,k=4)

        file1_hashed = hash_tokens(file1_tokenized)
        file2_hashed = hash_tokens(file2_tokenized)

        file1_subsetted = subset(file1_hashed)
        file2_subsetted = subset(file2_hashed)

        similarity_f1 = count_similar(file1_subsetted, file2_subsetted)[0]
        similarity_f2 = count_similar(file1_subsetted, file2_subsetted)[1]
        


        print(f"\nFile 1 Content ({file1_path}) without literals and keywords:")
        print(file1_stripped)
        print(f"File 2 Content ({file2_path}) without literals and keywords:")
        print(file2_stripped)

        print(f"\nFile 1 Content ({file1_path}) Tokenized")
        print(file1_tokenized)
        print(f"File 2 Content ({file2_path}) Tokenized")
        print(file2_tokenized)

        print(f"\nFile 1 Content ({file1_path}) Hashed")
        print(file1_hashed)
        print(f"File 2 Content ({file2_path}) Hashed")
        print(file2_hashed)

        print(f"\nFile 1 Content ({file1_path}) Hashes Subsetted")
        print(file1_subsetted)
        print(f"File 2 Content ({file2_path}) Hashes Subsetted")
        print(file2_subsetted)

        print(f"\nFile 1 Content ({file1_path}) Fingerprint Similarity")
        print(similarity_f1)
        print(f"File 2 Content ({file2_path}) Fingerprint Similarity")
        print(similarity_f2)


    # print(submission_preprocessing("A do run run run, a do run run"))
    # print(tokenization("adorunrunrunadorunrun"))
    # print(subset([72,77,42,17,98,50,17,98,8,88,67,39,77,72,42,17,98]))
    # print(winnowing([72,77,42,17,98,50,17,98,8,88,67,39,77,72,42,17,98]))
        
    # s1, s2 = count_similar(winnowing([72,10,42,17,98,50,14,98,8,92,67,39,77,72,42,17,98]), winnowing([72,77,42,17,98,50,17,98,8,88,67,39,77,72,42,17,98]))
    # print(f"Similarity 1: {s1}, Similarity 2: {s2}")

if __name__ == "__main__":
    main()