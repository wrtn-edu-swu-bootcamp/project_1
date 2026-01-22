"""
사용자 맞춤형 운동 플랜 생성
"""

import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fitness_plan_demo import UserProfile, FitnessPlanGenerator

def main():
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "나의 FitPlan AI" + " " * 27 + "║")
    print("║" + " " * 10 + "개인 맞춤형 운동 플랜 생성 서비스" + " " * 12 + "║")
    print("╚" + "═" * 58 + "╝")
    
    print("\n안녕하세요! 귀하의 정보로 맞춤형 플랜을 생성합니다.\n")
    
    # 사용자 기본 정보 입력
    print("=" * 60)
    print("📝 기본 정보 입력")
    print("=" * 60)
    
    print("\n[현재 입력된 정보]")
    print("• 키: 164cm")
    print("• 몸무게: 57kg")
    print("• 체지방률: 26%")
    print("• 골격근량: 25kg")
    
    # 추가 정보 입력
    print("\n추가 정보를 입력해주세요:")
    
    while True:
        try:
            age = input("\n나이를 입력하세요 (만 나이): ").strip()
            age = int(age)
            if 10 <= age <= 100:
                break
            else:
                print("❌ 올바른 나이를 입력해주세요 (10-100세)")
        except ValueError:
            print("❌ 숫자로 입력해주세요.")
    
    while True:
        gender = input("성별을 입력하세요 (남/여): ").strip()
        if gender in ['남', '여', 'M', 'F', 'm', 'f']:
            if gender in ['남', 'M', 'm']:
                gender = '남성'
            else:
                gender = '여성'
            break
        else:
            print("❌ '남' 또는 '여'로 입력해주세요.")
    
    # 운동 목표 선택
    print("\n" + "=" * 60)
    print("🎯 운동 목표 선택")
    print("=" * 60)
    print("\n1. 체중 감량")
    print("2. 근육 증가")
    print("3. 체중 감량 + 근육 증가 (바디 리컴포지션)")
    print("4. 체력 향상")
    print("5. 건강 유지")
    
    while True:
        try:
            choice = input("\n목표를 선택하세요 (1-5): ").strip()
            choice = int(choice)
            if 1 <= choice <= 5:
                goals = {
                    1: "체중 감량",
                    2: "근육 증가",
                    3: "체중 감량 + 근육 증가",
                    4: "체력 향상",
                    5: "건강 유지"
                }
                goal = goals[choice]
                break
            else:
                print("❌ 1-5 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("❌ 숫자로 입력해주세요.")
    
    # 운동 환경 선택
    print("\n" + "=" * 60)
    print("🏋️ 운동 환경 선택")
    print("=" * 60)
    print("\n1. 헬스장 (모든 장비 이용 가능)")
    print("2. 홈트레이닝 (장비 있음 - 덤벨, 밴드 등)")
    print("3. 홈트레이닝 (장비 없음 - 맨몸 운동)")
    
    while True:
        try:
            choice = input("\n운동 환경을 선택하세요 (1-3): ").strip()
            choice = int(choice)
            if 1 <= choice <= 3:
                environments = {
                    1: "헬스장",
                    2: "홈트레이닝 (장비 있음)",
                    3: "홈트레이닝 (장비 없음)"
                }
                environment = environments[choice]
                break
            else:
                print("❌ 1-3 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("❌ 숫자로 입력해주세요.")
    
    # 주간 운동 빈도
    print("\n" + "=" * 60)
    print("📅 주간 운동 계획")
    print("=" * 60)
    
    while True:
        try:
            frequency = input("\n일주일에 몇 회 운동하시겠습니까? (3-7): ").strip()
            frequency = int(frequency)
            if 3 <= frequency <= 7:
                break
            else:
                print("❌ 3-7 사이의 숫자를 입력해주세요. (최소 주 3회 권장)")
        except ValueError:
            print("❌ 숫자로 입력해주세요.")
    
    # 1회 운동 시간
    while True:
        try:
            duration = input("1회 운동 시간은 몇 분인가요? (30-120분): ").strip()
            duration = int(duration)
            if 30 <= duration <= 120:
                break
            else:
                print("❌ 30-120 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("❌ 숫자로 입력해주세요.")
    
    # 통증 부위 확인
    print("\n" + "=" * 60)
    print("⚠️ 통증 부위 확인")
    print("=" * 60)
    print("\n현재 통증이나 불편함을 느끼는 부위가 있나요?")
    print("해당 부위를 피하거나 저강도 강화 운동을 제안합니다.")
    
    pain_areas = []
    has_pain = input("\n통증이 있습니까? (예/아니오): ").strip()
    
    if has_pain in ['예', 'y', 'yes', 'Y', 'YES', '네']:
        print("\n부위를 선택하세요 (여러 개 선택 가능, 쉼표로 구분):")
        print("1. 목/어깨")
        print("2. 허리")
        print("3. 무릎")
        print("4. 손목")
        print("5. 팔꿈치")
        print("6. 발목")
        
        selections = input("\n번호를 입력하세요 (예: 1,3,4): ").strip()
        
        area_map = {
            "1": "목/어깨",
            "2": "허리",
            "3": "무릎",
            "4": "손목",
            "5": "팔꿈치",
            "6": "발목"
        }
        
        for num in selections.split(','):
            num = num.strip()
            if num in area_map:
                pain_areas.append(area_map[num])
    
    # 사용자 프로필 생성
    user = UserProfile(
        height=164,
        weight=57,
        age=age,
        gender=gender,
        body_fat_percentage=26,
        skeletal_muscle_mass=25
    )
    
    # 입력 확인
    print("\n" + "=" * 60)
    print("✅ 입력 정보 확인")
    print("=" * 60)
    print(f"\n👤 나이: {age}세")
    print(f"👤 성별: {gender}")
    print(f"🎯 운동 목표: {goal}")
    print(f"🏋️ 운동 환경: {environment}")
    print(f"📅 주간 운동 빈도: 주 {frequency}회")
    print(f"⏱  1회 운동 시간: {duration}분")
    if pain_areas:
        print(f"⚠️  통증 부위: {', '.join(pain_areas)}")
    else:
        print(f"⚠️  통증 부위: 없음")
    
    input("\n계속하려면 Enter를 누르세요...")
    
    print("\n⏳ 맞춤형 운동 플랜을 생성하고 있습니다...\n")
    
    # 프로필 출력
    user.print_profile()
    
    # 플랜 생성기 초기화
    planner = FitnessPlanGenerator(user, goal, environment, frequency, duration, pain_areas)
    
    # 추천 목표 출력
    print("\n" + "=" * 60)
    print("🎯 AI 분석 결과")
    print("=" * 60)
    
    recommendations = planner.recommend_goal()
    if recommendations:
        print("\n귀하의 신체 분석 결과, 다음 목표들을 추천드립니다:")
        for idx, rec in enumerate(recommendations, 1):
            print(f"\n{idx}. {rec['목표']}")
            print(f"   우선순위: {rec['우선순위']}")
            print(f"   이유: {rec['이유']}")
    
    print("\n" + "=" * 60)
    
    # 주간 운동 플랜 생성 및 출력
    weekly_plan = planner.generate_weekly_plan()
    planner.print_weekly_plan(weekly_plan)
    
    # 영양 가이드 출력
    planner.print_nutrition_guide()
    
    # 예시 식단 출력
    planner.print_meal_plan()
    
    # 유산소 운동 가이드 출력
    planner.print_cardio_guide()
    
    # 무게 가이드라인 출력
    planner.print_weight_guide()
    
    # 통증 부위 주의사항 출력
    planner.print_pain_guidance()
    
    # 운동 팁 출력
    planner.print_tips()
    
    print("\n" + "=" * 60)
    print("✨ FitPlan AI와 함께 건강한 변화를 시작하세요! ✨")
    print("=" * 60)
    print("\n💾 이 플랜을 저장하거나 인쇄하여 활용하세요!")
    print("📊 매주 진행 상황을 기록하고 필요시 플랜을 조정하세요!")
    print("\n")


if __name__ == "__main__":
    main()
