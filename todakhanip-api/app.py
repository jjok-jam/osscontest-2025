from flask import Flask, request
from dotenv import load_dotenv
import os
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.product_parser import extract_product_info
from utils.translation_manager import load_translation_data, translate_ingredients_batch
from utils.health_analysis import get_health_analysis, get_comprehensive_health_analysis
from prompts.api_prompts import API_MESSAGES, HTTP_STATUS_CODES, RESPONSE_KEYS
from prompts.constants import (
    OPENFOODFACTS_API_BASE_URL,
    API_TIMEOUT,
    FLASK_HOST,
    FLASK_PORT,
    FLASK_DEBUG,
)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Flask 앱 시작 시 번역 데이터 미리 로드
print("🔄 번역 데이터 로드 중...")
load_translation_data()
print("✅ Flask 앱 초기화 완료")


@app.route("/barcode/<barcode>", methods=["GET", "POST"])
def get_barcode_info(barcode):
    """
    바코드로 제품 정보를 조회하고 건강 프로필과 함께 분석하는 API
    GET: 바코드 정보만 조회
    POST: 바코드 정보 조회 + 건강 프로필 분석
    """
    try:
        # OpenFoodFacts API 호출
        url = f"{OPENFOODFACTS_API_BASE_URL}/{barcode}.json"
        response = requests.get(url, timeout=API_TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            # 제품이 존재하는지 확인
            if data.get("status") == 1 and data.get("product"):
                product = data["product"]
                # 제품 정보 추출
                product_info = extract_product_info(product, barcode)

                # POST 요청인 경우 건강 프로필 분석과 원료 번역을 병렬로 수행
                if request.method == "POST":
                    if not request.json:
                        return {
                            RESPONSE_KEYS["SUCCESS"]: False,
                            RESPONSE_KEYS["ERROR"]: API_MESSAGES["INVALID_JSON"],
                        }, HTTP_STATUS_CODES["BAD_REQUEST"]

                    health_profile = request.json.get("health_profile")
                    if not health_profile:
                        return {
                            RESPONSE_KEYS["SUCCESS"]: False,
                            RESPONSE_KEYS["ERROR"]: "건강 프로필 정보가 필요합니다.",
                        }, HTTP_STATUS_CODES["BAD_REQUEST"]

                    # 병렬 처리를 위한 함수들
                    def run_health_analysis():
                        return get_health_analysis(product_info, health_profile)

                    def run_ingredients_translation():
                        barcode = product_info.get("code", "")
                        ingredients = product_info.get("ingredients", [])

                        if ingredients and barcode:
                            # 원료 텍스트를 쉼표로 구분된 문자열로 변환
                            ingredients_texts = []
                            for ingredient in ingredients:
                                if (
                                    isinstance(ingredient, dict)
                                    and "text" in ingredient
                                ):
                                    ingredients_texts.append(ingredient["text"])
                                elif isinstance(ingredient, str):
                                    ingredients_texts.append(ingredient)

                            if ingredients_texts:
                                ingredients_string = ",".join(ingredients_texts)
                                return translate_ingredients_batch(
                                    barcode, ingredients_string
                                )
                        return {}

                    # ThreadPoolExecutor를 사용하여 병렬 처리
                    with ThreadPoolExecutor(max_workers=2) as executor:
                        # 두 작업을 동시에 실행
                        health_future = executor.submit(run_health_analysis)
                        translation_future = executor.submit(
                            run_ingredients_translation
                        )

                        # 결과 수집
                        health_analysis = health_future.result()
                        translations = translation_future.result()

                    # 분석 결과를 product_info에 추가
                    product_info["health_analysis"] = health_analysis

                    # 번역 결과로 ingredients.text를 대체
                    if translations and product_info.get("ingredients"):
                        for ingredient in product_info["ingredients"]:
                            if isinstance(ingredient, dict) and "text" in ingredient:
                                original_text = ingredient["text"]
                                if original_text in translations:
                                    ingredient["text"] = translations[original_text]

                print(product_info)

                return {
                    RESPONSE_KEYS["SUCCESS"]: True,
                    RESPONSE_KEYS["DATA"]: product_info,
                }
            else:
                return {
                    RESPONSE_KEYS["SUCCESS"]: False,
                    RESPONSE_KEYS["ERROR"]: API_MESSAGES["PRODUCT_NOT_FOUND"],
                }, HTTP_STATUS_CODES["NOT_FOUND"]
        else:
            return {
                RESPONSE_KEYS["SUCCESS"]: False,
                RESPONSE_KEYS["ERROR"]: API_MESSAGES["API_REQUEST_FAILED"].format(
                    status_code=response.status_code
                ),
            }, response.status_code

    except requests.exceptions.RequestException as e:
        return {
            RESPONSE_KEYS["SUCCESS"]: False,
            RESPONSE_KEYS["ERROR"]: API_MESSAGES["REQUEST_ERROR"].format(error=str(e)),
        }, HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"]
    except json.JSONDecodeError as e:
        return {
            RESPONSE_KEYS["SUCCESS"]: False,
            RESPONSE_KEYS["ERROR"]: API_MESSAGES["JSON_DECODE_ERROR"].format(
                error=str(e)
            ),
        }, HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"]
    except Exception as e:
        return {
            RESPONSE_KEYS["SUCCESS"]: False,
            RESPONSE_KEYS["ERROR"]: API_MESSAGES["UNEXPECTED_ERROR"].format(
                error=str(e)
            ),
        }, HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"]


@app.route("/comprehensive-analysis", methods=["POST"])
def comprehensive_health_analysis():
    """
    제품 정보와 건강 프로필을 받아 종합적인 건강 분석을 수행하는 API

    요청 형식:
    - products_data: 제품 정보 배열 (필수)
    - health_profile: 건강 프로필 정보 (필수)
    """
    try:
        if not request.json:
            return {
                RESPONSE_KEYS["SUCCESS"]: False,
                RESPONSE_KEYS["ERROR"]: API_MESSAGES["INVALID_JSON"],
            }, HTTP_STATUS_CODES["BAD_REQUEST"]

        data = request.json
        products_data = data.get("products_data", [])
        health_profile = data.get("health_profile")

        if not products_data:
            return {
                RESPONSE_KEYS["SUCCESS"]: False,
                RESPONSE_KEYS["ERROR"]: "제품 데이터가 필요합니다.",
            }, HTTP_STATUS_CODES["BAD_REQUEST"]

        if not health_profile:
            return {
                RESPONSE_KEYS["SUCCESS"]: False,
                RESPONSE_KEYS["ERROR"]: "건강 프로필 정보가 필요합니다.",
            }, HTTP_STATUS_CODES["BAD_REQUEST"]

        # 제품 개수 제한 (성능 고려)
        if len(products_data) > 10:
            return {
                RESPONSE_KEYS["SUCCESS"]: False,
                RESPONSE_KEYS["ERROR"]: "한 번에 최대 10개 제품까지 분석 가능합니다.",
            }, HTTP_STATUS_CODES["BAD_REQUEST"]

        products_info = []
        failed_products = []

        # 제공된 제품 데이터를 직접 사용
        for product_data in products_data:
            try:
                # 바코드 필드 확인 (code 또는 barcode)
                barcode = product_data.get("code") or product_data.get("barcode")
                if not barcode:
                    print(f"제품 데이터에 바코드가 없습니다: {product_data}")
                    continue

                # 영양 정보 필드 확인 (nutriments 또는 nutrition_data)
                nutrition_data = product_data.get("nutriments") or product_data.get(
                    "nutrition_data", {}
                )

                # 제품 정보 추출 및 정리
                product_info = {
                    "code": barcode,
                    "product_name": product_data.get("product_name", ""),
                    "brands": product_data.get("brands", ""),
                    "nutriments": nutrition_data,
                    "allergens_tags": product_data.get("allergens_tags", []),
                    "food_groups_tags": product_data.get("food_groups_tags", []),
                    "nutriscore_grade": product_data.get("nutriscore_grade", ""),
                    "nutrient_levels": product_data.get("nutrient_levels", {}),
                    "ingredients": product_data.get("ingredients", []),
                    "serving_size": product_data.get("serving_size", ""),
                    "quantity": product_data.get("quantity", ""),
                    "image_url": product_data.get("image_url", ""),
                }
                products_info.append(product_info)

            except Exception as e:
                print(f"제품 데이터 처리 중 오류: {str(e)}")
                barcode = product_data.get("code") or product_data.get("barcode")
                if barcode:
                    failed_products.append(barcode)

        if not products_info:
            return {
                RESPONSE_KEYS["SUCCESS"]: False,
                RESPONSE_KEYS["ERROR"]: "유효한 제품 정보를 찾을 수 없습니다.",
            }, HTTP_STATUS_CODES["NOT_FOUND"]

        # 종합 건강 분석 수행
        comprehensive_analysis = get_comprehensive_health_analysis(
            products_info, health_profile
        )

        # 응답 데이터 구성
        response_data = {
            "comprehensive_analysis": comprehensive_analysis,
            "analyzed_products": len(products_info),
            "total_requested": len(products_data),
            "failed_products": failed_products,
            "products_summary": [
                {
                    "barcode": product.get("code"),
                    "name": product.get("product_name"),
                    "brands": product.get("brands"),
                }
                for product in products_info
            ],
        }

        return {
            RESPONSE_KEYS["SUCCESS"]: True,
            RESPONSE_KEYS["DATA"]: response_data,
        }

    except Exception as e:
        return {
            RESPONSE_KEYS["SUCCESS"]: False,
            RESPONSE_KEYS["ERROR"]: API_MESSAGES["UNEXPECTED_ERROR"].format(
                error=str(e)
            ),
        }, HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"]


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
