import json
import random

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return [item[2] for item in data]  # Extract the comments section from each item

def build_markov_chain(data):
    markov_chain = {}
    for line in data:
        words = line.split()
        for i in range(len(words) - 1):
            if words[i] not in markov_chain:
                markov_chain[words[i]] = []
            markov_chain[words[i]].append(words[i + 1])
    return markov_chain

def generate_sentence(chain, length=20):
    word = random.choice(list(chain.keys()))
    sentence = [word]
    for _ in range(length - 1):
        next_words = chain.get(word, None)
        if not next_words:
            break
        word = random.choice(next_words)
        sentence.append(word)
    return ' '.join(sentence)

# Load the data
data = load_data('output.json')  # Replace with the path to your JSON file

# Build the Markov chain
chain = build_markov_chain(data)

# Generate a sentence
print(generate_sentence(chain))

# Example output length can be adjusted by changing the `length` parameter in `generate_sentence`
