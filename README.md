# Multi-Functional AI Assistant

## 🚀 Overview
The **Multi-Functional AI Assistant** is an AI-powered tool that integrates **LLMs (Large Language Models)** with **Natural Language Processing (NLP)** functionalities, **RAG-based document retrieval**, and a conversational interface using **Streamlit**. It allows users to perform various tasks like text summarization, sentiment analysis, named entity recognition (NER), question answering, and code generation.

## ✨ Features
- **Text Summarization**: Generates concise summaries of long texts or uploaded documents.
- **Sentiment Analysis**: Determines the sentiment of a given text (positive, negative, or neutral).
- **Named Entity Recognition (NER)**: Extracts key entities from the text.
- **Question Answering**:
  - **Generative QA**: Provides AI-generated answers based on the input query.
  - **RAG-Based QA**: Retrieves relevant answers from uploaded documents using **FAISS** (vector-based search).
- **Code Generation & Assistance**: Generates code snippets and provides programming assistance.
- **Multi-Turn Chat**: Enables conversational AI with persona switching.
- **LLM Switching**: Supports dynamic selection between **Gemini, DeepSeek, LLaMA, and Hugging Face models**.
- **Document Upload & Processing**: Supports PDF, DOCX, and TXT file uploads for text extraction and summarization.

## 🏗️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: LLM APIs (Google Gemini, Together AI, DeepSeek, Hugging Face)
- **Vector Database**: FAISS (for document-based Q&A)
- **Libraries Used**:
  - `langchain` (Text processing & chunking)
  - `PyMuPDF` (PDF extraction)
  - `python-docx` (DOCX extraction)
  - `together` (LLama3 & DeepSeek API)
  - `google.generativeai` (Gemini API)

## 🛠️ Setup Instructions
### Prerequisites
Ensure you have the following installed:
- Python (>= 3.8)
- `pip` (Python package manager)
- API Keys for:
  - **Together AI**: For LLaMA & DeepSeek models
  - **Google Gemini**: For Gemini LLM access

### Installation Steps
#### 1️⃣ Clone the Repository
```sh
git clone https://github.com/katakampranav/Multi-Functional-AI-Assistant.git
```

#### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

#### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

#### 4️⃣ Set Up API Keys
Create a **.env** file in the project root and add the required API keys:
```
TOGETHER_AI_API_KEY=your_together_ai_api_key
GEMINI_API_KEY=your_google_gemini_api_key
```

#### 5️⃣ Run the Application
```sh
streamlit run app.py
```

## 📌 Usage
1. **Open the Streamlit UI** in your browser after running the application.
2. **Select a task** from the available options:
   - Text Summarization
   - Sentiment Analysis
   - Named Entity Recognition
   - Question Answering (Generative or RAG-based)
   - Code Generation & Assistance
3. **Upload a document or enter text** as input.
4. **Choose an LLM model** (Gemini, DeepSeek, LLaMA, or Hugging Face).
5. **Click 'Run'** to execute the selected task and get results.

## 🛠️ Workflow of the Project

1. **User Interface (UI) Initialization**:
   - When the user runs the Streamlit app, they are presented with an interactive UI consisting of multiple task cards, allowing them to choose a task such as Text Summarization, Sentiment Analysis, or Code Generation.
   
2. **Task Selection**:
   - The user selects a task they wish to perform (e.g., Text Summarization). Depending on the task, they can either input text manually or upload a document (PDF, DOCX, TXT).
   
3. **Document or Text Processing**:
   - For document uploads, the system uses tools like **PyMuPDF** or `python-docx` to extract text from the uploaded file. Text input is passed directly into the NLP pipelines.
   
4. **LLM Selection**:
   - The user can choose the language model to use for processing the input. Available models include **Gemini**, **DeepSeek**, **LLaMA**, and **Hugging Face**. Each model is responsible for performing the NLP task the user selected.

5. **Task Execution**:
   - The assistant processes the user input according to the selected task:
     - **Text Summarization**: Summarizes the input text using the chosen LLM.
     - **Sentiment Analysis**: Analyzes the sentiment of the input text.
     - **Named Entity Recognition**: Identifies and extracts entities (names, dates, etc.) from the text.
     - **Question Answering (QA)**: Uses **Generative QA** for model-based answers or **RAG-based QA** for retrieving answers from documents using **FAISS**.
     - **Code Generation**: Provides code snippets based on the task or input.
   
6. **Response Generation**:
   - Once the task is executed, the model generates the corresponding output (summary, sentiment result, entities, answers, or code).
   
7. **Output Display**:
   - The result is displayed on the UI for the user. The output can be in the form of text, a summary, a list of entities, or code, depending on the task.

8. **Multi-Turn Interaction**:
   - The system supports multi-turn conversations, where the user can ask follow-up questions or modify inputs for further processing without having to reload the page.
  
## Architecture
![Image](https://github.com/user-attachments/assets/786435c4-a221-4fcc-91c4-8628a76f087b)


## 📬 Contact
For questions or collaboration, feel free to reach out:
- **GitHub**: [katakamprana](https://github.com/katakamprana)
- **Email**: katakampranavshankar@gmail.com
