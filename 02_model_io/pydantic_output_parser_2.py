#OutputFixingParser를 사용하여 AI 모델이 잘못된 데이터를 반환했을 때, 자동으로 이를 수정할 수 있는 기능을 제공하

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser  # OutputFixingParser를 가져옴 (오류 수정 용도)
from langchain.output_parsers import PydanticOutputParser  # PydanticOutputParser를 가져옴 (Pydantic 모델로 출력 파싱)
from langchain.schema import HumanMessage  # HumanMessage 가져옴 (사용자 메시지를 정의)
from pydantic import BaseModel, Field, validator  # Pydantic 모델과 필드, 검증 기능 가져옴

chat = ChatOpenAI()

class Smartphone(BaseModel):
    release_date: str = Field(description="스마트폰 출시일")
    screen_inches: float = Field(description="스마트폰의 화면 크기(인치)")
    os_installed: str = Field(description="스마트폰에 설치된 OS")
    model_name: str = Field(description="스마트폰 모델명")

    @validator("screen_inches") #Pydantic 모델에서 screen_inches 필드에 대한 유효성 검사 메서드임을 선언합니다.
    def validate_screen_inches(cls, field):
        if field <= 0:
            raise ValueError("Screen inches must be a positive number")
        return field


parser = OutputFixingParser.from_llm(  #← OutputFixingParser를 사용하도록 재작성
    parser=PydanticOutputParser(pydantic_object=Smartphone),  #← parser 설정
    llm=chat  #← 수정에 사용할 언어 모델 설정
)

result = chat([HumanMessage(content="안드로이드 스마트폰 1개를 꼽아주세요"), HumanMessage(content=parser.get_format_instructions())])

parsed_result = parser.parse(result.content)

print(f"모델명: {parsed_result.model_name}")
print(f"화면 크기: {parsed_result.screen_inches}인치")
print(f"OS: {parsed_result.os_installed}")
print(f"스마트폰 출시일: {parsed_result.release_date}")
