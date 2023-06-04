import io, textract, tempfile, os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from docx import Document


def get_text(doc):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        # Write the uploaded file data to the temporary file
        temp.write(doc.read())
        # Get the path of the temporary file
        temp_path = temp.name

    # Determine the file extension
    extension = doc.name.split('.')[-1]
    # Extract the text from the temporary file using textract
    text = textract.process(temp_path, extension=extension).decode('utf-8')

    # Delete the temporary file
    os.remove(temp_path)

    return text


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_docx_text(doc):
    # Load the docx file data into a stream
    doc_stream = io.BytesIO(doc.read())
    # Create a Document object from the stream
    document = Document(doc_stream)
    # Extract the text from the document
    text = '\n'.join([para.text for para in document.paragraphs])
    return text


def get_text_chunks(text, chunk_size, chunk_overlap):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)
