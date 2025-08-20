#!/usr/bin/env python3
"""
건강 프로필 분석 API 테스트 스크립트
"""

import requests
import json

# API 기본 URL
BASE_URL = "http://localhost:6318"

# 테스트용 건강 프로필 (사용자가 제공한 형식)
test_health_profile = {
    "name": "홍길동",
    "job": "연구원",
    "notes": "고도비만",
    "gender": "남",
    "birth_year": 1982,
    "weight": 93,
    "height": 183,
    "activity_level": "보통",
    "has_diabetes": "아니오",
    "has_hypertension": "예",
    "systolic_bp": "150",
    "diastolic_bp": "80",
    "has_allergies": "예",
    "selected_allergies": "알류,우유,메밀",
}

# 테스트용 바코드 (실제 존재하는 제품)
test_barcode = "3017620422003"  # Nutella 예시


def test_barcode_only():
    """바코드 정보만 조회하는 테스트 (GET 요청)"""
    print("=== 바코드 정보만 조회 (GET) ===")

    url = f"{BASE_URL}/barcode/{test_barcode}"
    response = requests.get(url)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ 성공!")
        print(f"제품명: {data['data']['product_name']}")
        print(f"브랜드: {data['data']['brands']}")
        print(f"영양등급: {data['data']['nutriscore_grade']}")
    else:
        print("❌ 실패!")
        print(response.text)

    print("\n" + "=" * 50 + "\n")


def test_barcode_with_health_analysis():
    """바코드 정보 + 건강 프로필 분석 테스트 (POST 요청)"""
    print("=== 바코드 정보 + 건강 프로필 분석 (POST) ===")

    url = f"{BASE_URL}/barcode/{test_barcode}"
    payload = {"health_profile": test_health_profile}

    response = requests.post(url, json=payload)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ 성공!")
        print(f"제품명: {data['data']['product_name']}")
        print(f"브랜드: {data['data']['brands']}")
        print(f"영양등급: {data['data']['nutriscore_grade']}")

        # 건강 분석 결과 출력
        if "health_analysis" in data["data"]:
            print("\n🔬 건강 분석 결과:")
            print(data["data"]["health_analysis"])
        else:
            print("\n❌ 건강 분석 결과가 없습니다.")
    else:
        print("❌ 실패!")
        print(response.text)

    print("\n" + "=" * 50 + "\n")


def test_invalid_barcode():
    """존재하지 않는 바코드 테스트"""
    print("=== 존재하지 않는 바코드 테스트 ===")

    invalid_barcode = "9999999999999"
    url = f"{BASE_URL}/barcode/{invalid_barcode}"

    # GET 요청
    response = requests.get(url)
    print(f"GET 요청 Status Code: {response.status_code}")
    if response.status_code == 404:
        print("✅ 올바른 오류 응답 (제품을 찾을 수 없음)")
    else:
        print("❌ 예상과 다른 응답")
        print(response.text)

    # POST 요청
    payload = {"health_profile": test_health_profile}
    response = requests.post(url, json=payload)
    print(f"POST 요청 Status Code: {response.status_code}")
    if response.status_code == 404:
        print("✅ 올바른 오류 응답 (제품을 찾을 수 없음)")
    else:
        print("❌ 예상과 다른 응답")
        print(response.text)

    print("\n" + "=" * 50 + "\n")


def test_invalid_health_profile():
    """잘못된 건강 프로필 테스트"""
    print("=== 잘못된 건강 프로필 테스트 ===")

    url = f"{BASE_URL}/barcode/{test_barcode}"

    # 건강 프로필 없이 POST 요청
    response = requests.post(url, json={})
    print(f"건강 프로필 없이 POST 요청 Status Code: {response.status_code}")
    if response.status_code == 400:
        print("✅ 올바른 오류 응답 (건강 프로필 정보가 필요함)")
    else:
        print("❌ 예상과 다른 응답")
        print(response.text)

    # 잘못된 JSON 형식
    response = requests.post(
        url, data="invalid json", headers={"Content-Type": "application/json"}
    )
    print(f"잘못된 JSON 형식 Status Code: {response.status_code}")
    if response.status_code == 400:
        print("✅ 올바른 오류 응답 (잘못된 JSON)")
    else:
        print("❌ 예상과 다른 응답")
        print(response.text)

    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    print("🏥 건강 프로필 분석 API 테스트 시작\n")

    try:
        # 1. 바코드 정보만 조회
        test_barcode_only()

        # 2. 바코드 정보 + 건강 프로필 분석
        test_barcode_with_health_analysis()

        # 3. 존재하지 않는 바코드 테스트
        test_invalid_barcode()

        # 4. 잘못된 건강 프로필 테스트
        test_invalid_health_profile()

        print("🎉 모든 테스트 완료!")

    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. Flask 앱이 실행 중인지 확인해주세요.")
        print("   python app.py 명령어로 서버를 시작하세요.")
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
