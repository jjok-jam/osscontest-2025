#!/usr/bin/env python3
"""
종합 건강 분석 API 테스트 스크립트
여러 제품의 바코드와 건강 프로필을 받아 종합적인 건강 분석을 수행하는 API를 테스트합니다.
"""

import requests
import json
import time

# API 기본 URL
BASE_URL = "http://localhost:6318"


def test_comprehensive_analysis():
    """종합 건강 분석 API 테스트"""

    # 테스트 데이터
    test_cases = [
        {
            "name": "고혈압/당뇨병 환자 테스트",
            "products_data": [
                {
                    "code": "20267605",
                    "product_name": "Cashewkerne",
                    "brands": "Alesto, Lidl",
                    "nutriments": {
                        "fat_100g": 47.6,
                        "saturated-fat_100g": 9,
                        "sugars_100g": 6.5,
                        "salt_100g": 0.02,
                    },
                    "allergens_tags": ["견과류"],
                    "food_groups_tags": ["식물성 간식", "견과류"],
                    "nutriscore_grade": "b",
                    "nutrient_levels": {
                        "fat": "high",
                        "saturated-fat": "high",
                        "sugars": "moderate",
                        "salt": "low",
                    },
                    "ingredients": [{"text": "캐슈너트", "percent_estimate": 100}],
                    "serving_size": "30 g",
                    "quantity": "200g",
                    "image_url": "https://images.openfoodfacts.org/images/products/000/002/026/7605/front_en.470.400.jpg",
                },
                {
                    "code": "3017620422003",
                    "product_name": "Nutella",
                    "brands": "Ferrero",
                    "nutriments": {
                        "fat_100g": 30.9,
                        "saturated-fat_100g": 10.6,
                        "sugars_100g": 56.3,
                        "salt_100g": 0.107,
                    },
                    "allergens_tags": ["우유", "견과류", "대두"],
                    "food_groups_tags": ["당류 간식", "사탕류"],
                    "nutriscore_grade": "e",
                    "nutrient_levels": {
                        "fat": "high",
                        "saturated-fat": "high",
                        "sugars": "high",
                        "salt": "low",
                    },
                    "ingredients": [
                        {"text": "Sucre", "percent_estimate": 38.35},
                        {"text": "huile de palme", "percent_estimate": 24.75},
                        {"text": "NOISETTES", "percent_estimate": 13},
                        {"text": "cacao maigre", "percent_estimate": 7.4},
                        {"text": "LAIT écrémé en poudre", "percent_estimate": 6.6},
                    ],
                    "serving_size": "15 g",
                    "quantity": "400 g",
                    "image_url": "https://images.openfoodfacts.org/images/products/301/762/042/2003/front_en.633.400.jpg",
                },
            ],
            "health_profile": {
                "name": "박영수",
                "job": "회사원",
                "notes": "고도비만",
                "gender": "남",
                "birth_year": 1985,
                "weight": 95,
                "height": 175,
                "activity_level": "보통",
                "has_diabetes": "예",
                "has_hypertension": "예",
                "systolic_bp": "160",
                "diastolic_bp": "100",
                "has_allergies": "아니오",
                "selected_allergies": "",
            },
        },
        {
            "name": "알레르기 환자 테스트",
            "products_data": [
                {
                    "code": "20267605",
                    "product_name": "Cashewkerne",
                    "brands": "Alesto, Lidl",
                    "nutriments": {
                        "fat_100g": 47.6,
                        "saturated-fat_100g": 9,
                        "sugars_100g": 6.5,
                        "salt_100g": 0.02,
                    },
                    "allergens_tags": ["견과류"],
                    "food_groups_tags": ["식물성 간식", "견과류"],
                    "nutriscore_grade": "b",
                    "nutrient_levels": {
                        "fat": "high",
                        "saturated-fat": "high",
                        "sugars": "moderate",
                        "salt": "low",
                    },
                    "ingredients": [{"text": "캐슈너트", "percent_estimate": 100}],
                    "serving_size": "30 g",
                    "quantity": "200g",
                },
                {
                    "code": "3017620422003",
                    "product_name": "Nutella",
                    "brands": "Ferrero",
                    "nutriments": {
                        "fat_100g": 30.9,
                        "saturated-fat_100g": 10.6,
                        "sugars_100g": 56.3,
                        "salt_100g": 0.107,
                    },
                    "allergens_tags": ["우유", "견과류", "대두"],
                    "food_groups_tags": ["당류 간식", "사탕류"],
                    "nutriscore_grade": "e",
                    "nutrient_levels": {
                        "fat": "high",
                        "saturated-fat": "high",
                        "sugars": "high",
                        "salt": "low",
                    },
                    "ingredients": [
                        {"text": "Sucre", "percent_estimate": 38.35},
                        {"text": "huile de palme", "percent_estimate": 24.75},
                        {"text": "NOISETTES", "percent_estimate": 13},
                    ],
                    "serving_size": "15 g",
                    "quantity": "400 g",
                },
                {
                    "code": "5000159407236",
                    "product_name": "Mars",
                    "brands": "Mars, Mars Wrigley",
                    "nutriments": {
                        "fat_100g": 17.2,
                        "saturated-fat_100g": 8.6,
                        "sugars_100g": 71.2,
                        "salt_100g": 0.2,
                    },
                    "allergens_tags": ["우유", "대두"],
                    "food_groups_tags": ["당류 간식", "사탕류"],
                    "nutriscore_grade": "e",
                    "nutrient_levels": {
                        "fat": "moderate",
                        "saturated-fat": "high",
                        "sugars": "high",
                        "salt": "low",
                    },
                    "ingredients": [
                        {"text": "sugar", "percent_estimate": 50},
                        {"text": "glucose syrup", "percent_estimate": 20},
                        {"text": "milk", "percent_estimate": 15},
                    ],
                    "serving_size": "51 g",
                    "quantity": "51g",
                },
            ],
            "health_profile": {
                "name": "김미영",
                "job": "주부",
                "notes": "정상체중",
                "gender": "여",
                "birth_year": 1990,
                "weight": 55,
                "height": 160,
                "activity_level": "보통",
                "has_diabetes": "아니오",
                "has_hypertension": "아니오",
                "systolic_bp": "110",
                "diastolic_bp": "70",
                "has_allergies": "예",
                "selected_allergies": "우유,대두",
            },
        },
        {
            "name": "정상 성인 테스트",
            "products_data": [
                {
                    "code": "20267605",
                    "product_name": "Cashewkerne",
                    "brands": "Alesto, Lidl",
                    "nutriments": {
                        "fat_100g": 47.6,
                        "saturated-fat_100g": 9,
                        "sugars_100g": 6.5,
                        "salt_100g": 0.02,
                    },
                    "allergens_tags": ["견과류"],
                    "food_groups_tags": ["식물성 간식", "견과류"],
                    "nutriscore_grade": "b",
                    "nutrient_levels": {
                        "fat": "high",
                        "saturated-fat": "high",
                        "sugars": "moderate",
                        "salt": "low",
                    },
                    "ingredients": [{"text": "캐슈너트", "percent_estimate": 100}],
                    "serving_size": "30 g",
                    "quantity": "200g",
                },
                {
                    "code": "5000159407236",
                    "product_name": "Mars",
                    "brands": "Mars, Mars Wrigley",
                    "nutriments": {
                        "fat_100g": 17.2,
                        "saturated-fat_100g": 8.6,
                        "sugars_100g": 71.2,
                        "salt_100g": 0.2,
                    },
                    "allergens_tags": ["우유", "대두"],
                    "food_groups_tags": ["당류 간식", "사탕류"],
                    "nutriscore_grade": "e",
                    "nutrient_levels": {
                        "fat": "moderate",
                        "saturated-fat": "high",
                        "sugars": "high",
                        "salt": "low",
                    },
                    "ingredients": [
                        {"text": "sugar", "percent_estimate": 50},
                        {"text": "glucose syrup", "percent_estimate": 20},
                        {"text": "milk", "percent_estimate": 15},
                    ],
                    "serving_size": "51 g",
                    "quantity": "51g",
                },
            ],
            "health_profile": {
                "name": "이철수",
                "job": "학생",
                "notes": "정상체중",
                "gender": "남",
                "birth_year": 2000,
                "weight": 70,
                "height": 175,
                "activity_level": "활동적",
                "has_diabetes": "아니오",
                "has_hypertension": "아니오",
                "systolic_bp": "120",
                "diastolic_bp": "80",
                "has_allergies": "아니오",
                "selected_allergies": "",
            },
        },
    ]

    print("🔍 종합 건강 분석 API 테스트 시작")
    print("=" * 60)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 테스트 케이스 {i}: {test_case['name']}")
        print("-" * 40)

        # 요청 데이터 준비
        request_data = {
            "products_data": test_case["products_data"],
            "health_profile": test_case["health_profile"],
        }
        product_count = len(test_case["products_data"])

        print(f"📦 분석할 제품 수: {product_count}개")
        print(
            f"🏥 건강 프로필: {test_case['health_profile']['name']} ({test_case['health_profile']['gender']}, {test_case['health_profile']['birth_year']}년생)"
        )
        print(
            f"📊 체중: {test_case['health_profile']['weight']}kg, 키: {test_case['health_profile']['height']}cm"
        )

        try:
            # API 호출
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/comprehensive-analysis",
                headers={"Content-Type": "application/json"},
                json=request_data,
                timeout=30,
            )
            end_time = time.time()

            print(f"⏱️  응답 시간: {end_time - start_time:.2f}초")

            if response.status_code == 200:
                result = response.json()

                if result.get("success"):
                    data = result.get("data", {})

                    print(f"✅ 성공!")
                    print(f"📊 분석된 제품: {data.get('analyzed_products')}개")
                    print(f"📋 요청한 제품: {data.get('total_requested')}개")

                    if data.get("failed_products"):
                        print(f"❌ 실패한 제품: {data.get('failed_products')}")

                    print("\n📋 분석된 제품 목록:")
                    for product in data.get("products_summary", []):
                        print(
                            f"  - {product.get('name')} ({product.get('barcode')}) - {product.get('brands')}"
                        )

                    print(f"\n💡 종합 건강 분석 결과:")
                    analysis = data.get("comprehensive_analysis", "")
                    # 분석 결과를 줄바꿈으로 구분하여 출력
                    for line in analysis.split("\n"):
                        if line.strip():
                            print(f"  {line}")

                else:
                    print(f"❌ API 오류: {result.get('error', '알 수 없는 오류')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
                print(f"응답 내용: {response.text}")

        except requests.exceptions.Timeout:
            print("❌ 요청 시간 초과")
        except requests.exceptions.ConnectionError:
            print("❌ 연결 오류 - Flask 앱이 실행 중인지 확인하세요")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {str(e)}")

        print("\n" + "=" * 60)

        # 테스트 간 간격
        if i < len(test_cases):
            print("⏳ 다음 테스트까지 2초 대기...")
            time.sleep(2)


def test_error_cases():
    """에러 케이스 테스트"""

    print("\n🚨 에러 케이스 테스트")
    print("=" * 60)

    error_cases = [
        {
            "name": "제품 데이터 없음",
            "data": {
                "health_profile": {
                    "name": "테스트",
                    "gender": "남",
                    "birth_year": 1990,
                    "weight": 70,
                    "height": 175,
                }
            },
        },
        {
            "name": "건강 프로필 없음",
            "data": {
                "products_data": [
                    {
                        "code": "20267605",
                        "product_name": "Test Product",
                        "brands": "Test Brand",
                    }
                ]
            },
        },
        {
            "name": "너무 많은 제품",
            "data": {
                "products_data": [{"code": "20267605", "product_name": "Test"}]
                * 15,  # 15개 제품
                "health_profile": {
                    "name": "테스트",
                    "gender": "남",
                    "birth_year": 1990,
                    "weight": 70,
                    "height": 175,
                },
            },
        },
    ]

    for i, test_case in enumerate(error_cases, 1):
        print(f"\n📋 에러 테스트 {i}: {test_case['name']}")
        print("-" * 40)

        try:
            response = requests.post(
                f"{BASE_URL}/comprehensive-analysis",
                headers={"Content-Type": "application/json"},
                json=test_case["data"],
                timeout=10,
            )

            result = response.json()
            print(f"📊 상태 코드: {response.status_code}")
            print(f"📋 응답: {result.get('error', '알 수 없는 오류')}")

        except Exception as e:
            print(f"❌ 예상치 못한 오류: {str(e)}")

        print("\n" + "-" * 40)


if __name__ == "__main__":
    print("🏥 Label Safe - 종합 건강 분석 API 테스트")
    print("=" * 60)

    # 정상 케이스 테스트
    test_comprehensive_analysis()

    # 에러 케이스 테스트
    test_error_cases()

    print("\n🎉 모든 테스트 완료!")
