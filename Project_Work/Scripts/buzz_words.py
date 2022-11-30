import matplotlib.pyplot as plt
import pandas as pd
import wordcloud as wc
import string
import re
import streamlit as st

def get_buzz_words():

    x = pd.read_csv('../Data/Climate_change_tweets.csv')

    word_count = {}
    stop_words = wc.STOPWORDS
    stop_words.add('s')
    stop_words.add('')
    stop_words.add('·')
    for tweet in x['Embedded_text']:
        tweet = re.sub(r'http\S+', '', tweet)
        tweet = re.sub('@[\w]*', '', tweet)
        tweet = re.sub(r'\d+', '', tweet)
        tweet = tweet.lower()
        tweet = tweet.translate(str.maketrans('', '', string.punctuation))
        words = tweet.split()
        for word in words:
            word.translate(str.maketrans('', '', string.punctuation))
            if word in stop_words:
                continue
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

    word_count = sorted(word_count.items(), key=lambda count: count[1], reverse=True)
    word_count = word_count[0:30]  # extract top 30 words
    string_of_words = ''
    for item in word_count:
        string_of_words += ' '
        string_of_words += item[0]
        string_of_words += ' '

    wordcloud = wc.WordCloud(width=500, height=500,
                             background_color='white',
                             stopwords=wc.STOPWORDS,
                             min_font_size=10).generate(string_of_words)

    # plot the WordCloud image
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('../Data/buzz_words.png')
    st.image('../Data/buzz_words.png')
    #plt.show()



