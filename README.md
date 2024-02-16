# MOSS
![image](https://github.com/saiccoumar/MOSS/assets/55699636/6c05ac01-6969-4f7f-adec-0fc80f3c372a)
by Sai Coumar
Welcome to my implementation of MOSS from scratch in python! MOSS, known as Measure of Similarity Software, is a tool that is used to detect plagiarism; it's often used to compare code similarity in computer science education and has been used for decades. This was done as an exercise to understand how MOSS works. In reality, MOSS can be used as a tool with relative ease and re-implemenatation is completely unnecessary - which is why reimplementations aren't very common. It's also important to note certain functions, like the hashing and text preprocessing, are done with proprietary hashing functions and tailored to specific programming languages. If you ever have to use MOSS, purchase the binary from Alex Aiken or look up integration yourself here: https://theory.stanford.edu/~aiken/moss/. 
## Usage:
```
python moss.py <path_to_python_file> <path_to_copied_python_file>
```

## MOSS Explained:
MOSS works by creating fingerprints for code and then checking the similarity between the fingerprints. There are many similarity algorithms, and naively you can check character by character, but fingerprinting has good results and can defend against some simple adversarial techniques like variable renaming. 

### Preprocessing:
The first step in MOSS is preprocessing the raw text. This is done by lowercasing all the text, replacing literals and language specific keywords, comments, replacing variables with placeholders, and removing whitespaces/newlines. It's better to avoid using simple one-character variable names. For my implementation I used vari where i is the ith variable to be instantiated/used in the code. Note that my MOSS will only work well on python because I specifically preprocessed python keywords and literals. Different preprocessing must be used with different languages. 
```
ex.
A do run run run, a do run run -> var1var2var3var3var3,var1var2var3var3
```

### Tokenization:
The processed string is then tokenized by being split into K-grams. K-grams are contiguous sequences of k items, commonly used in text processing and similarity analysis but also popular in genome sequences. K-grams are useful in text analysis because we analyze sections of text without creating gaps of sections that are ignored. 
```
ex.
A do run run run, a do run run -> var1var2var3var3var3,var1var2var3var3
```

### Hashing:
The tokens are then hashed into numbers for each token which are easier to compare. The hash function I used was the default hashing function from python but you could easily use something more complex like sha1. Stanford likely uses a custom proprietary hashing function.
```
ex.
adoru dorun orunr runru unrun nrunr runru
unrun nruna runad unado nador adoru dorun
orunr runru unrun -> 77 72 42 17 98 50 17 98 8 88 67 39 77 72 42
17 98
```

### Winnowing
The hash tokens are then reduced into fingerprints using the winnowing algorithm. Winnowing creates windows where the minimum hash is selected. If a hash h is selected already in another window it is not selected again. Different hashes can have the same value.  
```
ex.
77 72 42 17 98 50 17 98 8 88 67 39 77 72 42 17 98 -> [[17,3] [17,6] [8,8] [39,11] [17,15]]
```

### Similarity Count
With the two fingerprints developed, we compare them and count how many common tokens are in both fingerprints. Comparing the proportions of similar tokens to the amount of tokens we have in a fingerprint tells us how similar code is. Similarity ~905 or higher likely has been copied
```
[[17,3] [17,6] [8,8] [39,11] [17,15]] and [[17,3] [17,6] [8,8] [39,11] [18,19]] -> 0.8
```

Once again, this implementation is simplified. Check out the original theory that I used to make this: https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf
