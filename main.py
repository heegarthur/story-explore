import random, os
import nltk
from nltk.corpus import stopwords

# Zorg ervoor dat je de stopwoorden downloadt
nltk.download('stopwords')

# Haal de Engelse stopwoorden op
STOPWORDS = set(stopwords.words('english'))

def load_sentences(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            sentences = f.readlines()
        return [sentence.strip() for sentence in sentences]
    except FileNotFoundError:
        print(f"Error: {file} not found.")
        return []

def load_words(file):
    words = {}
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                parts = line.strip().split(":")
                if len(parts) == 2:  # Zorg ervoor dat we precies 2 delen hebben
                    word, score = parts
                    words[word.lower()] = int(score)  # Gebruik lowercase voor consistente opslag
                else:
                    print(f"Skipping invalid line: {line.strip()}")  # Log ongeldige lijnen
    except FileNotFoundError:
        print(f"Error: {file} not found.")
    return words

def load_shown_sentences(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            sentences = f.readlines()
        return set([sentence.strip() for sentence in sentences])
    except FileNotFoundError:
        return set()

def save_shown_sentences(file, sentences):
    with open(file, 'a', encoding='utf-8') as f:  # Gebruik 'a' voor append (toevoegen)
        for sentence in sentences:
            f.write(f"{sentence}\n")

def save_words(file, words):
    with open(file, 'w', encoding='utf-8') as f:
        for word, score in words.items():
            f.write(f"{word}:{score}\n")

def process_sentence(sentence, words):
    unique_words = set(sentence.split())
    for word in unique_words:
        if word.lower() not in STOPWORDS:  # Exclude stopwords
            if word.lower() not in words:
                words[word.lower()] = 0  # Voeg het woord toe met score 0
    return words

def calculate_score_sentence(sentence, words):
    score = 0
    unique_words = set(sentence.split())
    for word in unique_words:
        if word.lower() not in STOPWORDS:  # Exclude stopwords
            score += words.get(word.lower(), 0)  # Gebruik .lower() voor consistente vergelijkingen
    return score

def show_random_sentence(sentences, words, shown_sentences):
    # Sort sentences based on the highest score
    sentences_with_score = [(sentence, calculate_score_sentence(sentence, words)) for sentence in sentences if sentence not in shown_sentences]
    if not sentences_with_score:
        return None  # If there are no new sentences left
    sentences_with_score.sort(key=lambda x: x[1], reverse=True)  # Sort by score, highest first
    best_sentence = sentences_with_score[0][0]
    shown_sentences.add(best_sentence)  # Add the shown sentence to the list of shown sentences
    return best_sentence

def main():
    sentences_file = "sentences.txt"
    words_file = "words.txt"
    shown_sentences_file = "shown_sentences.txt"  # Bestandsnaam voor de zinnen die al getoond zijn
    
    sentences = load_sentences(sentences_file)
    if not sentences:
        return  # Stop als er geen zinnen kunnen worden geladen
    
    words = load_words(words_file)
    shown_sentences = load_shown_sentences(shown_sentences_file)  # Laad zinnen die al getoond zijn
    
    while True:
        sentence = show_random_sentence(sentences, words, shown_sentences)
        if sentence is None:
            print("All sentences have been shown.")
            break
        clearscreen()
        print(f"\nSentence: {sentence}")
        words = process_sentence(sentence, words)
        
        choice = input("Press 'x' if you liked it, 'c' if it was okay, or 'v' if you didn't like it (q to quit): ").lower()
        
        if choice == 'q':
            break
        
        if choice not in ['x', 'c', 'v']:
            print("Invalid input. Please try again.")
            continue
        
        unique_words = set(sentence.split())
        
        if choice == 'x':
            for word in unique_words:
                if word.lower() not in STOPWORDS:  # Exclude stopwords
                    words[word.lower()] += 1
        elif choice == 'v':
            for word in unique_words:
                if word.lower() not in STOPWORDS:  # Exclude stopwords
                    words[word.lower()] -= 1
        
        # Sort words by score
        words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
        
        save_words(words_file, words)
        save_shown_sentences(shown_sentences_file, [sentence])  # Voeg de getoonde zin toe aan het bestand

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
