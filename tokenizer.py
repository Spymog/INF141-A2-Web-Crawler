import sys

from collections import defaultdict 


# - We iterate in chunks, but the while loop will go through every character just once, which takes O(n) time, where n is the length of the list.
#     - The other operations in the loop take O(1) time. 
# - The total time compexity is O(n)
def tokenize(text: str) -> list:
    tokens = []
    current_token = []
    for char in text:
        try:
            if char.isdigit() or ('a' <= char.lower() <= 'z'): # this line is from chatgpt, after asking how one might only count chars that are English alphabet and digits 0-9
                current_token.append(char)
            else:
                if current_token:
                    tokens.append(''.join(current_token).lower())
                    current_token.clear()
        except Exception:
            continue
        
    # adding the last token (if it's real)
    if current_token:
        tokens.append(''.join(current_token).lower())
        current_token.clear()

    return tokens


# - We iterate through the tokens list just once, which takes O(n) time, where n is the length of the list.
#     - Every operation inside the for loop runs in O(1) because we are using a defaultdict. 
# - The total time complexity is O(n)
def compute_word_frequencies(tokens: list) -> dict:
    word_frequencies = defaultdict(int)
    
    # Iterate through the list of tokens and update their count
    for token in tokens:
        word_frequencies[token] += 1
    
    return dict(word_frequencies)  # Convert defaultdict to a regular dict


# - sorted() uses Timsort, which runs in O(nlogn) time
# - printing each token and their counts takes O(n) time
# - The total time complexity is O(nlogn)
def print_frequencies(frequencies: dict) -> None:

    # Sort the dictionary by values in descending order
    sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    
    # Print the sorted tokens and their counts
    for token, count in sorted_frequencies:
        print(f"{token} = {count}")


if __name__ == '__main__':
    tokens = tokenize(sys.argv[1])
    freqs = compute_word_frequencies(tokens)
    print_frequencies(freqs)

    # python PartA.py alphanumeric_mixed.txt
    # python PartA.py hyphenated.txt
    # python PartA.py mixed_symbols.txt
    # python PartA.py Wellerman.txt
    # python PartA.py bad_input.txt
    # python PartA.py The_Whale.txt
    # python Parta.py The_Modern_Prometheus.txt