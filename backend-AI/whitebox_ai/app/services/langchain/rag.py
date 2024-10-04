import pickle
import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

with open('precedent_embedding_dict.pickle', 'rb') as f:
    precedent_embedding_dict = pickle.load(f)

    # 2. OpenAI 임베딩 함수 설정
embedding_function = OpenAIEmbeddings(openai_api_key= os.getenv("SECRET_KEY"))  


vector_store = Chroma(persist_directory="chroma_data", embedding_function=embedding_function)

for key, embedding in precedent_embedding_dict.items():
    vector_store.add_texts(
        texts=[key],  
        embeddings=[embedding]
    )

vector_store.persist()

def query_similar_terms(query_text):
    results = vector_store.similarity_search(query_text, k=5)
    
    return [result.page_content for result in results]  


query_text = "판례와 관련된 법적 용어"
similar_terms = query_similar_terms(query_text)
print("유사한 5개의 용어:", similar_terms)

