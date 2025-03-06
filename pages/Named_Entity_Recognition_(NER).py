import streamlit as st
import os
from dotenv import load_dotenv
from together import Together

def main():
    st.set_page_config(page_title='Named Entity Recognition (NER)')

    st.title('Named Entity Recognition (NER)')
    st.write('Extract named entities (names, locations, dates, etc.) from the provided text.')
    st.divider()

    # Text input field for Named Entity Recognition
    input_text = st.text_area("Enter Text for Named Entity Recognition (NER)")

    submit = st.button('Extract Entities')

    if submit:
        entities = extract_entities(input_text)
        st.subheader('Extracted Entities: \n')
        st.write(entities)

def extract_entities(text):
    if text:
        # Load environment variables for API key
        load_dotenv()
        TOGETHER_AI_API = os.getenv("api_key")

        # Initialize Together API client
        client = Together(api_key=TOGETHER_AI_API)

        # Query for Named Entity Recognition (NER)
        query = f'''You are an expert in Named Entity Recognition. Your task is to extract all named entities from the provided text and present them in a structured format, grouped by entity type and enclosed in quotation marks.

        Instructions:
        1.  Analyze the provided text to identify all named entities.
        2.  Group the extracted entities by their respective entity types (e.g., Dates, Persons, Locations, Organizations, etc.).
        3.  For each identified entity type, create a label (e.g., 'Dates:', 'Persons:').
        4.  Enclose each entity in double quotation marks (\").
        5.  Present the entities for each type on the same line, separated by commas.
        6.  If no entities of a specific type are found, omit that type from the output.

        Text: {text}

        Entities:'''

        # Send the query to the Llama model for NER
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": query}]
        )

        # Parse and return the extracted entities
        entities = response.choices[0].message.content.strip()
        return entities

if __name__ == '__main__':
    main()
