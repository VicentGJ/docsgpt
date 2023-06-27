import io, textract, tempfile, os
import ai21
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from docx import Document
from googletrans import Translator


def get_text_from_file(file):
    text = ""

    # If the file is a PDF, use the PyPDF2 library to extract the text
    if file.type == "application/pdf":
        text = get_pdf_text(file)
    else:
        # Other formats allowed by textract: doc, docx, eml, epub, html, json, rtf, txt, odt
        # TODO Test all the textract formats

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            # Write the uploaded file data to the temporary file
            temp.write(file.read())
            # Get the path of the temporary file
            temp_path = temp.name

        # Extract the text from the temporary file
        text = extract_text(temp_path)

        # Delete the temporary file
        os.remove(temp_path)

    return text


def get_pdf_text(pdf):
    text = ""
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


def get_text_segments(source: str, sourceType: str) -> list[str]:
    """
    The parameter sourceType must be "TEXT" or "URL"
    """
    segments = []
    texts: list[str] = [source]
    i = 0

    while sourceType == "TEXT" and i < len(texts):
        if len(texts[i]) > 100000:
            middle_index = int(len(texts[i]) / 2)
            first_half = texts[i][:middle_index]
            second_half = texts[i][middle_index:]
            index = texts.index(texts[i])
            texts.remove(texts[i])
            texts.insert(index, second_half)
            texts.insert(index, first_half)
        else:
            i += 1

    for text in texts:
        response = ai21.Segmentation.execute(
            source=text,
            sourceType=sourceType
        )
        segments_list = response["segments"]
        for dict in segments_list:
            segments.append(dict['segmentText'])

    return segments


def get_text_from_path(path: str) -> str:
    text = ""
    if path.endswith(".pdf"):
        text = get_pdf_text(path)
    else:
        text = extract_text(path)

    return text


def extract_text(file_path: str) -> str:
    """
    Extracts text from a file at the given path.
    """

    # Determine the file extension
    extension = file_path.split('.')[-1]
    # Extract the text from the temporary file using textract
    text = textract.process(file_path, extension=extension).decode('utf-8')
    return text


def translate_text(text: str, dest: str) -> str:
    trans = Translator()
    resp = trans.translate(text=text, dest=dest)
    return resp.text


def detect_text_language(text: str) -> str:
    trans = Translator()
    return trans.detect(text).lang
