"""
사용자 데이터로 자동 예시 생성
키 164cm, 몸무게 57kg, 체지방률 26%, 골격근량 25kg
"""

import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fitness_plan_demo import UserProfile, FitnessPlanGenerator

def create_example_plans():
    """여러 시나리오로 플랜 생성"""
    
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "나의 맞춤형 운동 플랜 예시" + " " * 18 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # 사용자 기본 정보
    base_info = {
        "height": 164,
        "weight": 57,
        "body_fat_percentage": 26,
        "skeletal_muscle_mass": 25
    }
    
    print("\n📋 사용자 기본 정보")
    print("=" * 60)
    print(f"키: {base_info['height']}cm")
    print(f"몸무게: {base_info['weight']}kg")
    print(f"체지방률: {base_info['body_fat_percentage']}%")
    print(f"골격근량: {base_info['skeletal_muscle_mass']}kg")
    print("=" * 60)
    
    # 여러 시나리오 생성
    scenarios = [
        {
            "name": "시나리오 1: 헬스장에서 체중 감량",
            "age": 25,
            "gender": "여성",
            "goal": "체중 감량 + 근육 증가",
            "environment": "헬스장",
            "frequency": 4,
            "duration": 60,
            "pain_areas": ["손목"]
        },
        {
            "name": "시나리오 2: 홈트로 체력 향상",
            "age": 28,
            "gender": "여성",
            "goal": "체력 향상",
            "environment": "홈트레이닝 (장비 있음)",
            "frequency": 3,
            "duration": 45,
            "pain_areas": []
        },
        {
            "name": "시나리오 3: 맨몸 운동으로 건강 유지",
            "age": 30,
            "gender": "여성",
            "goal": "건강 유지",
            "environment": "홈트레이닝 (장비 없음)",
            "frequency": 5,
            "duration": 40,
            "pain_areas": ["허리", "무릎"]
        }
    ]
    
    for idx, scenario in enumerate(scenarios, 1):
        print("\n\n")
        print("█" * 60)
        print(f"  {scenario['name']}")
        print("█" * 60)
        
        print("\n📌 시나리오 설정")
        print("=" * 60)
        print(f"나이: {scenario['age']}세")
        print(f"성별: {scenario['gender']}")
        print(f"목표: {scenario['goal']}")
        print(f"환경: {scenario['environment']}")
        print(f"빈도: 주 {scenario['frequency']}회")
        print(f"시간: {scenario['duration']}분/회")
        if scenario['pain_areas']:
            print(f"통증 부위: {', '.join(scenario['pain_areas'])}")
        else:
            print("통증 부위: 없음")
        print("=" * 60)
        
        # 사용자 프로필 생성
        user = UserProfile(
            height=base_info['height'],
            weight=base_info['weight'],
            age=scenario['age'],
            gender=scenario['gender'],
            body_fat_percentage=base_info['body_fat_percentage'],
            skeletal_muscle_mass=base_info['skeletal_muscle_mass']
        )
        
        # 프로필 출력
        user.print_profile()
        
        # 플랜 생성기 초기화
        planner = FitnessPlanGenerator(
            user,
            scenario['goal'],
            scenario['environment'],
            scenario['frequency'],
            scenario['duration'],
            scenario['pain_areas']
        )
        
        # AI 분석 결과
        print("\n" + "=" * 60)
        print("🎯 AI 분석 결과")
        print("=" * 60)
        
        recommendations = planner.recommend_goal()
        if recommendations:
            print("\n신체 분석 결과 추천 목표:")
            for rec_idx, rec in enumerate(recommendations, 1):
                print(f"\n{rec_idx}. {rec['목표']}")
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
        
        # 마지막 시나리오가 아니면 구분선
        if idx < len(scenarios):
            print("\n" + "▼" * 60)
            print("다음 시나리오로 넘어갑니다...")
            print("▼" * 60)
    
    # 운동 팁은 마지막에 한 번만
    print("\n\n")
    print("=" * 60)
    print("💡 모든 시나리오 공통 운동 팁")
    print("=" * 60)
    
    tips = [
        "워밍업은 필수! 운동 전 5-10분 가벼운 유산소와 동적 스트레칭",
        "운동 후 쿨다운과 정적 스트레칭으로 근육 회복 촉진",
        "충분한 수면 (7-8시간)은 근육 회복과 성장에 필수적입니다",
        "점진적 과부하: 매주 조금씩 무게나 횟수를 늘려가세요",
        "운동 일지를 작성하여 진행 상황을 추적하세요",
        "통증이 느껴지면 즉시 중단하고 휴식을 취하세요",
        "일주일에 2-3일은 충분한 휴식일을 가지세요"
    ]
    
    for tip_idx, tip in enumerate(tips, 1):
        print(f"\n  {tip_idx}. {tip}")
    
    print("\n" + "=" * 60)
    print("✨ FitPlan AI와 함께 건강한 변화를 시작하세요! ✨")
    print("=" * 60)
    print("\n💡 위의 3가지 시나리오 중 가장 적합한 것을 선택하거나,")
    print("   my_fitness_plan.py를 실행하여 직접 맞춤 플랜을 생성하세요!")
    print("\n")


if __name__ == "__main__":
    create_example_plans()
