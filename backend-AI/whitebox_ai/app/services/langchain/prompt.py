from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from dotenv import load_dotenv
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# 캐싱 적용
if not os.path.exists("cache"):
    os.makedirs("cache")

set_llm_cache(SQLiteCache(database_path="cache/llm_cache.db"))

# 환경 설정
load_dotenv()

# 결과물 출력
class Result(BaseModel):
    # 사고 상황, 과실 해설, 최종 결론
    description: str = Field()
    explanation: str = Field()
    Result: str = Field()

# JsonOutputParser를 이용해 결과를 파싱
parser = JsonOutputParser(pydantic_object=Result)

# ChatGPT API 생성
llm = ChatOpenAI(
    temperature=0.1,  
    model_name="gpt-4", 
)

# 프롬프트 템플릿 수정
template = """
당신은 교통사고 전문가입니다. 주어진 사고 정보를 바탕으로 사고 상황을 단계적으로 분석하고, 과실 비율에 대한 평가를 진행해 주세요. 이 과정에서 사고 정보에 대한 사고를 단계적으로 진행하고, 필요할 때 추가적인 설명을 하거나 추론을 통해 결론에 도달합니다.

사고 정보:
1. 사고 장소 특징: {accident_location}
2. 상대차량의 진행 방향: {a_direction}
3. 사용자의 진행 방향(올린 사람): {b_direction}
4. 상대차량의 과실 비율: {a_percentage}%
5. 사용자의 과실 비율: {b_percentage}%
6. 사고 장소 설명: {accident_location_description}

## 단계별 사고 과정:
1. 먼저, 사고 장소 및 차량의 진행 방향에 대한 설명을 바탕으로 사고 발생 상황을 분석하세요.
2. 다음으로, 상대차량과 사용자의 과실 비율을 바탕으로 각각의 책임을 평가하세요. 추가적으로 이 과실 비율에 대한 논리적 근거를 제공하세요.
3. 마지막으로, 유사한 사고에 대한 법적 기준이나 관행을 바탕으로 최종 결론을 도출하세요.

사고 상황을 평가하는 과정에서 각 단계를 설명하고, 논리적으로 사고를 진행해 주세요.

다음 형식으로 응답을 출력해 주세요:

{{
  "description": "<사고 발생 상황 분석>",
  "explanation": "<과실 비율과 그 근거>",
  "Result": "<법적 기준 및 결론>"
}}
"""

# PromptTemplate 생성
prompt = PromptTemplate.from_template(template)

def run_chain(accident_location, a_direction, b_direction, a_percentage, b_percentage, accident_location_description):
    
    # 프롬프트에 사고 정보를 포맷팅
    formatted_prompt = prompt.format(
        accident_location=accident_location,
        a_direction=a_direction,
        b_direction=b_direction,
        a_percentage=a_percentage,
        b_percentage=b_percentage,
        accident_location_description=accident_location_description
    )

    # LLM 실행 후 결과 파싱
    response = llm.invoke(formatted_prompt)  # 모델에 포맷된 프롬프트를 전달하여 결과를 얻음
    
    response_content = response.content  # AIMessage 객체의 content 부분을 가져옴
    result = parser.parse(response_content) 
    
    return result


result = run_chain(
    accident_location="서울시 강남구", 
    a_direction="북쪽", 
    b_direction="남쪽", 
    a_percentage="40", 
    b_percentage="60", 
    accident_location_description="사거리에서 발생한 사고"
)

print(result)