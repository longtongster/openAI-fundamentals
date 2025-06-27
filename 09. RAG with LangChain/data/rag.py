__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import shutil
import getpass
import os

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

openai_api_key = os.environ["OPENAI_API_KEY"]

loader = PyPDFLoader("rag_paper.pdf")
documents = loader.load()
# Split the documents into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_documents = text_splitter.split_documents(documents)

# Initialize the all-MiniLM-L6-v2 embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create a Chroma vector store and embed the chunks
vector_store = Chroma.from_documents(
    documents=chunks, 
    embedding=embedding_model
)

prompt = ChatPromptTemplate.from_template("""
Use the only the context provided to answer the following question. If you don't know the answer, reply that you are unsure.
Context: {context}
Question: {question}
""")

llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini")

# Convert the vector store into a retriever
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})

# Create the LCEL retrieval chain
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Invoke the chain
print(chain.invoke({"question": "Who are the authors?"}))