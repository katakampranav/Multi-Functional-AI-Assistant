import streamlit as st
from PIL import Image

def main():
    st.set_page_config(page_title='Multi-Functional AI Assistant', layout='wide')
    
    # Title with a gradient effect
    st.markdown(
        """
        <h1 style='text-align: center; background: -webkit-linear-gradient(45deg, #ff7eb3, #ff758c, #ff7eb3); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Multi-Functional AI Assistant 🚀
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("""<p style='text-align: center; font-size: 18px;'>
        An AI-powered assistant offering various NLP tasks including summarization, sentiment analysis, entity recognition, and more.
    </p>""", unsafe_allow_html=True)
    
    st.divider()
    
    # Section for tasks
    st.subheader("What This AI Assistant Can Do")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #262730; padding: 20px; border-radius: 10px;">
            <h3 style="color: #ff7eb3;">📄 Text Summarization</h3>
            <p>Generate concise summaries from lengthy text inputs.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #262730; padding: 20px; border-radius: 10px; margin-top: 15px;">
            <h3 style="color: #ff7eb3;">🔍 Named Entity Recognition (NER)</h3>
            <p>Extract entities such as names, locations, and dates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #262730; padding: 20px; border-radius: 10px;">
            <h3 style="color: #ff7eb3;">😊 Sentiment Analysis</h3>
            <p>Classify text sentiment (positive, negative, neutral).</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #262730; padding: 20px; border-radius: 10px; margin-top: 15px;">
            <h3 style="color: #ff7eb3;">🛠️ Code Generation & Assistance</h3>
            <p>Generate or review Python code snippets based on problem statements.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #262730; padding: 20px; border-radius: 10px;">
            <h3 style="color: #ff7eb3;">❓ Question Answering</h3>
            <p>Answer questions based on a provided context.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #262730; padding: 20px; border-radius: 10px; margin-top: 15px;">
            <h3 style="color: #ff7eb3;">📚 RAG Q&A</h3>
            <p>Retrieve and generate answers based on external documents.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Footer
    st.markdown("""<p style='text-align: center; font-size: 16px;'>
        Made with ❤️ for AI enthusiasts.
    </p>""", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()
