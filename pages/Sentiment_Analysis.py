import streamlit as st
import os
from dotenv import load_dotenv
from together import Together

def main():
    st.set_page_config(page_title='Sentiment Analyzer')

    st.title('Sentiment Analyzer')
    st.write('Classify the sentiment of the provided text (Positive, Negative, Neutral).')
    st.divider()

    # Text input field for sentiment analysis
    input_text = st.text_area("Enter Text for Sentiment Analysis")

    submit = st.button('Analyze Sentiment')

    if submit:
        sentiment = analyze_sentiment(input_text)
        st.subheader('Sentiment: \n')
        st.write(sentiment)

def analyze_sentiment(text):
    if text:
        # Load environment variables for API key
        load_dotenv()
        TOGETHER_AI_API = os.getenv("TOGETHER_AI_API_KEY")

        # Initialize Together API client
        client = Together(api_key=TOGETHER_AI_API)

        # Query for sentiment analysis
        query = f'''You are a sentiment analysis expert. Your task is to analyze the following text and classify its overall sentiment.

        Instructions:
        1. Read the provided text carefully.
        2. Identify the dominant emotional tone.
        3. Classify the sentiment as either positive, negative, or neutral.
        4. **Provide only the sentiment classification (positive, negative, or neutral) without any additional explanation or analysis.**

        Text: {text}

        Sentiment: '''

        # Send the query to the Llama model for sentiment classification
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": query}]
        )

        # Parse and return the sentiment result
        sentiment = response.choices[0].message.content.strip()
        return sentiment

if __name__ == '__main__':
    main()
