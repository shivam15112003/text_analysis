import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import nltk
nltk.download('punkt')

# Load input data
input_data = pd.read_excel("Input.xlsx")

# Load positive and negative words
with open('positive-words.txt', 'r') as file:
    positive_words = [word.strip() for word in file.readlines()]

with open('negative-words.txt', 'r') as file:
    negative_words = [word.strip() for word in file.readlines()]

# Load stopwords
stop_words = []
stop_files = [
    'StopWords_Auditor.txt', 'StopWords_Currencies.txt', 'StopWords_DatesandNumbers.txt',
    'StopWords_Generic.txt', 'StopWords_GenericLong.txt', 'StopWords_Geographic.txt', 'StopWords_Names.txt'
]

for stop_file in stop_files:
    with open(stop_file, 'r') as file:
        stop_words += [word.strip() for word in file.readlines()]

# Cleaning function to remove stopwords
def clean_text(tokenized_words):
    return [word for word in tokenized_words if word.lower() not in stop_words]

# Calculate positive and negative scores
def calculate_sentiment_scores(words):
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    return positive_score, negative_score

# Personal pronoun count
def count_personal_pronouns(text):
    pronoun_pattern = r'\b(I|we|my|ours|us)\b'
    matches = re.findall(pronoun_pattern, text, flags=re.IGNORECASE)
    return len(matches)

# Syllable count function
def count_syllables(word):
    word = word.lower()
    matches = re.findall(r'[aeiouy]+', word)
    count = len(matches)
    if word.endswith(('es', 'ed')):
        count = max(1, count - 1)
    return count

# Extract article text from URL
def extract_article(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.text.strip() if soup.title else ""
            paragraphs = [p.text.strip() for p in soup.find_all('p')]
            article = ' '.join(paragraphs)
            return title, article
        else:
            print(f"Error fetching {url}: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None, None

# Perform full text analysis
def analyze_text(text):
    words = nltk.word_tokenize(text)
    clean_words = clean_text(words)
    sentences = nltk.sent_tokenize(text)

    positive_score, negative_score = calculate_sentiment_scores(clean_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 1e-6)
    subjectivity_score = (positive_score + negative_score) / (len(clean_words) + 1e-6)

    avg_sentence_length = sum(len(s.split()) for s in sentences) / (len(sentences) or 1)
    complex_word_count = sum(1 for word in clean_words if count_syllables(word) > 2)
    percentage_complex_words = (complex_word_count / (len(clean_words) or 1)) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    avg_words_per_sentence = len(clean_words) / (len(sentences) or 1)
    personal_pronouns = count_personal_pronouns(text)
    avg_word_length = sum(len(word) for word in clean_words) / (len(clean_words) or 1)

    return [
        positive_score, negative_score, polarity_score, subjectivity_score,
        avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence,
        complex_word_count, len(clean_words), personal_pronouns, avg_word_length
    ]

# Final analysis loop
results = []
for _, row in input_data.iterrows():
    url_id, url = row['URL_ID'], row['URL']
    title, article = extract_article(url)
    
    if article:
        with open(f"{url_id}.txt", "w", encoding="utf-8") as f:
            f.write(title + '\n' + article)
        
        metrics = analyze_text(article)
        results.append([url_id, url, title, article] + metrics)
    else:
        results.append([url_id, url, "", ""] + [None]*12)

# Output to DataFrame
columns = [
    'URL_ID', 'URL', 'Article_Title', 'Article_Text',
    'positive_score', 'negative_score', 'polarity_score', 'subjectivity_score',
    'avg_sentence_length', 'percentage_complex_words', 'fog_index',
    'avg_words_per_sentence', 'complex_word_count', 'word_count',
    'personal_pronouns', 'avg_word_length'
]

output_df = pd.DataFrame(results, columns=columns)
output_df.to_excel("Output.xlsx", index=False)
