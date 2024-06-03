import streamlit as st
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt

# Function to process text data
def process_text(text, max_words=50, text_case='Lower case'):
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Count word frequency
    word_freq = Counter(filtered_tokens)
    
    # Convert to lowercase or uppercase based on text_case
    if text_case == 'Lower case':
        word_freq = {word.lower(): freq for word, freq in word_freq.items()}
    elif text_case == 'Upper case':
        word_freq = {word.upper(): freq for word, freq in word_freq.items()}
    
    # Sort words by frequency and select top words
    word_freq = dict(sorted(word_freq.items(), key=lambda item: item[1], reverse=True)[:max_words])
    
    return word_freq

# Function to generate word cloud
def generate_wordcloud(word_freq, text_color='black', bg_color='white'):
    wordcloud = WordCloud(width=800, height=400, background_color=bg_color, colormap='viridis', color_func=lambda *args, **kwargs: text_color)
    wordcloud.generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

# Main function
def main():
    st.title("Word Cloud Generator")

    st.sidebar.header("Settings")
    max_words = st.sidebar.slider("Number of words", min_value=5, max_value=100, step=5, value=50)
    text_color_option = st.sidebar.selectbox("Text color", ["Black on White", "Colorful"])
    text_case_option = st.sidebar.selectbox("Text case", ["Lower case", "Upper case"])

    text_input = st.text_area("Enter or upload your text data", height=200)

    if st.button("Generate Word Cloud"):
        word_freq = process_text(text_input, max_words, text_case_option)
        text_color = 'black'
        bg_color = 'white'
        if text_color_option == "Colorful":
            text_color = None
        generate_wordcloud(word_freq, text_color, bg_color)

if __name__ == "__main__":
    main()
