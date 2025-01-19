import streamlit as st
import PyPDF2
from PIL import Image
import torch
from torchvision import models, transforms
import google.generativeai as genai
import requests


GEMINI_API_KEY = "AIzaSyBfZx6G70_oodWvCY_O4477nZQhKpMBWoI"
genai.configure(api_key=GEMINI_API_KEY)


@st.cache_resource
def load_model():
    model = models.resnet50(pretrained=True)
    model.eval()
    return model


def preprocess_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),  
        transforms.ToTensor(),        
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225]),
    ])
    return preprocess(image).unsqueeze(0)  


def identify_image(image, model):
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        labels = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching labels: {e}"
    
    image_tensor = preprocess_image(image)
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = outputs.max(1)
    return labels[predicted.item()]


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def query_gemini(context, question):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{question} {context}")
        return response.text
    except Exception as e:
        return f"Error: {e}"


def main():
    st.set_page_config(page_title="AI & Image Identifier", page_icon="🤖", layout="wide")
    
    st.markdown("""
    <h1 style='font-family:Arial, sans-serif; color:#000000; font-weight:bold;'>🎨 Conversational AI and Image Identification</h1>
    """, unsafe_allow_html=True)
    
    st.write("**Explore the power of AI with our interactive tool!**")

    tab1, tab2 = st.tabs([
        "📄 PDF Q&A", "🖼️ Image Identification"])

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #FF7E5F, #feb47b);  /* Gradient background */
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f0f2f6;  /* Light background for tabs */
            border-radius: 5px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #cfe2f3;  /* Hover effect */
        }
        /* Ensuring both tabs have black text and the hover effect */
        .stTabs [data-baseweb="tab"]:nth-child(1) {
            color: black;  /* PDF Q&A text color */
        }
        .stTabs [data-baseweb="tab"]:nth-child(2) {
            color: black;  /* Image Identification text color */
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #cfe2f3;
            color: black;  /* Hover text color remains black */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with tab1:
        st.header("📄 Upload PDF and Ask Questions")
        uploaded_pdf = st.file_uploader("Upload your PDF file", type="pdf")
        
        if uploaded_pdf:
            st.write("🔄 Extracting text from the uploaded PDF...")
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            st.success("✅ Text extracted successfully!")
            
            with st.expander("📜 View Extracted Text (Optional)"):
                st.write(pdf_text)

            st.write("🤔 Now, you can ask questions based on the content of the PDF.")
            question = st.text_input("Type your question here:")
            
            if question:
                st.write("💡 Generating answer using GEMINI LLM...")
                answer = query_gemini(pdf_text, question)
                st.markdown(f"**Answer:** {answer}")

    with tab2:
        st.header("🖼️ Upload an Image for Identification")
        uploaded_image = st.file_uploader("Upload your Image file", type=["jpg", "jpeg", "png"])
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            st.write("🔍 Identifying the image...")
            model = load_model()
            label = identify_image(image, model)
            st.success(f"🏷️ Predicted Label: **{label}**")

if __name__ == "__main__":
    main()
