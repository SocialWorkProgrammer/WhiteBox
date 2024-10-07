import pickle
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# 환경 변수 로드
load_dotenv()

# OpenAI 임베딩 함수 초기화
embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Chroma 벡터 스토어 초기화
vector_store = Chroma(persist_directory="chroma_data", embedding_function=embedding_function)

# langchainembedding.pickle 파일 경로 설정
embedding_file_path = os.path.join("app", "services", "langchainembedding.pickle")

# 벡터 스토어 초기화 부분 (한 번만 실행)
if not os.path.exists(os.path.join("chroma_data", "index")):
    if not os.path.exists(embedding_file_path):
        print(f"파일을 찾을 수 없습니다: {embedding_file_path}")
    else:
        with open(embedding_file_path, 'rb') as f:
            precedent_embedding_dict = pickle.load(f)

        texts = list(precedent_embedding_dict.keys())
        embeddings = list(precedent_embedding_dict.values())

        # 배치 크기 설정 (5461보다 작은 값으로 설정)
        batch_size = 5000

        try:
            # 텍스트와 임베딩을 배치 단위로 나누어 벡터 스토어에 추가
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = embeddings[i:i + batch_size]
                vector_store.add_texts(texts=batch_texts, embeddings=batch_embeddings)

            # 벡터 스토어에 데이터 저장
            vector_store.persist()
            print("벡터 스토어에 데이터가 성공적으로 추가되었습니다.")
        except Exception as e:
            print(f"벡터 스토어에 텍스트를 추가하는 중 오류가 발생했습니다: {e}")
else:
    print("벡터 스토어가 이미 초기화되어 있습니다.")
