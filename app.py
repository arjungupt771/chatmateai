import os
import google.generativeai as genai
import PyPDF2
import streamlit as st

# Set page configuration (title and favicon)
st.set_page_config(page_title="ChatMate AI", page_icon="static/robot.png")

# Configure the Google Generative AI API
genai.configure(api_key='AIzaSyAfBnFjJ-80s7iy71wLVGNh2q3NccSjVo0')  # Replace with your actual API key

# Set generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 100,
    "max_output_tokens": 32768,
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to clear the uploads directory
def clear_uploads_directory(upload_dir="uploads/"):
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove file
        except Exception as e:
            st.error(f"Error removing {file_path}: {str(e)}")

# Streamlit App
def main():
    # Clear the uploads directory when the app is refreshed
    clear_uploads_directory()

    st.title("Welcome to ChatMate AI...")
    st.markdown("Ask, upload, and discover—AI at your service.")
    st.markdown("~ Arjun Gupta", unsafe_allow_html=True)  # Add your portfolio URL here

    # Initialize chat_history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Initialize chat session in session state
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Sidebar for PDF Upload
    st.sidebar.header("Upload PDF Documents")
    pdf_files = st.sidebar.file_uploader("Upload PDFs (Max 10MB each)", type=["pdf"], accept_multiple_files=True)

    # Initialize PDF text variable
    pdf_text = ""

    if pdf_files:
        pdf_texts = []  # Store the extracted text from each PDF
        for pdf_file in pdf_files:
            # Check file size
            if pdf_file.size > 10 * 1024 * 1024:  # 10 MB in bytes
                st.sidebar.error(f"File {pdf_file.name} exceeds 10MB limit. Skipping.")
                continue

            # Save each uploaded PDF temporarily
            pdf_path = os.path.join("uploads", pdf_file.name)
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            # Extract text from the PDF
            extracted_text = extract_text_from_pdf(pdf_path)
            pdf_texts.append(f"--- Text from {pdf_file.name} ---\n{extracted_text}")

        # Combine text from all PDFs
        pdf_text = "\n\n".join(pdf_texts)
        st.sidebar.success(f"Uploaded {len(pdf_texts)} PDF(s) successfully!")

    # Display chat messages from history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0])

    # React to user input
    if prompt := st.chat_input("What is your question?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)

        # Combine user question with the relevant PDF text if available
        context = f"Based on the documents:\n{pdf_text}\n\nUser Question: {prompt}" if pdf_text else prompt

        try:
            # Send the combined context to the generative model
            response = st.session_state.chat_session.send_message(context)

            # Display assistant response in chat message container using the built-in chatbot icon
            st.chat_message("assistant").markdown(response.text)

            # Update chat history
            st.session_state.chat_history.append({"role": "user", "parts": [prompt]})
            st.session_state.chat_history.append({"role": "assistant", "parts": [response.text]})

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
