import json
import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 환경 변수에서 설정 로드
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "label-safe")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "ingredients")

# 번역 파일 경로 전역변수 (환경 변수에서 로드)
TRANSLATION_FILES = {
    "product": os.getenv(
        "TRANSLATION_PRODUCT_FILE", "data/translated/product_translated.json"
    ),
    "food_groups": os.getenv(
        "TRANSLATION_FOOD_GROUPS_FILE", "data/translated/food_groups_translated.json"
    ),
    "allergens": os.getenv(
        "TRANSLATION_ALLERGENS_FILE", "data/translated/allergens_translated.json"
    ),
}

# 번역 데이터를 메모리에 로드
_translation_cache = {}


def load_translation_data():
    """번역 데이터를 메모리에 로드하는 함수"""
    global _translation_cache
    if not _translation_cache:
        try:
            # 각 번역 파일 로드
            for translation_type, file_path in TRANSLATION_FILES.items():
                with open(file_path, "r", encoding="utf-8") as f:
                    translations = json.load(f)
                    _translation_cache[translation_type] = {
                        item["original"]: item["korean"] for item in translations
                    }

            print("✅ 번역 데이터 로드 완료")
        except FileNotFoundError as e:
            print(f"⚠️ 번역 파일을 찾을 수 없습니다: {e}")
            _translation_cache = {"product": {}, "food_groups": {}, "allergens": {}}
        except Exception as e:
            print(f"❌ 번역 데이터 로드 오류: {e}")
            _translation_cache = {"product": {}, "food_groups": {}, "allergens": {}}


def translate_text(text, translation_type):
    """텍스트를 한글로 번역하는 함수"""
    global _translation_cache
    if translation_type in _translation_cache:
        return _translation_cache[translation_type].get(text, text)
    return text


def translate_tags(tags, translation_type):
    """태그 배열을 한글로 번역하는 함수"""
    if not tags:
        return []

    translated_tags = []
    for tag in tags:
        if ":" in tag:
            # ":" 분리하여 [1] 값 사용
            parts = tag.split(":")
            if len(parts) > 1:
                original_text = parts[1]
                translated_text = translate_text(original_text, translation_type)
                translated_tags.append(translated_text)
            else:
                translated_tags.append(tag)
        else:
            # ":" 없는 경우 그대로 사용
            translated_tags.append(tag)

    return translated_tags


def get_translation_cache():
    """번역 캐시 상태 확인 함수"""
    return _translation_cache


def clear_translation_cache():
    """번역 캐시 초기화 함수"""
    global _translation_cache
    _translation_cache = {}
    print("🗑️ 번역 캐시 초기화 완료")


def translate_ingredients_batch(barcode, ingredients_string):
    """
    바코드와 쉼표로 구분된 원료 문자열을 받아 번역하는 함수

    Args:
        barcode (str): 바코드 값
        ingredients_string (str): 쉼표로 구분된 원료 문자열

    Returns:
        dict: {원본: 번역} 형태의 딕셔너리
    """
    try:
        # MongoDB 연결
        from pymongo import MongoClient

        client_mongo = MongoClient(MONGODB_URI)
        db = client_mongo[DB_NAME]
        collection = db[COLLECTION_NAME]

        # 1. MongoDB에서 기존 번역 데이터 확인
        existing_data = collection.find_one({"_id": barcode})
        if existing_data:
            print(f"✅ 바코드 {barcode}의 기존 번역 데이터 사용")
            return existing_data.get("translations", {})

        # 2. 기존 데이터가 없으면 번역 수행
        print(f"🔄 바코드 {barcode}의 원료 번역 시작")

        # 쉼표로 구분된 문자열을 리스트로 변환
        ingredients_list = [
            item.strip() for item in ingredients_string.split(",") if item.strip()
        ]

        if not ingredients_list:
            print(f"⚠️ 바코드 {barcode}: 번역할 원료가 없습니다.")
            return {}

        # OpenAI API로 번역 요청
        ingredients_text = ",".join(ingredients_list)

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 비용 효율적인 모델 사용
            messages=[
                {
                    "role": "system",
                    "content": "당신은 전문 번역가입니다. 주어진 식품 원료 목록을 한국어로 정확하게 번역해주세요. 각 항목을 'original: 원본텍스트, korean: 한국어번역' 형식으로 JSON 배열로 반환해주세요.",
                },
                {
                    "role": "user",
                    "content": f"다음 식품 원료들을 한국어로 번역해주세요:\n\n{ingredients_text}",
                },
            ],
            temperature=0.1,
            max_tokens=4000,
        )

        # 응답에서 JSON 추출
        content = response.choices[0].message.content
        if content is None:
            print(f"❌ 바코드 {barcode}: 빈 응답 받음")
            return {}

        content = content.strip()

        # JSON 파싱
        try:
            # JSON 부분만 추출
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            else:
                json_content = content

            translated_data = json.loads(json_content)

            # 딕셔너리 형태로 변환
            translations_dict = {}
            for item in translated_data:
                if "original" in item and "korean" in item:
                    translations_dict[item["original"]] = item["korean"]

            # 3. MongoDB에 번역 결과 저장
            collection.insert_one(
                {
                    "_id": barcode,
                    "translations": translations_dict,
                    "ingredients_count": len(ingredients_list),
                    "created_at": datetime.datetime.now(),
                }
            )

            print(
                f"✅ 바코드 {barcode}: {len(translations_dict)}개 원료 번역 완료 및 저장"
            )
            return translations_dict

        except json.JSONDecodeError as e:
            print(f"❌ 바코드 {barcode}: JSON 파싱 오류 - {e}")
            return {}
        except Exception as e:
            print(f"❌ 바코드 {barcode}: 번역 오류 - {e}")
            return {}

    except Exception as e:
        print(f"❌ 바코드 {barcode}: 전체 처리 오류 - {e}")
        return {}
    finally:
        # MongoDB 연결 종료
        if "client_mongo" in locals():
            client_mongo.close()
