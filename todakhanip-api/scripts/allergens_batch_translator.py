import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read_allergens_file(file_path):
    """allergens.txt 파일을 읽어서 리스트로 반환"""
    with open(file_path, "r", encoding="utf-8") as f:
        allergens = [line.strip() for line in f if line.strip()]
    return allergens


def translate_batch(allergens_batch, batch_num):
    """OpenAI API를 사용하여 배치 번역"""
    try:
        # 번역 요청 메시지 구성
        allergens_text = "\n".join(allergens_batch)

        response = client.chat.completions.create(
            model="gpt-4o",  # 최고 성능 모델 사용
            messages=[
                {
                    "role": "system",
                    "content": "당신은 전문 번역가입니다. 주어진 알레르기 원료 목록을 한국어로 정확하게 번역해주세요. 각 항목을 'original: 원본텍스트, korean: 한국어번역' 형식으로 JSON 배열로 반환해주세요.",
                },
                {
                    "role": "user",
                    "content": f"다음 알레르기 원료들을 한국어로 번역해주세요:\n\n{allergens_text}",
                },
            ],
            temperature=0.1,  # 일관된 번역을 위해 낮은 temperature 사용
            max_tokens=4000,
        )

        # 응답에서 JSON 추출
        content = response.choices[0].message.content
        if content is None:
            print(f"❌ 배치 {batch_num} 빈 응답 받음")
            return []

        content = content.strip()

        # JSON 파싱 시도
        try:
            # JSON 부분만 추출 (```json ... ``` 형태일 수 있음)
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
            print(f"✅ 배치 {batch_num} 번역 완료: {len(translated_data)}개 항목")
            return translated_data

        except json.JSONDecodeError as e:
            print(f"❌ 배치 {batch_num} JSON 파싱 오류: {e}")
            print(f"응답 내용: {content}")
            return []

    except Exception as e:
        print(f"❌ 배치 {batch_num} 번역 오류: {e}")
        return []


def save_translations(translations, output_file):
    """번역 결과를 JSON 파일로 저장"""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        print(f"✅ 번역 결과 저장 완료: {output_file}")
    except Exception as e:
        print(f"❌ 파일 저장 오류: {e}")


def main():
    # 파일 경로 설정
    input_file = "../data/03.allergens.txt"
    output_file = "../data/103.allergens_translated.json"

    print("🚀 알레르기 원료 번역 시작")
    print("=" * 50)

    # 입력 파일 읽기
    print(f"📖 파일 읽기: {input_file}")
    allergens = read_allergens_file(input_file)
    print(f"📊 총 {len(allergens)}개의 알레르기 원료 발견")

    # 기존 번역 파일이 있다면 로드
    existing_translations = []
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                existing_translations = json.load(f)
            print(f"📋 기존 번역 {len(existing_translations)}개 로드됨")
        except:
            print("📋 기존 번역 파일 로드 실패, 새로 시작합니다.")

    # 이미 번역된 항목들 제외
    translated_originals = {item["original"] for item in existing_translations}
    remaining_allergens = [
        item for item in allergens if item not in translated_originals
    ]

    if not remaining_allergens:
        print("✅ 모든 항목이 이미 번역되었습니다.")
        return

    print(f"🔄 번역할 항목: {len(remaining_allergens)}개")

    # 배치 크기 설정
    batch_size = 100
    all_translations = existing_translations.copy()

    # 배치별 번역 처리
    total_batches = (len(remaining_allergens) + batch_size - 1) // batch_size

    with tqdm(total=total_batches, desc="번역 진행률", unit="배치") as pbar:
        for i in range(0, len(remaining_allergens), batch_size):
            batch_num = (i // batch_size) + 1
            batch = remaining_allergens[i : i + batch_size]

            pbar.set_description(f"배치 {batch_num}/{total_batches} 처리 중")
            pbar.set_postfix({"항목수": len(batch), "총번역": len(all_translations)})

            # 번역 실행
            batch_translations = translate_batch(batch, batch_num)

            if batch_translations:
                all_translations.extend(batch_translations)

                # 중간 저장 (배치마다)
                save_translations(all_translations, output_file)

            # API 호출 간격 조절 (Rate limiting 방지)
            if i + batch_size < len(remaining_allergens):
                pbar.set_postfix({"대기": "3초"})
                time.sleep(3)

            pbar.update(1)

    # 최종 저장
    save_translations(all_translations, output_file)

    print("\n🎉 번역 완료!")
    print(f"📊 총 번역된 항목: {len(all_translations)}개")
    print(f"💾 저장된 파일: {output_file}")


if __name__ == "__main__":
    main()
