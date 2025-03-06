import streamlit as st
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain import FAISS
from pypdf import PdfReader
from docx import Document
from together import Together
from dotenv import load_dotenv

# Initialize session state for conversation history
def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about your document 🤗"]
    
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hello!!"]  # Initialize past


# Function to handle chat between the user and the model
def conversation_chat(query, knowledgebase):
    result = answer_query_from_document(query, knowledgebase)
    
    # Append the query and result to session state
    st.session_state['past'].append(query)  # Add query to past
    st.session_state['generated'].append(result)  # Add result to generated
    
    return result

# Function to display the chat interface
def display_chat_history(knowledgebase):
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Ask a Question", placeholder="Ask about your document", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            with st.spinner('Generating response...'):
                output = conversation_chat(user_input, knowledgebase)

    if st.session_state['generated']:
        with reply_container:
            # Get the number of messages to display, based on the length of the shorter list
            num_messages = min(len(st.session_state['generated']), len(st.session_state['past']))
            
            for i in range(num_messages):
                st.markdown(f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                            <div style="max-width: 70%; background-color: #262730; padding: 10px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                                {st.session_state['past'][i]}
                            </div>
                            <div style="border-radius: 50%; background-color: #262730; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-left: 10px;">
                                🧑‍💼
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                            <div style="border-radius: 50%; background-color: #262730; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                🤖
                            </div>
                            <div style="max-width: 70%; background-color: #262730; padding: 10px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                                {st.session_state['generated'][i]}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)


# Main function to handle document upload and start conversation
def main():
    st.set_page_config(page_title='Document Q&A with RAG')

    st.title('Document Q&A with RAG Concept')
    st.write('Upload a document (PDF, DOCX, TXT) and ask questions related to it. The AI will retrieve relevant sections from the document and generate answers based on it.')
    st.divider()
    
    uploaded_file = st.file_uploader('Upload your Document', type=['pdf', 'docx', 'txt'])
    
    if uploaded_file:
        # Extract text from the uploaded file based on its type
        text = extract_text_from_file(uploaded_file)
        
        # Process the text to create the knowledgebase (embeddings + FAISS index)
        knowledgebase = process_text(text)
        
        # Initialize session state and start conversation
        initialize_session_state()
        display_chat_history(knowledgebase)

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
    # Split the text into smaller chunks for embedding
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Create embeddings for each chunk using HuggingFace BGE embeddings
    embeddings = HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Store the chunks and their embeddings in a FAISS index
    knowledgebase = FAISS.from_texts(chunks, embeddings)

    return knowledgebase

def answer_query_from_document(query, knowledgebase):
    # Perform a similarity search to find the most relevant chunks for the given query
    docs = knowledgebase.similarity_search(query, k=3)  # Retrieve top 3 relevant chunks

    # Combine the retrieved chunks into a context for the LLM
    context = "\n\n".join([doc.page_content for doc in docs])

    # Prepare the prompt for LLM, providing context to answer the query
    prompt = f"Answer the following question based on the provided context:\n\n{context}\n\nQuestion: {query}"

    # Load environment variables
    load_dotenv()
    TOGETHER_AI_API = os.getenv("TOGETHER_AI_API_KEY")

    # Initialize Together API client
    client = Together(api_key=TOGETHER_AI_API)

    # Send the prompt to the Llama 3.3 model for generating an answer
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # Return the response generated by the model
    return response.choices[0].message.content

if __name__ == '__main__':
    main()
