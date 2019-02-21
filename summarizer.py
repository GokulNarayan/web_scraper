import scraper
import nltk
import string
from nltk.corpus import stopwords
from collections import defaultdict
from heapq import nlargest

completed_texts = []
sentence_tokens = []
word_tokens = []
sentence_ranks = []


def gather_data():
    #user_query = input("what do you want to search?")
    #scraper.find_web_pages(user_query)
    scraper.create_soups()
    scraper.clean_soups()
    completed_texts.extend(scraper.get_pure_texts())


def get_tokenize_info():
    for text in completed_texts:
        if len(text) > 3000:
            s_t, w_t = tokenize_content(text)
            sentence_tokens.append(s_t)
            word_tokens.append(w_t)


def tokenize_content(text):
    stop_words = set(stopwords.words('english')+list(string.punctuation))
    words = nltk.word_tokenize(text.lower())

    return[
        nltk.sent_tokenize(text),
        [word for word in words if word not in stop_words]
    ]


def get_score_info():

    for counter, s_t in enumerate(sentence_tokens):
        sentence_ranks.append(score_tokens(word_tokens[counter], s_t))


def score_tokens(filtered_words, sentences):
    word_freq = nltk.FreqDist(filtered_words)
    ranking = defaultdict(int)

    for i, sentence in enumerate(sentences):
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_freq:
                ranking[i] = word_freq[word]

    return ranking


def print_all_summaries():
    for counter, rank in enumerate(sentence_ranks):
        print(summarize(rank, sentence_tokens[counter], 10)+'\n')


def summarize(rank, sentence, length):
    indexes = nlargest(length, rank, key=rank.get)
    final_summary = [sentence[j] for j in sorted(indexes)]
    return ' '.join(final_summary)
