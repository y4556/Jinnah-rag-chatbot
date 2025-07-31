import os
import hashlib
import time
import pandas as pd
import fitz  # PyMuPDF
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import DATA_DIR, CHROMA_PATH, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

def get_file_hash(file_path):
    """Generate unique hash for file"""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def is_scanned_pdf(file_path):
    """Check if PDF is image-based (scanned)"""
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            if text.strip():  # If any text found, it's not scanned
                return False
        return True
    except:
        return False

def process_pdfs():
    # Create directories if needed
    os.makedirs("data", exist_ok=True)
    os.makedirs("chroma_db", exist_ok=True)
    
    # Load PDFs from data directory
    pdf_dir = DATA_DIR
    documents = []
    processed_files = []
    failed_files = []
    
    print("📂 Processing PDFs...")
    
    files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    if not files:
        print("No PDFs found in data/ directory")
        return None, None
    
    # Create a table for processing status
    table_data = []
    
    for i, file in enumerate(files):
        file_path = os.path.join(pdf_dir, file)
        file_status = {"File": file, "Status": "Processing...", "Method": "", "Time": ""}
        table_data.append(file_status)
        
        start_time = time.time()
        success = False
        
        try:
            # First try with PyPDFLoader (faster for text-based PDFs)
            if not is_scanned_pdf(file_path):
                try:
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    documents.extend(docs)
                    file_status["Status"] = "Success"
                    file_status["Method"] = "PyPDFLoader"
                    success = True
                except Exception as e:
                    file_status["Status"] = f"PyPDF failed: {str(e)[:30]}"
            
            # If not successful, try UnstructuredPDFLoader
            if not success:
                try:
                    loader = UnstructuredPDFLoader(
                        file_path,
                        strategy="fast",
                        mode="elements"
                    )
                    docs = loader.load()
                    documents.extend(docs)
                    file_status["Status"] = " Success"
                    file_status["Method"] = "UnstructuredPDFLoader"
                    success = True
                except Exception as e:
                    file_status["Status"] = f"Failed: {str(e)[:30]}"
                    failed_files.append(file)
        except Exception as e:
            file_status["Status"] = f"Error: {str(e)[:30]}"
            failed_files.append(file)
        
        if success:
            processed_files.append(file)
        
        processing_time = time.time() - start_time
        file_status["Time"] = f"{processing_time:.1f}s"
        
        # Print progress
        print(f"{i+1}/{len(files)}: {file} - {file_status['Status']}")
    
    if not documents:
        print("No valid documents processed")
        return None, None
    
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} document chunks")
    
    print("Creating vector database...")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Generate unique collection name based on file hashes
    file_hashes = "-".join(sorted([get_file_hash(os.path.join(pdf_dir, f)) for f in processed_files]))
    collection_name = f"jinnah-{file_hashes[:8]}"
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH,
        collection_name=collection_name
    )
    
    print(f" Vector database created: chroma_db/{collection_name}")
    
    if failed_files:
        print(f"Some files failed: {', '.join(failed_files)}")
    
    return vector_db, collection_name

if __name__ == "__main__":
    print("Starting Quaid-e-Azam Document Processing")
    print("=" * 50)
    vector_db, collection_name = process_pdfs()
    
    if vector_db:
        print("\n Processing complete!")
        print(f"Collection name: {collection_name}")
    else:
        print("\nProcessing failed. Check error messages above.")