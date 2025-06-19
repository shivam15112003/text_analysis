# 🔬 Methodology: Web Article Text Analysis Project

---

## 1️⃣ Objective

To build a system that can automatically extract text from online news articles and perform advanced Natural Language Processing (NLP) based text analysis to calculate readability and sentiment metrics.

---

## 2️⃣ Data Collection

* Input URLs are provided in an Excel file (`Input.xlsx`), each having a unique ID.
* The script reads each URL and fetches the full article using `requests` and `BeautifulSoup`.
* Extracted data includes:

  * Article title (from HTML `<title>` tag)
  * Full article body (extracted from `<p>` tags)

---

## 3️⃣ Text Preprocessing

* Tokenization: The full article text is tokenized into words and sentences using NLTK.
* Stopword Removal:

  * Multiple domain-specific stopword files are used (`StopWords_*.txt`), loaded and combined.
  * Stopwords are removed from the tokenized words.
  * The result is a clean word list ready for analysis.

---

## 4️⃣ Sentiment Analysis

* Positive and Negative word lists are loaded from `positive-words.txt` and `negative-words.txt`.
* The cleaned word list is scanned to count occurrences of positive and negative words.
* Sentiment Metrics Calculated:

  * **Positive Score**: Number of positive words.
  * **Negative Score**: Number of negative words.
  * **Polarity Score**:
    $\frac{Positive - Negative}{Positive + Negative + 1e-6}$
  * **Subjectivity Score**:
    $\frac{Positive + Negative}{Total Words + 1e-6}$

---

## 5️⃣ Readability Metrics

* Sentence tokenization allows calculation of sentence length metrics.
* **Average Sentence Length**: Mean number of words per sentence.
* **Complex Word Count**: Words with more than 2 syllables.
* **Percentage of Complex Words**: $\frac{Complex Words}{Total Words}$
* **Fog Index**: $0.4 \times (Average Sentence Length + Percentage of Complex Words)$
* **Average Words Per Sentence**: Total words divided by number of sentences.
* **Average Word Length**: Total characters divided by total words.

---

## 6️⃣ Special NLP Metrics

* **Personal Pronoun Count**: Using regex to count words like `I, we, my, ours, us`.
* **Syllable Count Function**: Custom function using regular expressions to estimate syllables in words.

---

## 7️⃣ Output Generation

* For each URL, the article text is also saved as individual `.txt` files for backup.
* All calculated metrics are compiled into a Pandas DataFrame.
* Final results are exported into `Output.xlsx` file for easy reporting.

---

## 8️⃣ Libraries Used

* **pandas** : Data handling
* **nltk** : Tokenization & NLP processing
* **requests** : Web scraping HTTP requests
* **beautifulsoup4** : HTML parsing
* **re (regex)** : Text pattern matching
* **openpyxl** : Excel output support

---



---

## 👨‍💻 Author

**Shivam Sharma**
