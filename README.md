# 🔖 Web Article Text Analysis

A complete web scraping and text analysis project to extract articles from URLs, clean text, and calculate multiple NLP-based readability and sentiment metrics.

---

## 🚀 Features

* ✅ Automatically fetches articles from URLs.
* ✅ Extracts title and full text using BeautifulSoup.
* ✅ Cleans text using multiple domain-specific stopwords.
* ✅ Calculates:

  * Positive & Negative Score
  * Polarity & Subjectivity Score
  * Average Sentence Length
  * Percentage of Complex Words
  * Fog Index
  * Personal Pronoun Count
  * Average Word Length
* ✅ Saves results to Excel file.

---

## 🗃 Project Files

| File                 | Description                                |
| -------------------- | ------------------------------------------ |
| `text_analysis.py`   | Full Python code for scraping and analysis |
| `Input.xlsx`         | Input file containing list of URLs         |
| `positive-words.txt` | Positive words list                        |
| `negative-words.txt` | Negative words list                        |
| `StopWords_*.txt`    | Stopword lists for different domains       |
| `Output.xlsx`        | Generated output with analysis results     |

---

## 🔧 Installation

Make sure you have Python 3.x installed.
Install the required libraries:

```bash
pip install pandas beautifulsoup4 requests nltk openpyxl
```

> Note: `openpyxl` is required to write Excel output.

Also download NLTK tokenizer resources:

```python
import nltk
nltk.download('punkt')
```

---

## 📂 Input File Format

Input file should be an Excel file named `Input.xlsx` with following columns:

| URL\_ID | URL                                                          |
| ------- | ------------------------------------------------------------ |
| 1       | [https://example.com/article1](https://example.com/article1) |
| 2       | [https://example.com/article2](https://example.com/article2) |
| ...     | ...                                                          |

---

## 🏃‍♂️ How to Run

1️⃣ Place all required files in the same directory.
2️⃣ Run the script:

```bash
python text_analysis.py
```

3️⃣ Output will be saved as `Output.xlsx` containing extracted data and all calculated metrics.

---

## 🔍 Metrics Calculated

* Positive Score
* Negative Score
* Polarity Score
* Subjectivity Score
* Average Sentence Length
* Percentage of Complex Words
* Fog Index
* Average Words Per Sentence
* Complex Word Count
* Word Count
* Personal Pronouns Count
* Average Word Length

---

## 👨‍💻 Author

**Shivam Sharma**
