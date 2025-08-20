import requests
import json

# API 기본 URL
BASE_URL = "http://localhost:6318"


def test_barcode_api():
    """
    바코드 API 테스트 함수
    """
    # 테스트용 바코드
    test_barcode = "20724696"

    print(f"Testing barcode API with barcode: {test_barcode}")

    try:
        # 로컬 서버가 실행 중이라고 가정하고 테스트
        response = requests.get(f"{BASE_URL}/barcode/{test_barcode}")

        if response.status_code == 200:
            data = response.json()
            print("✅ API 호출 성공!")

            # 기본 정보
            print(f"제품명: {data['data']['product_name']}")
            print(f"영문 제품명: {data['data']['product_name_en']}")
            print(f"브랜드: {data['data']['brands']}")
            print(f"바코드: {data['data']['code']}")
            print(f"제품 분류: {data['data']['product_type']}")

            # 중량 정보
            print(
                f"중량: {data['data']['product_quantity']} {data['data']['product_quantity_unit']}"
            )
            print(f"중량 표기: {data['data']['quantity']}")

            # 영양 정보
            print(f"Nutri-Score: {data['data']['nutriscore_grade']}")
            print(f"영양소 수준:")
            for nutrient, level in data["data"]["nutrient_levels"].items():
                print(f"  - {nutrient}: {level}")

            print(f"영양소 함량 (100g당):")
            for nutrient, value in data["data"]["nutriments"].items():
                print(f"  - {nutrient}: {value}")

            # 원재료 정보
            ingredients = data["data"]["ingredients"]
            if ingredients:
                print(f"원재료 개수: {len(ingredients)}개")
                for i, ingredient in enumerate(ingredients, 1):
                    print(f"원재료 {i}: {ingredient['text']}")
                    print(f"  비율: {ingredient['percent_estimate']}%")
                    print(f"  가공 방법: {ingredient['processing']}")
                    print(f"  비건 여부: {ingredient['vegan']}")
                    print(f"  채식주의자 여부: {ingredient['vegetarian']}")
            else:
                print("원재료 정보 없음")

            # 알레르기 정보
            print(
                f"알레르기: {', '.join(data['data']['allergens_tags']) if data['data']['allergens_tags'] else '알레르기 정보 없음'}"
            )

            # 1회 섭취량
            print(
                f"1회 섭취량: {data['data']['serving_quantity']} {data['data']['serving_quantity_unit']}"
            )
            print(f"1회 섭취량 표기: {data['data']['serving_size']}")

            # 이미지 정보
            print(f"제품 이미지: {data['data']['image_url']}")
            print(f"영양 정보 이미지: {data['data']['image_nutrition_url']}")
            print(f"원재료 이미지: {data['data']['image_ingredients_url']}")

            # 국가 정보
            print(
                f"판매 국가: {', '.join(data['data']['countries_tags']) if data['data']['countries_tags'] else '국가 정보 없음'}"
            )

            # 식품 그룹
            print(
                f"식품 그룹: {', '.join(data['data']['food_groups_tags']) if data['data']['food_groups_tags'] else '식품 그룹 정보 없음'}"
            )

        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")


def test_multiple_barcodes():
    """
    여러 바코드로 테스트하는 함수
    """
    test_barcodes = [
        "20724696",  # Almonds
        "3017620422003",  # Nutella
        "5000159407236",  # Snickers
        "5000112519945",  # Coca Cola
    ]

    print("Testing multiple barcodes...")
    print("=" * 50)

    for barcode in test_barcodes:
        print(f"\n🔍 Testing barcode: {barcode}")
        try:
            response = requests.get(f"{BASE_URL}/barcode/{barcode}")

            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    print(f"✅ 성공: {data['data']['product_name']}")
                    print(f"   브랜드: {data['data']['brands']}")
                    print(f"   Nutri-Score: {data['data']['nutriscore_grade']}")
                else:
                    print(f"❌ 실패: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP 에러: {response.status_code}")

        except Exception as e:
            print(f"❌ 예외 발생: {str(e)}")

        print("-" * 30)


if __name__ == "__main__":
    print("🧪 바코드 API 테스트 시작")
    print("=" * 50)

    # 단일 바코드 상세 테스트
    test_barcode_api()

    print("\n" + "=" * 50)

    # 여러 바코드 테스트
    test_multiple_barcodes()
