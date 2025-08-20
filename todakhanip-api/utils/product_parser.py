from utils.translation_manager import translate_text, translate_tags


def extract_product_info(product, barcode):
    """
    OpenFoodFacts API 응답에서 제품 정보를 추출하는 함수

    Args:
        product (dict): OpenFoodFacts API에서 받은 제품 데이터
        barcode (str): 제품 바코드

    Returns:
        dict: 추출된 제품 정보
    """

    # ingredients 처리 함수
    def process_ingredients(ingredients_data):
        """ingredients 데이터를 안전하게 처리"""
        if isinstance(ingredients_data, list) and len(ingredients_data) > 0:
            # 리스트인 경우 모든 항목을 처리
            processed_ingredients = []
            for ingredient in ingredients_data:
                processed_ingredient = {
                    "text": ingredient.get("text", "원재료 정보 없음"),
                    "percent_estimate": ingredient.get("percent_estimate", 0),
                    "processing": ingredient.get("processing", "가공 정보 없음"),
                    "vegan": ingredient.get("vegan", "비건 여부 정보 없음"),
                    "vegetarian": ingredient.get(
                        "vegetarian", "채식주의자 여부 정보 없음"
                    ),
                }
                processed_ingredients.append(processed_ingredient)
            return processed_ingredients
        else:
            # 기본값 반환 (빈 배열)
            return []

    # nutriments 안전 처리 함수
    def process_nutriments(nutriments_data):
        """nutriments 데이터를 안전하게 처리"""
        if isinstance(nutriments_data, dict):
            return {
                "fat_100g": nutriments_data.get("fat_100g", 0),
                "saturated-fat_100g": nutriments_data.get("saturated-fat_100g", 0),
                "sugars_100g": nutriments_data.get("sugars_100g", 0),
                "salt_100g": nutriments_data.get("salt_100g", 0),
            }
        else:
            return {
                "fat_100g": 0,
                "saturated-fat_100g": 0,
                "sugars_100g": 0,
                "salt_100g": 0,
            }

    # nutrient_levels 안전 처리 함수
    def process_nutrient_levels(nutrient_levels_data):
        """nutrient_levels 데이터를 안전하게 처리"""
        if isinstance(nutrient_levels_data, dict):
            return {
                "fat": nutrient_levels_data.get("fat", "지방 함량 수준 정보 없음"),
                "saturated-fat": nutrient_levels_data.get(
                    "saturated-fat", "포화지방 함량 수준 정보 없음"
                ),
                "sugars": nutrient_levels_data.get(
                    "sugars", "당류 함량 수준 정보 없음"
                ),
                "salt": nutrient_levels_data.get("salt", "나트륨 함량 수준 정보 없음"),
            }
        else:
            return {
                "fat": "지방 함량 수준 정보 없음",
                "saturated-fat": "포화지방 함량 수준 정보 없음",
                "sugars": "당류 함량 수준 정보 없음",
                "salt": "나트륨 함량 수준 정보 없음",
            }

    # 번역 데이터는 Flask 앱 시작 시 이미 로드됨

    product_info = {
        # 일반 정보
        "code": barcode,
        "brands": product.get("brands", "상표 브랜드 정보 없음"),
        "countries_tags": product.get("countries_tags", []),
        "product_name": product.get("product_name", "상품명 정보 없음"),
        "product_name_en": product.get("product_name_en", "영문 상품명 정보 없음"),
        "product_type": translate_text(
            product.get("product_type", "상품 분류 정보 없음"), "product"
        ),
        "product_quantity": product.get("product_quantity", "상품 중량 정보 없음"),
        "product_quantity_unit": product.get(
            "product_quantity_unit", "상품 중량 단위 정보 없음"
        ),
        "quantity": product.get("quantity", "상품 중량 표기 정보 없음"),
        "allergens_tags": translate_tags(
            product.get("allergens_tags", []), "allergens"
        ),
        "food_groups_tags": translate_tags(
            product.get("food_groups_tags", []), "food_groups"
        ),
        # 영양소 정보
        "nutriscore_grade": product.get("nutriscore_grade", "영양 등급 정보 없음"),
        "nutrient_levels": process_nutrient_levels(product.get("nutrient_levels", {})),
        "nutriments": process_nutriments(product.get("nutriments", {})),
        # 원재료 정보
        "ingredients": process_ingredients(product.get("ingredients", [])),
        # 1회 섭취 기준량
        "serving_quantity": product.get("serving_quantity", "1회 섭취량 정보 없음"),
        "serving_quantity_unit": product.get(
            "serving_quantity_unit", "1회 섭취량 단위 정보 없음"
        ),
        "serving_size": product.get("serving_size", "1회 섭취량 표기 정보 없음"),
        # 상품 이미지 정보
        "image_front_url": product.get("image_front_url", ""),
        "image_ingredients_url": product.get("image_ingredients_url", ""),
        "image_nutrition_url": product.get("image_nutrition_url", ""),
        "image_packaging_url": product.get("image_packaging_url", ""),
        "image_url": product.get("image_url", ""),
        "image_thumb_url": product.get("image_thumb_url", ""),
    }

    return product_info
