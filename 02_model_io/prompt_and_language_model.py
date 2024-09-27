from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# ChatOpenAI 객체를 생성하고 chat에 저장
# OpenAI의 GPT-3.5-turbo 모델을 호출하도록 설정
chat = ChatOpenAI(
    model="gpt-4o-2024-08-06",  # 호출할 모델 지정
)

# PromptTemplate을 생성, 템플릿 안에는 "product"라는 변수가 포함됨
# {product}는 실제 값으로 대체될 자리임
prompt = PromptTemplate(
    template="{product}는 어느 회사에서 개발한 제품인가요？",  # 질문에 "product"라는 변수를 포함
    input_variables=[
        "product"  # "product" 변수를 input으로 받음
    ]
)

# chat 모델에 프롬프트를 보내서 실행
result = chat( 
    [
        # HumanMessage로 템플릿에 "아이폰"을 채워서 실행
        HumanMessage(content=prompt.format(product="아이폰")),
    ]
)

# 결과 출력
print(result.content)
