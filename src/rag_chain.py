import os
from .config import OPENAI_API_KEY
from .prompts import SYNTHESIS_PROMPT

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import logging

# Get the logger
logger = logging.getLogger(__name__)

# --- 1. Load Knowledge Base (PDFs) ---
def load_knowledge_base():
    """
    Loads PDFs from the data/buffett and data/dalio directories,
    assigns metadata (the source), and returns a list of documents.
    """
    logger.info("Loading knowledge base from PDFs...")
    
    # Load Buffett's documents
    buffett_loader = DirectoryLoader(
        "data/buffett/",
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        use_multithreading=True
    )
    buffett_docs = buffett_loader.load()
    # Assign metadata
    for doc in buffett_docs:
        doc.metadata["source"] = "Warren Buffett"
        
    logger.info(f"Loaded {len(buffett_docs)} pages from Buffett's documents.")
    
    # Load Dalio's documents
    dalio_loader = DirectoryLoader(
        "data/dalio/",
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        use_multithreading=True
    )
    dalio_docs = dalio_loader.load()
    # Assign metadata
    for doc in dalio_docs:
        doc.metadata["source"] = "Ray Dalio"
        
    logger.info(f"Loaded {len(dalio_docs)} pages from Dalio's documents.")
    
    return buffett_docs + dalio_docs

# --- 2. Format Documents for Context ---
def format_docs_with_metadata(docs):
    """
    Formats the retrieved documents to include their metadata (source)
    so the LLM knows who said what.
    """
    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'Unknown')}\nSnippet: {doc.page_content}"
        for doc in docs
    )

# --- 3. Create the Full RAG Chain ---
def create_rag_chain():
    """
    This is the main function that builds the end-to-end RAG chain.
    """
    
    # Load the documents
    docs = load_knowledge_base()
    
    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)
    
    logger.info(f"Split documents into {len(splits)} chunks.")
    
    # Create the embedding model
    embedding_model = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model="text-embedding-3-small"
    )
    
    # Create the in-memory vector store
    logger.info("Creating in-memory vector store (ChromaDB)...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding_model
    )
    
    # Create the retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6} # Retrieve 6 relevant chunks
    )
    
    # Define the LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o",
        temperature=0.1 
    )
    
    # Build the RAG chain using LangChain Expression Language (LCEL)
    rag_prompt_runnable = RunnablePassthrough.assign(
        context=(lambda x: format_docs_with_metadata(x["context"]))
    ) | SYNTHESIS_PROMPT
    
    rag_chain = RunnablePassthrough.assign(
        context=(lambda x: retriever.invoke(x["question"]))
    ) | rag_prompt_runnable | llm | StrOutputParser()
    
    return rag_chain