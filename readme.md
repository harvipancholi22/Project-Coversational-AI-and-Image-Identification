# AI-Powered Document and Image Analysis Tool

This application combines document analysis and image identification capabilities using Streamlit, GEMINI LLM, and PyTorch. It features two main functionalities:
1. PDF Document Q&A using Google's GEMINI LLM
2. Image Classification using ResNet50

## Features

- **PDF Analysis**
  - Upload PDF documents
  - Extract text content
  - Ask questions about the document content
  - Get AI-powered responses using GEMINI LLM

- **Image Identification**
  - Upload images (JPG, JPEG, PNG)
  - Automatic classification using ResNet50
  - Real-time prediction display

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your GEMINI API key:
   - Get your API key from Google AI Studio
   - Replace the `GEMINI_API_KEY` in `main.py` with your actual API key
   - Alternatively, set it as an environment variable:
     ```bash
     # On Windows
     set GEMINI_API_KEY=your_api_key_here
     # On Unix or MacOS
     export GEMINI_API_KEY=your_api_key_here
     ```

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Access the application in your web browser (typically http://localhost:8501)

3. Using the PDF Q&A feature:
   - Upload a PDF file using the file uploader
   - Wait for text extraction to complete
   - Type your question in the text input field
   - View the AI-generated answer

4. Using the Image Identification feature:
   - Switch to the Image Identification tab
   - Upload an image file
   - View the classification result

## Architecture

- **Frontend**: Streamlit web interface
- **PDF Processing**: PyPDF2 for text extraction
- **Image Processing**: 
  - PIL (Python Imaging Library) for image handling
  - ResNet50 pre-trained model for classification
- **AI Integration**: 
  - GEMINI LLM for document question answering
  - PyTorch for image classification

## Security Notes

- Store API keys securely using environment variables in production
- Implement proper input validation and file size limits
- Consider adding user authentication for production use

## Error Handling

The application includes error handling for:
- PDF processing errors
- Image loading and processing issues
- API communication failures
- Invalid file types

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your chosen license here]

## Support

For support, please [create an issue](link-to-issues) in the repository.
