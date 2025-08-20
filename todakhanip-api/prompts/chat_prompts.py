"""
채팅 관련 프롬프트 상수 관리
"""

# 건강 전문가 시스템 프롬프트
HEALTH_EXPERT_SYSTEM_PROMPT = (
    "You are a health expert who evaluates the impact of food on various health conditions. "
    "The person is 44 years old, has a blood pressure of 150, and has diabetes. "
    "Your task is to analyze the nutritional information provided and explain its "
    "effect on this person's health, with a special focus on conditions like high blood pressure, "
    "diabetes, and obesity. You should provide the analysis in Korean."
)

# 종합 건강 전문가 시스템 프롬프트
COMPREHENSIVE_HEALTH_EXPERT_SYSTEM_PROMPT = (
    "You are a comprehensive health expert who analyzes multiple food products and their combined "
    "impact on a person's health. You evaluate nutritional interactions, cumulative effects, "
    "and provide holistic dietary recommendations. You should provide the analysis in Korean "
    "and consider the overall dietary pattern rather than individual products in isolation."
)

# 영양 성분 분석 사용자 프롬프트 템플릿
NUTRITION_ANALYSIS_USER_PROMPT_TEMPLATE = "영양 성분 표: {nutrition_data}"

# 건강 프로필 기반 제품 분석 프롬프트 템플릿
HEALTH_PROFILE_ANALYSIS_PROMPT_TEMPLATE = """
건강 프로필 정보:
{health_profile}

제품 정보:
{product_info}

위의 건강 프로필을 가진 사용자에게 이 제품이 어떤 영향을 미칠지 분석해주세요. 
다음 사항들을 고려하여 한국어로 답변해주세요:

1. 고혈압, 당뇨병, 비만 등 기존 질환에 미치는 영향
2. 알레르기 반응 가능성
3. 체중 관리에 미치는 영향
4. 혈압에 미치는 영향
5. 당뇨병 관리에 미치는 영향
6. 전반적인 건강상 권장사항

분석 결과를 간결하고 이해하기 쉽게 정리해주세요. 답변은 500자 이내로 작성하고, 문장이 중간에 끊어지지 않도록 완성된 형태로 작성해주세요.
"""

# 종합 건강 분석 프롬프트 템플릿
COMPREHENSIVE_HEALTH_ANALYSIS_PROMPT_TEMPLATE = """
건강 프로필 정보:
{health_profile}

제품 정보 목록:
{products_info}

위의 건강 프로필을 가진 사용자가 여러 제품을 함께 섭취할 때의 종합적인 건강 영향을 분석해주세요.
다음 사항들을 고려하여 한국어로 답변해주세요:

1. **영양소 상호작용**: 제품들 간의 영양소 조합이 건강에 미치는 영향
2. **누적 효과**: 여러 제품의 영양소가 합쳐져서 나타나는 효과
3. **균형 분석**: 전체적인 영양 균형과 부족/과다 영양소
4. **건강 위험도**: 기존 질환(고혈압, 당뇨병, 비만 등)에 미치는 종합적 영향
5. **알레르기 위험**: 여러 제품의 알레르기 성분 조합 분석
6. **섭취 권장사항**: 
   - 어떤 제품을 우선적으로 섭취해야 하는지
   - 어떤 제품을 제한하거나 피해야 하는지
   - 대체 식품 추천
7. **일일 영양 목표**: 이 조합으로 하루 영양 요구량 충족도
8. **장기적 건강 영향**: 지속적 섭취 시 예상되는 건강 변화

분석 결과를 체계적이고 실용적으로 정리해주세요. 
답변은 최대 1500자까지 작성 가능하며, 모든 분석 항목을 완전하게 포함하여 
사용자가 쉽게 이해하고 실천할 수 있도록 상세하게 설명해주세요.
"""

# 모델 설정
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_MAX_TOKENS = 500

# 종합 분석용 토큰 설정
COMPREHENSIVE_MAX_TOKENS = 2000
