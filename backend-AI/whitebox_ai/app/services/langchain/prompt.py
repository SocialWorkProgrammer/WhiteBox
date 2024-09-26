from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 환경 설정
load_dotenv()

# ChatGPT API 생성
llm = ChatOpenAI(
    temperature=0.1,  
    model_name="gpt-4", 
)

# 아직 baseline
template = """
당신은 교통사고 전문가입니다. 다음 사고 정보를 바탕으로 사고 상황에 대한 설명과 사용자와 상대차량의 과실 비율에 대한 평가를 해주세요.

사고 정보:
1. 사고 장소 특징: {accident_location}
2. 상대차량의 진행 방향: {a_direction}
3. 사용자의 진행 방향(올린 사람): {b_direction}
4. 상대차량의 과실 비율: {a_percentage}%
5. 사용자의 과실 비율: {b_percentage}%
6. 사고 장소 설명: {accident_location_description}

제공해 주세요:
- 사고 상황에 대한 설명
-  상대차량과 사용자의 과실 비율에 대한 해설
- 유사한 사고에서의 일반적인 법적 기준 또는 관행
"""

prompt = PromptTemplate.from_template(template)


def run_chain(accident_location, a_direction, b_direction, a_percentage, b_percentage, accident_location_description):
    
    formatted_prompt = prompt.format(
        accident_location=accident_location,
        a_direction=a_direction,
        b_direction=b_direction,
        a_percentage=a_percentage,
        b_percentage=b_percentage,
        accident_location_description=accident_location_description
    )

    # chain 실행
    chain = (
        formatted_prompt 
        | llm 
        | JsonOutputParser()
    )

    return chain  
