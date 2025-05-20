from textblob import TextBlob
import random
import os

def load_words():
    """Load words from lyrics.txt file and predefined titles."""
    # Read the content of the file
    try:
        with open('lyrics.txt', 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print("Error: lyrics.txt file not found in the current directory.")
        print(f"Current directory: {os.getcwd()}")
        return [], []

    # Clean and process the text
    text = text.lower()
    text = text.replace("\n", " ")
    text = text.replace(",", "")

    # Split the text into a list of words
    lyrics = text.split()

    # Predefined list of song titles
    titles = ['20','Dollar','Nose','Bleed','7','Minutes','In','Heaven','Church','Sunshine','Riptide','Bishops','Knife','Trick','The','Mighty','Fall','Death','Valley','The','Kids','Arent','Alright','She\'s','My','Winona','The','Takes','Over','The','Breaks','Over','Don\'t','You','Know','Who','I','Think','I','Am','?','The','After','Life','Of','The','Party','Its','Hard','To','Say','I','Do','When','I','Don\'t','Back','To','Earth','Grand','Theft','Autumn','/','Where','Is','Your','Boy','Get','Busy','Living','Or','Get','Busy','Dying','Do','Your','Part','To','Save','The','Scene','and','Stop','Going','To','Shows','Saturday','A','Little','Less','Sixteen','Candles','A','Little','More','Touch','Me','Twin','Skeletons','Hotel','In','NYC','I','Don\'t','Care','Sugar','We\'re','Going','Down','Dance','Dance','My','Songs','Know','What','You','Did','In','The','Dark','Light','Em','Up','Young','Volcanoes','Alone','Together','Centuries','Stay','Frosty','Royal','Milk','Tea','The','Pheonix','Wilson','Expensive','Mistakes','The','Last','Of','The','Real','Ones','Thanks','For','The','Memories','Immortals','Irresistible','Young','And','Menace','Champion','Just','One','Yesterday','This','Ain\'t','A','Scene','It\'s','An','Arms','Race','Where','Did','The','Party','Go','Save','Rock','And','Roll','Fourth','Of','July','Sophomore','Slump','Or','Comeback','Of','The','Year','The','Shipped','Gold','Standard','7','Minutes','In','Heaven','Hum','Hallelujah','Dear', 'Future','Self','Hands','Up','XO','27','Run','Dry','Explode','I\'m','Like','A','Lawyer','With','The','Way','I\'m','Always','Trying','To','Get','You','Off','Tell','That','Mick','He','Just','Made','My','List','Of','Things','To','Do','Today','Yule','Shoot','Your','Eye','Out','What','A','Catch','Donnie']
    
    return titles, lyrics

def categorize_words(all_words):
    """Categorize words into parts of speech using TextBlob."""
    # Custom dictionary for manual tags
    custom_tags = {
        "DNA": "NN",         # Noun
        "TNA": "NN",         # Noun
        "dick": "NN",
        "workin'": "VB",     # Verb (informal form)
        "fuckin'": "VB",     # Verb (informal form)
        "see-through": "JJ", # Adjective
        "bel": "NN",         # Noun
        "air": "NN",         # Noun
        "malibu": "NN",      # Noun (not a pronoun)
        "i'll": "PRP",       # Pronoun
        "we're": "PRP",      # Pronoun
        "they're": "PRP",    # Pronoun
        "don't": "VB",       # Verb
        "can't": "VB",       # Verb
        "won't": "VB",       # Verb
        "ain't": "VB",       # Verb
    }
    
    # Initialize lists for different parts of speech
    word_categories = {
        'nouns': [],
        'verbs': [],
        'adjectives': [],
        'adverbs': [],
        'pronouns': [],
        'prepositions': [],
        'conjunctions': [],
        'articles': [],
        'subject_pronouns': [],  # Pronouns that can start a sentence (I, you, he, she, etc.)
        'object_pronouns': [],   # Pronouns that are objects (me, him, her, etc.)
        'others': []
    }
    
    # Join all words into a single string for TextBlob
    all_words_string = ' '.join(all_words)
    
    # Create a TextBlob object
    blob = TextBlob(all_words_string)
    
    # Categorize words based on their parts of speech
    for word, pos in blob.tags:
        pos = custom_tags.get(word.lower(), pos)  # Use custom tags if available
        
        if pos.startswith('NN'):
            word_categories['nouns'].append(word)
        elif pos.startswith('VB'):
            word_categories['verbs'].append(word)
        elif pos.startswith('JJ'):
            word_categories['adjectives'].append(word)
        elif pos.startswith('RB'):
            word_categories['adverbs'].append(word)
        elif pos == 'PRP':
            word_categories['pronouns'].append(word)
            # Categorize pronouns as subject or object
            if word.lower() in ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'who', 'i\'ll', 'you\'ll', 'we\'ll', 'they\'ll']:
                word_categories['subject_pronouns'].append(word)
            elif word.lower() in ['me', 'him', 'her', 'us', 'them', 'whom']:
                word_categories['object_pronouns'].append(word)
        elif pos == 'IN':
            word_categories['prepositions'].append(word)
        elif pos == 'CC':
            word_categories['conjunctions'].append(word)
        elif pos == 'DT':  # Articles are often tagged as determiners (DT)
            word_categories['articles'].append(word)
        else:
            word_categories['others'].append(word)
    
    # Remove duplicates from all categories
    for category in word_categories:
        word_categories[category] = remove_duplicates_list(word_categories[category])
    
    return word_categories, blob

def remove_duplicates_list(word_list):
    """Remove duplicate words from a list while preserving case."""
    lowercase_list = [word.lower() for word in word_list]
    seen = set()
    unique_list = []
    for i, word in enumerate(lowercase_list):
        if word not in seen:
            unique_list.append(word_list[i])  # Keep original case
            seen.add(word)
    return unique_list

def capitalize_title(title):
    """Properly capitalize a title."""
    # Words that shouldn't be capitalized in a title (unless they're the first word)
    lowercase_words = {'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 
                      'to', 'from', 'by', 'in', 'of', 'with', 'as'}
    
    words = title.split()
    if not words:
        return ""
    
    # Always capitalize the first word
    result = [words[0].capitalize()]
    
    # Process the rest of the words
    for word in words[1:]:
        if word.lower() in lowercase_words:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    
    return ' '.join(result)

def generate_titles(word_categories, blob, num_titles=10, mode='grammar'):
    """Generate song titles based on the specified mode."""
    titles = []
    
    for _ in range(num_titles):
        if mode == 'true_random':
            title = generate_true_random_title(word_categories)
        elif mode == 'grammar_basic':
            title = generate_grammar_basic_title(word_categories)
        elif mode == 'grammar_complex':
            title = generate_grammar_complex_title(word_categories)
        elif mode == 'noun_phrase':
            title = generate_noun_phrase_title(blob)
        else:  # Default to grammar_basic
            title = generate_grammar_basic_title(word_categories)
        
        titles.append(capitalize_title(title))
    
    return titles

def generate_true_random_title(word_categories):
    """Generate a completely random title."""
    all_words = []
    for category in word_categories.values():
        all_words.extend(category)
    
    # Generate 2-4 random words
    num_words = random.randint(2, 4)
    selected_words = [random.choice(all_words) for _ in range(num_words)]
    
    return ' '.join(selected_words)

def generate_grammar_basic_title(word_categories):
    """Generate a title with basic grammar rules."""
    patterns = [
        # Pattern 1: Article + Adjective + Noun
        lambda: ' '.join([
            random.choice(word_categories['articles']),
            random.choice(word_categories['adjectives']),
            random.choice(word_categories['nouns'])
        ]),
        
        # Pattern 2: Adjective + Noun + Verb
        lambda: ' '.join([
            random.choice(word_categories['adjectives']),
            random.choice(word_categories['nouns']),
            random.choice(word_categories['verbs'])
        ]),
        
        # Pattern 3: Noun + Verb + Adjective
        lambda: ' '.join([
            random.choice(word_categories['nouns']),
            random.choice(word_categories['verbs']),
            random.choice(word_categories['adjectives'])
        ]),
        
        # Pattern 4: Verb + Article + Noun
        lambda: ' '.join([
            random.choice(word_categories['verbs']),
            random.choice(word_categories['articles']),
            random.choice(word_categories['nouns'])
        ]),
        
        # Pattern 5: Noun + Preposition + Noun
        lambda: ' '.join([
            random.choice(word_categories['nouns']),
            random.choice(word_categories['prepositions']),
            random.choice(word_categories['nouns'])
        ]),
    ]
    
    # Choose a random pattern
    pattern_func = random.choice(patterns)
    return pattern_func()

def generate_grammar_complex_title(word_categories):
    """Generate a title with more complex grammar rules."""
    patterns = [
        # Pattern 1: Subject Pronoun + Verb + Preposition + Article + Noun
        lambda: ' '.join([
            random.choice(word_categories['subject_pronouns']),
            random.choice(word_categories['verbs']),
            random.choice(word_categories['prepositions']),
            random.choice(word_categories['articles']),
            random.choice(word_categories['nouns'])
        ]),
        
        # Pattern 2: Article + Adjective + Noun + Verb + Adverb
        lambda: ' '.join([
            random.choice(word_categories['articles']),
            random.choice(word_categories['adjectives']),
            random.choice(word_categories['nouns']),
            random.choice(word_categories['verbs']),
            random.choice(word_categories['adverbs'] if word_categories['adverbs'] else word_categories['adjectives'])
        ]),
        
        # Pattern 3: Verb + Article + Adjective + Noun
        lambda: ' '.join([
            random.choice(word_categories['verbs']),
            random.choice(word_categories['articles']),
            random.choice(word_categories['adjectives']),
            random.choice(word_categories['nouns'])
        ]),
        
        # Pattern 4: Noun + Conjunction + Noun
        lambda: ' '.join([
            random.choice(word_categories['nouns']),
            random.choice(word_categories['conjunctions']),
            random.choice(word_categories['nouns'])
        ]),
        
        # Pattern 5: Adjective + Noun + Preposition + Adjective + Noun
        lambda: ' '.join([
            random.choice(word_categories['adjectives']),
            random.choice(word_categories['nouns']),
            random.choice(word_categories['prepositions']),
            random.choice(word_categories['adjectives']),
            random.choice(word_categories['nouns'])
        ]),
    ]
    
    # Choose a random pattern
    pattern_func = random.choice(patterns)
    return pattern_func()

def generate_noun_phrase_title(blob):
    """Generate a title using TextBlob's noun phrases."""
    noun_phrases = list(blob.noun_phrases)
    if not noun_phrases:
        return "No noun phrases found"
    
    # Choose 1-2 random noun phrases
    num_phrases = random.randint(1, min(2, len(noun_phrases)))
    selected_phrases = random.sample(noun_phrases, num_phrases)
    
    return ' '.join(selected_phrases)

def main():
    """Main function to run the song title generator."""
    print("Song Title Generator")
    print("===================")
    
    # Load words from files
    titles, lyrics = load_words()
    all_words = titles + lyrics
    
    # Categorize words
    word_categories, blob = categorize_words(all_words)
    
    # Main loop
    while True:
        print("\nOptions:")
        print("1. True Random (completely random words)")
        print("2. Basic Grammar (simple patterns)")
        print("3. Complex Grammar (more complex patterns)")
        print("4. Noun Phrases (using TextBlob's noun phrases)")
        print("5. Exit")
        
        choice = input("\nSelect a mode (1-5): ")
        
        if choice == '5':
            print("Goodbye!")
            break
        
        try:
            num_titles = int(input("How many titles do you want to generate? (1-20): "))
            num_titles = max(1, min(20, num_titles))  # Limit between 1 and 20
        except ValueError:
            num_titles = 10
            print("Invalid input. Generating 10 titles.")
        
        mode_map = {
            '1': 'true_random',
            '2': 'grammar_basic',
            '3': 'grammar_complex',
            '4': 'noun_phrase'
        }
        
        mode = mode_map.get(choice, 'grammar_basic')
        
        print("\nGenerated Titles:")
        print("-----------------")
        titles = generate_titles(word_categories, blob, num_titles, mode)
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")

if __name__ == "__main__":
    main()
