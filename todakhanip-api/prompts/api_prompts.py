"""
API 관련 프롬프트 및 메시지 상수 관리
"""

# API 응답 메시지
API_MESSAGES = {
    "INVALID_JSON": "Invalid JSON data",
    "NO_QUESTION": "No question provided",
    "PRODUCT_NOT_FOUND": "Product not found",
    "API_REQUEST_FAILED": "API request failed with status {status_code}",
    "REQUEST_ERROR": "Request error: {error}",
    "JSON_DECODE_ERROR": "JSON decode error: {error}",
    "UNEXPECTED_ERROR": "Unexpected error: {error}",
}

# HTTP 상태 코드
HTTP_STATUS_CODES = {"BAD_REQUEST": 400, "NOT_FOUND": 404, "INTERNAL_SERVER_ERROR": 500}

# 성공/실패 응답 키
RESPONSE_KEYS = {"SUCCESS": "success", "ERROR": "error", "DATA": "data"}
