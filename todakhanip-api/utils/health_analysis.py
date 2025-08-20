import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from prompts.chat_prompts import (
    HEALTH_EXPERT_SYSTEM_PROMPT,
    HEALTH_PROFILE_ANALYSIS_PROMPT_TEMPLATE,
    COMPREHENSIVE_HEALTH_EXPERT_SYSTEM_PROMPT,
    COMPREHENSIVE_HEALTH_ANALYSIS_PROMPT_TEMPLATE,
    DEFAULT_MODEL,
    DEFAULT_MAX_TOKENS,
    COMPREHENSIVE_MAX_TOKENS,
)

# Load environment variables
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_health_analysis(product_info, health_profile):
    """
    제품 정보와 건강 프로필을 기반으로 건강 분석을 수행하는 함수

    Args:
        product_info (dict): 제품 정보
        health_profile (dict): 건강 프로필 정보

    Returns:
        str: 건강 분석 결과
    """
    try:
        # 제품 정보를 문자열로 변환
        product_info_str = json.dumps(product_info, ensure_ascii=False, indent=2)
        health_profile_str = json.dumps(health_profile, ensure_ascii=False, indent=2)

        # OpenAI API 호출
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": HEALTH_EXPERT_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": HEALTH_PROFILE_ANALYSIS_PROMPT_TEMPLATE.format(
                        health_profile=health_profile_str, product_info=product_info_str
                    ),
                },
            ],
            max_tokens=DEFAULT_MAX_TOKENS,
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"건강 분석 중 오류 발생: {str(e)}")
        return "건강 분석을 수행하는 중 오류가 발생했습니다."


def get_comprehensive_health_analysis(products_info, health_profile):
    """
    여러 제품 정보와 건강 프로필을 기반으로 종합적인 건강 분석을 수행하는 함수

    Args:
        products_info (list): 제품 정보 리스트
        health_profile (dict): 건강 프로필 정보

    Returns:
        str: 종합 건강 분석 결과
    """
    try:
        # 제품 정보를 문자열로 변환
        products_info_str = json.dumps(products_info, ensure_ascii=False, indent=2)
        health_profile_str = json.dumps(health_profile, ensure_ascii=False, indent=2)

        # OpenAI API 호출
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": COMPREHENSIVE_HEALTH_EXPERT_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": COMPREHENSIVE_HEALTH_ANALYSIS_PROMPT_TEMPLATE.format(
                        health_profile=health_profile_str,
                        products_info=products_info_str,
                    ),
                },
            ],
            max_tokens=COMPREHENSIVE_MAX_TOKENS,
            temperature=0.3,  # 더 일관된 답변을 위해 낮은 temperature 설정
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"종합 건강 분석 중 오류 발생: {str(e)}")
        return "종합 건강 분석을 수행하는 중 오류가 발생했습니다."
