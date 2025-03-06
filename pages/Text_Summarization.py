import streamlit as st
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain import FAISS
from pypdf import PdfReader
from docx import Document
from together import Together
from dotenv import load_dotenv
from google import genai

# Load environment variables (e.g., API keys)
load_dotenv()

TOGETHER_AI_API = os.getenv("TOGETHER_AI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def call_model(model, query, context="", persona="Professional"):
    if persona == "Technical":
        prompt_prefix = "Respond in a highly technical manner with detailed explanations."
    elif persona == "Casual":
        prompt_prefix = "Respond in a casual, friendly tone."
    elif persona == "Professional":
        prompt_prefix = "Respond in a formal, professional tone."
    else:
        prompt_prefix = ""

    if model == "LLama 3.3 Meta":
        client = Together(api_key=TOGETHER_AI_API)
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": prompt_prefix + "\n\n" + query + "\n\n" + context}]
        )
        return response.choices[0].message.content

    elif model == "Google Gemini":
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt_prefix + "\n\n" + query + "\n\n" + context
        )
        return response.text

    elif model == "Deepseek":
        client = Together(api_key=TOGETHER_AI_API)
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            messages=[{"role": "user", "content": prompt_prefix + "\n\n" + query}])
        return response.choices[0].message.content

def main():
    st.set_page_config(page_title='Document Summarizer')

    st.sidebar.markdown("<h1 style='text-align: center; font-size: 2.5em; color: white;'>AI Assistant Configuration</h1>", unsafe_allow_html=True)

    model = st.sidebar.selectbox("Select Model", ["LLama 3.3 Meta", "Google Gemini", "Deepseek"], 
                                index=0, help="Select the LLM model you want to use for processing")

    persona = st.sidebar.selectbox("Select Persona", ["Professional", "Technical", "Casual"], 
                                index=0, help="Choose a response persona for the assistant")

    st.title('Document Summarizer App')
    st.write('Summarize your documents (PDF, DOCX, TXT) in just a few seconds')
    st.divider()
    
    # File uploader for document upload
    uploaded_file = st.file_uploader("Upload a Document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

    # Text area for manual text input
    text_input = st.text_area("Or Enter Text Manually for Summarization")

    if uploaded_file or text_input:
        if st.button("Generate Summary"):
            # Call the summarizer function based on the available input
            summary = summarizer(uploaded_file, text_input, model, persona)
            st.write("Summary:")
            st.write(summary)

# Function to extract text from different document types
def extract_text_from_file(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        return extract_text_from_docx(uploaded_file)
    elif file_extension == "txt":
        return extract_text_from_txt(uploaded_file)
    else:
        st.warning(f"Unsupported file type: {file_extension}")
        return ""

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ''
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_file):
    text = ""
    doc = Document(docx_file)
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

# Function to extract text from a TXT file
def extract_text_from_txt(txt_file):
    text = txt_file.read().decode('utf-8')
    return text

def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    knowledgebase = FAISS.from_texts(chunks, embeddings)

    return knowledgebase

# Summarization function with model selection
def summarizer(uploaded_file=None, text_input=None, model="llama", persona="professional"):
    if uploaded_file:
        # Extract text from the uploaded file
        text = extract_text_from_file(uploaded_file)
    elif text_input:
        # Use the manual text input for summarization
        text = text_input
    else:
        return "Please provide either a document or some text to summarize."

    # Process the extracted text (either from file or text input)
    knowledgebase = process_text(text)

    query = '''You are an advanced AI assistant skilled in document summarization. Your task is to provide a concise, yet informative summary of the provided content and the pdf. The summary should:
    - Highlight the main points and key information.
    - Be clear, structured, and well-organized.
    - Be in a format that is easy to read and understand.
    
    Please focus on summarizing the core ideas and present them in a structured manner without unnecessary repetition.'''

    if query:
        docs = knowledgebase.similarity_search(query)
        context = docs[0].page_content if docs else ""

        # Call the selected model with persona for summarization
        return call_model(model, query, context, persona)

if __name__ == '__main__':
    main()
