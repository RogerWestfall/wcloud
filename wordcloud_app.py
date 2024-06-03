import nltk
nltk.download('punkt')
nltk.download('stopwords')

import streamlit as st
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# Disable PyplotGlobalUse warning
st.set_option('deprecation.showPyplotGlobalUse', False)

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

# Modify the generate_wordcloud function to handle color_func correctly
def generate_wordcloud(word_freq, text_color='black', bg_color='white', color_func=None):
    wordcloud = WordCloud(width=800, height=400, background_color=bg_color, color_func=color_func)
    wordcloud.generate_from_frequencies(word_freq)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

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
        
        if text_color_option == "Black on White":
            text_color = 'black'
            bg_color = 'white'
            color_func = None
        else:
            text_color = None
            bg_color = 'white'
            # Define a custom color function that randomly selects colors
            def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
                h = int(360.0 * np.random.rand())
                s = int(100.0 * np.random.rand())
                l = int(100.0 * np.random.rand())
                return f"hsl({h}, {s}%, {l}%)"
            
            color_func = random_color_func

        fig = generate_wordcloud(word_freq, text_color, bg_color, color_func)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
