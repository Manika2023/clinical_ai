from langchain.tools import tool
from trials.models import ClinicalTrial
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
import os
from langchain.schema import Document

@tool
def search_trials_db(query: str) -> str:
    '''search clinical trials database'''
    trials = ClinicalTrial.objects.filter(title__icontains=query)
    results = []
    for t in trials:
        results.append(
            f"{t.trial_id}, {t.title}, {t.phase}, {t.status}"
        )

    return "\n".join(results)

@tool
def search_trial_docs(query: str) -> str:
    """Search clinical trial documents using semantic similarity."""
    # embeddings means of converting text to vectors
    embeddings = OpenAIEmbeddings()
    vector_path = "trial_vectors"
    # Create vector DB if it doesn't exist
    if not os.path.exists(vector_path):
        # 1️ Fetch trial records from database
        trials = ClinicalTrial.objects.all()
        # 2️ Convert DB rows → LangChain Documents
        documents = []
        for t in trials:
            content = f"""
            Trial ID: {t.trial_id}
            Title: {t.title}
            Phase: {t.phase}
            Status: {t.status}
            Description: {t.description}
            """
            documents.append(Document(page_content=content))
        # 3️ Split long text into chunks- each chunk is of 1000 characters and each will  share 100 chars by nexxt one
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(documents)
        # 4️ Create FAISS vector store
        vector_store = FAISS.from_documents(docs, embeddings)
        # 5️ Save for future runs
        vector_store.save_local(vector_path)
    #  Otherwise load existing vectors
    else:
        vector_store = FAISS.load_local(vector_path, embeddings)
    # 6️ Similarity search
    results = vector_store.similarity_search(query, k=2)
    return "\n".join(d.page_content for d in results)