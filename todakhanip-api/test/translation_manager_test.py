#!/usr/bin/env python3
"""
translation_manager의 translate_ingredients_batch 함수 테스트 스크립트
"""

import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.translation_manager import translate_ingredients_batch


def test_translate_ingredients_batch():
    """translate_ingredients_batch 함수 테스트"""

    # 테스트 데이터
    test_barcode = "3017620422003"
    test_ingredients = "Sucre,cacao maigre"

    print("🧪 translate_ingredients_batch 함수 테스트 시작")
    print("=" * 60)
    print(f"📦 바코드: {test_barcode}")
    print(f"🥗 원료: {test_ingredients}")
    print("=" * 60)

    try:
        # 번역 함수 호출
        print("🔄 번역 시작...")
        translations = translate_ingredients_batch(test_barcode, test_ingredients)

        # 결과 출력
        print("\n📊 번역 결과:")
        print("-" * 40)

        if translations:
            print("✅ 번역 성공!")
            for original, korean in translations.items():
                print(f"  {original} → {korean}")

            print(f"\n📈 총 {len(translations)}개 원료 번역 완료")
        else:
            print("❌ 번역 실패 또는 빈 결과")

    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback

        traceback.print_exc()


def test_multiple_barcodes():
    """여러 바코드로 테스트"""

    test_cases = [
        {"barcode": "3017620422003", "ingredients": "Sucre,cacao maigre"},
        {"barcode": "5000159407236", "ingredients": "sugar,flour,milk,eggs"},
        {"barcode": "5000112519945", "ingredients": "water,sugar,carbon dioxide"},
    ]

    print("\n🧪 여러 바코드 테스트 시작")
    print("=" * 60)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📦 테스트 {i}: 바코드 {test_case['barcode']}")
        print(f"🥗 원료: {test_case['ingredients']}")

        try:
            translations = translate_ingredients_batch(
                test_case["barcode"], test_case["ingredients"]
            )

            if translations:
                print("✅ 번역 성공!")
                for original, korean in translations.items():
                    print(f"  {original} → {korean}")
            else:
                print("❌ 번역 실패")

        except Exception as e:
            print(f"❌ 오류: {str(e)}")

        print("-" * 40)


def test_mongodb_cache():
    """MongoDB 캐싱 기능 테스트"""

    test_barcode = "3017620422003"
    test_ingredients = "Sucre,cacao maigre"

    print("\n🧪 MongoDB 캐싱 기능 테스트")
    print("=" * 60)
    print("1️⃣ 첫 번째 호출 (번역 수행)")

    # 첫 번째 호출
    translations1 = translate_ingredients_batch(test_barcode, test_ingredients)

    print("\n2️⃣ 두 번째 호출 (캐시에서 조회)")

    # 두 번째 호출 (캐시에서 조회되어야 함)
    translations2 = translate_ingredients_batch(test_barcode, test_ingredients)

    # 결과 비교
    print("\n📊 결과 비교:")
    print(f"첫 번째 호출 결과: {len(translations1)}개")
    print(f"두 번째 호출 결과: {len(translations2)}개")

    if translations1 == translations2:
        print("✅ 캐싱 기능 정상 작동!")
    else:
        print("❌ 캐싱 기능에 문제가 있습니다.")


if __name__ == "__main__":
    print("🚀 Translation Manager 테스트 시작\n")

    # 기본 테스트
    test_translate_ingredients_batch()

    # 여러 바코드 테스트
    test_multiple_barcodes()

    # 캐싱 기능 테스트
    test_mongodb_cache()

    print("\n🎉 모든 테스트 완료!")
