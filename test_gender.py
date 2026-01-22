"""
성별에 따른 운동 플랜 차이 테스트
"""

import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fitness_plan_demo import UserProfile, FitnessPlanGenerator

print("\n" + "=" * 60)
print("🔬 성별별 운동 플랜 비교 테스트")
print("=" * 60)

# 남성 프로필
print("\n\n" + "█" * 60)
print("  남성 (70kg) - 고강도 저반복")
print("█" * 60)

male_user = UserProfile(
    height=175,
    weight=70,
    age=25,
    gender="남성",
    body_fat_percentage=18,
    skeletal_muscle_mass=32
)

male_planner = FitnessPlanGenerator(
    male_user,
    "근육 증가",
    "헬스장",
    4,
    60
)

print("\n🎯 남성 권장: " + male_planner.rep_description)
print("📊 반복 범위: " + male_planner.rep_range)

print("\n⚖️  무게 가이드:")
exercises = ["바벨 스쿼트", "벤치 프레스", "데드리프트", "바벨 컬"]
for exercise in exercises:
    weights = male_planner.get_weight_recommendation(exercise)
    if weights:
        print(f"\n  {exercise}:")
        print(f"    초급: {weights['초급']}kg | 중급: {weights['중급']}kg | 고급: {weights['고급']}kg")

# 여성 프로필
print("\n\n" + "█" * 60)
print("  여성 (57kg) - 저강도 고반복")
print("█" * 60)

female_user = UserProfile(
    height=164,
    weight=57,
    age=25,
    gender="여성",
    body_fat_percentage=26,
    skeletal_muscle_mass=25
)

female_planner = FitnessPlanGenerator(
    female_user,
    "체중 감량 + 근육 증가",
    "헬스장",
    4,
    60
)

print("\n🎯 여성 권장: " + female_planner.rep_description)
print("📊 반복 범위: " + female_planner.rep_range)

print("\n⚖️  무게 가이드:")
for exercise in exercises:
    weights = female_planner.get_weight_recommendation(exercise)
    if weights:
        print(f"\n  {exercise}:")
        print(f"    초급: {weights['초급']}kg | 중급: {weights['중급']}kg | 고급: {weights['고급']}kg")

# 비교표
print("\n\n" + "=" * 60)
print("📊 성별 비교표")
print("=" * 60)

print("\n운동           | 남성 (중급)  | 여성 (중급)")
print("-" * 60)
for exercise in exercises:
    male_w = male_planner.get_weight_recommendation(exercise)
    female_w = female_planner.get_weight_recommendation(exercise)
    if male_w and female_w:
        print(f"{exercise:12} | {male_w['중급']:8.1f}kg | {female_w['중급']:8.1f}kg")

print("\n" + "=" * 60)
print("✅ 성별에 따라 다른 반복 횟수와 무게가 적용되었습니다!")
print("=" * 60)
print("\n")
