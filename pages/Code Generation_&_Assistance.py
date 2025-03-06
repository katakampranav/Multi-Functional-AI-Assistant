import streamlit as st
import os
from dotenv import load_dotenv
from together import Together
from google import genai

# Load environment variables
load_dotenv()
TOGETHER_AI_API = os.getenv("TOGETHER_AI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_model(model, query, persona="Professional"):
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
            messages=[{"role": "user", "content": prompt_prefix + "\n\n" + query}]
        )
        return response.choices[0].message.content

    elif model == "Google Gemini":
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt_prefix + "\n\n" + query
        )
        return response.text

    elif model == "Deepseek":
        client = Together(api_key=TOGETHER_AI_API)
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            messages=[{"role": "user", "content": prompt_prefix + "\n\n" + query}]
        )
        return response.choices[0].message.content

# Initialize session state
def code_generation_initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about Python code 🤖"]
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hello!!"]

# Function to clear session state
def clear_chat_history():
    st.session_state['history'] = []
    st.session_state['generated'] = ["Hello! Ask me anything about Python code 🤖"]
    st.session_state['past'] = ["Hello!!"]

# Function to generate clean Python code
def generate_code(model, query, persona):
    if query:
        
        code = call_model(model, f"""You are a highly skilled Python code generator. Your task is to produce clean, efficient, and directly executable Python code based on the user's request.

        Instructions:
        1. Understand the user's request precisely.
        2. Generate the complete Python code to fulfill the request.
        3. Provide **only** the Python code. Do not include any explanations, comments, docstrings, or example usage.
        4. The code should be self-contained and ready to run.
        
        User Request: {query}
        """, persona=persona)
        final_code = code.replace("```python", "").replace("```", "").strip()
        return final_code

# Function to handle chat between the user and the model
def code_generation_conversation_chat(query, model, persona):
    result = generate_code(model, query, persona)
    st.session_state['past'].append(query)
    st.session_state['generated'].append(result)
    return result

# Function to display chat interface
def code_generation_display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("Ask your programming question or request Python code:", key='input')
            submit_button = st.form_submit_button(label='Generate/Assist with Code')

        if submit_button and user_input:
            with st.spinner('Generating code...'):
                output = code_generation_conversation_chat(user_input, st.session_state['model'], st.session_state['persona'])

    if 'generated' in st.session_state and st.session_state['generated']:
        with reply_container:
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
                                <div style="margin-top: 10px;">
                                    AI Response:
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                st.code(st.session_state['generated'][i], language="python")

# Main function
def main():
    st.set_page_config(page_title='Code Generation & Assistance')
    st.sidebar.title("AI Assistant Configuration")
    st.session_state['model'] = st.sidebar.selectbox("Select Model", ["LLama 3.3 Meta", "Google Gemini", "Deepseek"], index=0)
    st.session_state['persona'] = st.sidebar.selectbox("Select Persona", ["Professional", "Technical", "Casual"], index=0)
    
    st.title('Code Generation & Assistance')
    st.write('Ask for Python code generation or assistance with code snippets.')
    st.divider()
    
    code_generation_initialize_session_state()
    code_generation_display_chat_history()
    
    if st.button('Clear Chat History'):
        clear_chat_history()

if __name__ == '__main__':
    main()
