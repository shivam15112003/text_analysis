import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import nltk
nltk.download('punkt')
#fetching data
input_data = pd.read_excel("Input.xlsx")

#reading postive and negative words
with open('positive-words.txt', 'r') as file:
    positive_words = file.readlines()
    
with open('negative-words.txt', 'r') as file:
    negative_words = file.readlines()

# Load stop words list
stop_word=[]
with open('StopWords_Auditor.txt', 'r') as file:
    stop_wordsa= file.readlines()
  
with open('StopWords_Currencies.txt', 'r') as file:
     stop_wordsc= file.readlines()

with open('StopWords_DatesandNumbers.txt', 'r') as file:
     stop_wordsd= file.readlines()

with open('StopWords_Generic.txt', 'r') as file:
    stop_wordsg= file.readlines()

with open('StopWords_GenericLong.txt', 'r') as file:
     stop_wordgl= file.readlines()
     
with open('StopWords_Geographic.txt', 'r') as file:
    stop_wordsgg=file.readlines()

with open('StopWords_Names.txt', 'r') as file:
    stop_wordsn=file.readlines()
stop_word=stop_wordsa+stop_wordsc+stop_wordsd+stop_wordsg+stop_wordgl+stop_wordsgg+stop_wordsn

def cleaning(tk_word):
    filtered_tokens=[]
    # Filtering stop words
    for tokens in tk_word:
        for i in stop_word:
                if tokens!=i:
                   filtered_tokens.append(tokens)
    # Reconstruction (joining tokens back into a string)
    clean_text = ' '.join(filtered_tokens)  
    return clean_text   

def dir(text,positive_words,negative_words):
    fdir={}
    for words in text:
        if words in positive_words:
            fdir['positive']=words
        if words in negative_words:
            fdir['negative']=words
    return fdir

def count_personal_pronouns(text):
    # Define a regex pattern to match personal pronouns
    pronoun_pattern = r'\b(I|we|my|ours|us)\b'
    # Compile the regex pattern
    regex = re.compile(pronoun_pattern, re.IGNORECASE)
    # Find all matches of the pattern in the text
    matches = regex.findall(text)
    # Count the number of matches
    count = len(matches)
    return count

def count_syllables(word):
    # Define a regex pattern to match vowels
    vowel_pattern = r'[aeiouyAEIOUY]+'
    # Find all matches of vowels in the word
    matches = re.findall(vowel_pattern, word)
    # Count the number of matches
    syllable_count = len(matches)
    # Handle exceptions for words ending with "es" or "ed"
    if word.endswith('es') or word.endswith('ed'):
        syllable_count -= 1  # Subtract 1 from syllable count
    return syllable_count

def extract_article_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_title = soup.title.text.strip()
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.text.strip() for p in paragraphs])
            return article_title, article_text
        else:
            print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"An error occurred while extracting content from {url}: {str(e)}")
        return None, None

def perform_text_analysis(clean_text,fdir):
    try:
        #tokenization
        tk_word= nltk.word_tokenize(clean_text)
        #tokenizing into sentences
        tk_sen= nltk.sent_tokenize(clean_text) 

        # Calculate positive and negative scores
        positive_score,negative_score=0
        for key in fdir:
            if key == 'positive':
                positive_score+=1
            else:
                negative_score+=1
        negative_score=(-1)*negative_score      
       
        #Polarity Score:
        polarity_Score = (positive_score - negative_score)/ ((positive_score + negative_score) + 0.000001)
        
        #subjectivity_score
        subjectivity_score = (positive_score + negative_score )/ ((len(tk_word)) + 0.000001)

        # Calculate average sentence length
        avg_sentence_length = sum(len(sen.split()) for sen in tk_sen) / len(tk_sen)
        
        # Calculate percentage of complex words
        complex_word_count = sum(1 for word in tk_word if count_syllables(word) > 2)
        percentage_complex_words = (complex_word_count / len(tk_word)) * 100
        
        #fog_index
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

        
        # Calculate average number of words per sentence
        avg_words_per_sentence = len(tk_word) / len(tk_sen)
        
        
        #Syllable Count Per Word
        countsyll=()
        for i in tk_word:
            countsyll.append([i,count_syllables(i)])
            
        # Calculate number of personal pronouns
        count_pp=count_personal_pronouns(clean_text)
        
        # Calculate average word length
        word_lengths = sum([len(word) for word in tk_word])
        avg_word_length = sum(word_lengths) / len(word_lengths)
        
        #lenght of clean word
        len_of_clean_txt=len(clean_text)

        
        return [positive_score, negative_score, polarity_Score, subjectivity_score, 
                avg_sentence_length, percentage_complex_words, fog_index, 
                avg_words_per_sentence, complex_word_count, len(tk_word), 
                countsyll, count_pp, avg_word_length]
    
    except Exception as e:
        print(f"An error occurred during text analysis: {str(e)}")
        return (None,) * 13  # Return a tuple of Nones if an error occurs
    pass

# Iterate through each URL and perform extraction and analysis
output_data = []
for index, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    # Extract article text
    article_title, article_text = extract_article_text(url)
    with open(f"{url_id}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(article_title+'\n'+ article_text)
    #tokenization
    tk_word= nltk.word_tokenize(article_text)
    #Cleaning using Stop Words Lists
    clean_text=cleaning(tk_word)
    #Creating a dictionary of Positive and Negative words
    fdir=dir(clean_text,positive_words,negative_words)
    #text_analysis_results
    text_analysis_results = perform_text_analysis(clean_text,fdir)
    # Append results to output_data
    output_data.append([url_id, url, article_title, article_text , text_analysis_results])

# Create DataFrame for output
text_analysis_variables=['positive_score', 'negative_score', 'polarity_Score', 'subjectivity_score', 
                'avg_sentence_length', 'percentage_complex_words', 'fog_index', 
                'avg_words_per_sentence',' complex_word_count','Count', 
                'countsyll', 'count_pp', 'avg_word_length']
output_columns = ['URL_ID', 'Article_Title', 'Article_Text'] + text_analysis_variables
output_df = pd.DataFrame(output_data, columns=output_columns)

# Write output to Excel or CSV file
output_df.to_excel("Output.xlsx", index=False)  # or output_df.to_csv("Output.csv", index=False)

