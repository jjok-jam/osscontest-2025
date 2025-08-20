# TodakHanip (토닥한입) - 나만의 가공식품 건강 분석 서비스

<div align="center">
  <img src="todakhanip/assets/logo/logo-5.png" alt="LabelSafe Logo" width="200"/>
  
  [![Flutter](https://img.shields.io/badge/Flutter-3.2.3+-blue.svg)](https://flutter.dev/)
  [![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org/)
  [![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)
  [![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)
</div>

## 📋 프로젝트 개요

TodakHanip (토닥한입)은 개인의 건강 프로필을 기반으로 식품 라벨을 분석하여 맞춤형 건강 정보를 제공하는 스마트 시스템입니다.
바코드 스캔을 통해 제품 정보를 조회하고, AI 기반 건강 분석을 통해 개인에게 최적화된 식품 선택 가이드를 제공합니다.

### 🎯 주요 기능

- **📱 바코드 스캔**: 모바일 앱을 통한 간편한 바코드 스캔
- **🧠 AI 건강 분석**: 개인 건강 프로필 기반 맞춤형 분석
- **🌍 다국어 지원**: 원료 정보 자동 번역 (한국어)
- **📊 영양 정보 분석**: 상세한 영양 성분 및 알레르기 정보
- **🔍 종합 분석**: 여러 제품의 통합 건강 분석

## 🏗️ 시스템 아키텍처

### TodakHanip 시스템 구조도
![토닥한입 시스템 아키텍처](https://github.com/user-attachments/assets/72722f86-1fb5-43da-b41e-6c5d0fb9e47b)

### 데이터 흐름

1. **사용자 입력**: 모바일 앱에서 바코드 스캔 및 건강 프로필 입력
2. **제품 정보 조회**: Core API Server가 OpenFoodFacts API에서 제품 정보 가져오기
3. **데이터 캐싱**: 조회된 제품 정보를 MongoDB에 캐시 저장
4. **AI 분석**: 제품 정보와 건강 프로필을 OpenAI API로 전송하여 개인화된 건강 영향 분석
5. **보고서 생성**: Reports & Visualization에서 영양 등급, 위험 요약, 개인화된 팁 생성
6. **결과 전달**: 분석 결과를 모바일 앱 사용자에게 제공

## 📦 프로젝트 구조

```

osscontest-2025/
├── todakhanip/ # Flutter 모바일 앱
│ ├── lib/ # Dart 소스 코드
│ │ ├── screen/ # 화면 UI
│ │ ├── services/ # API 서비스
│ │ ├── models/ # 데이터 모델
│ │ └── widget/ # 재사용 컴포넌트
│ ├── assets/ # 이미지 및 리소스
│ └── pubspec.yaml # Flutter 의존성
├── todakhanip-api/ # Flask 백엔드 API
│ ├── app.py # 메인 Flask 앱
│ ├── utils/ # 유틸리티 함수
│ ├── prompts/ # AI 프롬프트
│ ├── data/ # 데이터 파일
│ └── test/ # 테스트 코드
└── README.md # 프로젝트 문서

```

## 🚀 기술 스택

### Frontend (Flutter)

- **Flutter 3.2.3+**: 크로스 플랫폼 모바일 개발
- **Camera**: 바코드 스캔 기능
- **Mobile Scanner**: QR/바코드 인식
- **HTTP**: API 통신
- **SQLite**: 로컬 데이터 저장

### Backend (Python/Flask)

- **Flask**: RESTful API 서버
- **OpenAI GPT-4**: AI 기반 건강 분석
- **OpenFoodFacts API**: 제품 정보 조회
- **MongoDB**: 번역 데이터 저장
- **ThreadPoolExecutor**: 병렬 처리

### AI & Data

- **OpenAI GPT-4**: 자연어 처리 및 건강 분석
- **번역 시스템**: 다국어 원료 정보 한국어 번역
- **건강 프로필 분석**: 개인 맞춤형 식품 추천

## 📊 상품 메타데이터 구조

시스템에서 처리하는 제품 정보는 다음과 같은 구조로 구성됩니다:

### 기본 제품 정보

```json
{
  "code": "3017620422003", // 바코드
  "product_name": "Nutella", // 제품명
  "product_name_en": "Nutella", // 영문 제품명
  "brands": "Ferrero", // 브랜드
  "product_type": "식품", // 제품 분류
  "product_quantity": "400", // 제품 중량
  "product_quantity_unit": "g", // 중량 단위
  "quantity": "400 g" // 중량 표기
}
```

### 영양 정보

```json
{
  "nutriscore_grade": "e", // 영양등급 (a~e)
  "nutrient_levels": {
    // 영양소 수준
    "fat": "high",
    "saturated-fat": "high",
    "sugars": "high",
    "salt": "low"
  },
  "nutriments": {
    // 영양성분 (100g당)
    "fat_100g": 30.9,
    "saturated-fat_100g": 10.6,
    "sugars_100g": 56.3,
    "salt_100g": 0.107
  }
}
```

### 원료 및 알레르기 정보

```json
{
  "ingredients": [
    // 원료 정보
    {
      "text": "Sucre", // 원료명
      "percent_estimate": 38.35, // 함량 비율
      "processing": "가공 정보", // 가공 방법
      "vegan": "yes", // 비건 여부
      "vegetarian": "yes" // 채식주의자 여부
    }
  ],
  "allergens_tags": ["우유", "견과류", "대두"], // 알레르기 정보
  "food_groups_tags": ["당류 간식", "사탕류"] // 식품 그룹
}
```

### 서빙 정보

```json
{
  "serving_quantity": "15", // 1회 섭취량
  "serving_quantity_unit": "g", // 섭취량 단위
  "serving_size": "15 g" // 섭취량 표기
}
```

### 이미지 정보

```json
{
  "image_url": "https://...", // 제품 이미지
  "image_nutrition_url": "https://...", // 영양정보 이미지
  "image_ingredients_url": "https://...", // 원료 이미지
  "image_packaging_url": "https://..." // 패키지 이미지
}
```

### 판매 지역 정보

```json
{
  "countries_tags": [
    // 판매 국가
    "en:belgium",
    "en:france",
    "en:germany",
    "en:italy"
  ]
}
```

## 🔧 설치 및 실행

### 1. 환경 설정

#### API 서버 설정

```bash
cd todakhanip-api

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열고 실제 값으로 수정
```

#### Flutter 앱 설정

```bash
cd todakhanip

# 의존성 설치
flutter pub get

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열고 실제 값으로 수정
```

### 2. 서버 실행

```bash
# API 서버 실행
cd todakhanip-api
python app.py

# Flutter 앱 실행
cd todakhanip
flutter run
```

## 📱 API 엔드포인트

### 1. 바코드 정보 조회

```http
GET /barcode/{barcode}
```

**응답 예시:**

```json
{
  "success": true,
  "data": {
    "code": "3017620422003",
    "product_name": "Nutella",
    "brands": "Ferrero",
    "nutriscore_grade": "e",
    "ingredients": [...],
    "nutriments": {...}
  }
}
```

### 2. 건강 프로필 분석

```http
POST /barcode/{barcode}
Content-Type: application/json

{
  "health_profile": {
    "name": "홍길동",
    "age": 30,
    "weight": 70,
    "height": 175,
    "has_diabetes": "아니오",
    "has_hypertension": "예",
    "has_allergies": "예",
    "selected_allergies": ["우유", "견과류"]
  }
}
```

### 3. 종합 건강 분석

```http
POST /comprehensive-analysis
Content-Type: application/json

{
  "products_data": [...],
  "health_profile": {...}
}
```

## 🧪 테스트

### API 테스트

```bash
cd todakhanip-api/test

# 바코드 API 테스트
python barcord_test.py

# 건강 분석 테스트
python health_analysis_test.py

# 종합 분석 테스트
python test_comprehensive_analysis.py
```

### Flutter 앱 테스트

```bash
cd todakhanip
flutter test
```

## 🔒 보안

- 모든 API 키와 민감한 정보는 환경변수로 관리
- `.env` 파일은 Git에 추적되지 않음
- HTTPS 통신 권장
- API 요청 제한 및 인증 시스템

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👥 팀 정보

- **팀명**: 팀제이
- **팀장**: 고건환
- **프로젝트**: 2025 오픈소스 개발자대회 참가작

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

<div align="center">
  <p>Made with by Team J</p>
  <p>2025 Open Source Developer Contest</p>
</div>
