import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Sentiment Analysis of Tweets about US Airlines")

DATA_URL = "Tweets.csv"

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.markdown("This project is made by Electro Pi to analyze the sentiment of tweets 🐦 about US airlines ✈️")
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment type', ('positive', 'negative', 'neutral'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])

st.sidebar.markdown("### Number of tweets by sentiment type")
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie Chart'])
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

st.markdown("### Number of tweets by Sentiment")
if select == "Histogram":
    fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
    st.plotly_chart(fig)
else:
    fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
    st.plotly_chart(fig)


st.sidebar.subheader("When and where are the users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]

st.markdown("### Tweets location based on the time of the day")
st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
st.map(modified_data)

if st.sidebar.checkbox("Show raw data", False):
    st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick airlines", ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'))

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_0 = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
                         facet_col='airline_sentiment', labels={'airline_sentiment': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig_0)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for which sentiment?', ('positive', 'negative', 'neutral'))

st.header('Word cloud for %s sentiment' % (word_sentiment))
df = data[data['airline_sentiment'] == word_sentiment]
words = ' '.join(df['text'])
processed_words = ' '.join([word for word in words.split() if 'http' not in word and word.startswith('@') and word != 'RT'])
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=600, width=800).generate(processed_words)
plt.imshow(wordcloud)
plt.xticks([])
plt.yticks([])
st.pyplot()

# Hide "Made with Streamlit" footer
hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)
