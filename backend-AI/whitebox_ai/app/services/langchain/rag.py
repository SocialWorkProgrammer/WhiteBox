import pickle
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
load_dotenv()

embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

vector_store = Chroma(persist_directory="chroma_data", embedding_function=embedding_function)

embedding_file_path = os.path.join("app", "services", "langchain", "embedding.pickle")

if not os.path.exists(os.path.join("chroma_data", "index")):
    if not os.path.exists(embedding_file_path):
        print(f"파일을 찾을 수 없습니다: {embedding_file_path}")
    else:
        with open(embedding_file_path, 'rb') as f:
            precedent_embedding_dict = pickle.load(f)

        texts = list(precedent_embedding_dict.keys())
        embeddings = list(precedent_embedding_dict.values())

        try:
            vector_store.add_texts(texts=texts, embeddings=embeddings)
            vector_store.persist()
            print("벡터 스토어에 데이터가 성공적으로 추가되었습니다.")
        except Exception as e:
            print(f"벡터 스토어에 텍스트를 추가하는 중 오류가 발생했습니다: {e}")
else:
    print("벡터 스토어가 이미 초기화되어 있습니다.")

def query_similar_terms(query_text):
    try:
        results = vector_store.similarity_search(query_text, k=5)
        return [result.page_content for result in results]
    except Exception as e:
        print(f"유사한 용어를 쿼리하는 중 오류가 발생했습니다: {e}")
        return []
