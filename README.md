# FitPlan AI - 개인 맞춤형 운동 플랜 생성 서비스

AI 기반 개인 맞춤형 운동 플랜 자동 생성 프로그램입니다.

## 🎯 주요 기능

- ✅ **대화형 정보 수집**: 누락된 정보 자동 질문
- ✅ **신체 구성 분석**: BMI, 체지방률, 골격근 비율 등 분석
- ✅ **맞춤형 운동 플랜**: 목표, 환경, 빈도에 따른 최적화된 플랜 생성
- ✅ **환경별 운동**: 헬스장/홈트(장비 O/X) 별 다른 운동 제공
- ✅ **빈도별 분할**: 주 3-7회에 맞는 다양한 운동 분할
- ✅ **성별 맞춤**: 남성(고강도 저반복) vs 여성(저강도 고반복)
- ✅ **무게 가이드**: 체중 기반 운동별 추천 무게 (초급/중급/고급)
- ✅ **영양 가이드**: BMR, TDEE 기반 맞춤 칼로리 및 영양소 가이드
- ✅ **예시 식단**: 목표별 구체적인 하루 식단 (칼로리 및 영양소 정보 포함)
- ✅ **유산소 가이드**: 목표별 심박수, 강도, 기구, 시간 추천
- ✅ **통증 관리**: 통증 부위별 피해야 할/대체 운동 및 재활 운동 제공
- ✅ **운동 팁**: 효과적인 운동을 위한 실용적인 조언

## 🚀 빠른 시작

### 1. 테스트 모드로 실행

```bash
python fitness_plan_demo.py test
```

예시 데이터로 즉시 결과를 확인할 수 있습니다.

### 2. 대화형 모드로 실행

```bash
python fitness_plan_demo.py
```

질문에 답하며 나만의 맞춤형 플랜을 생성합니다.

자세한 사용법은 [사용 가이드](사용_가이드.md)를 참고하세요.

## 📋 파일 구성

- `fitness_plan_demo.py` - 메인 프로그램
- `기획안.md` - 프로젝트 기획 문서
- `사용_가이드.md` - 사용 가이드
- `README.md` - 프로젝트 소개

## 📊 프로젝트 구조

```
mcp/
├── fitness_plan_demo.py   # 메인 프로그램
├── 기획안.md              # 서비스 기획안
├── 사용_가이드.md         # 상세 사용 가이드
└── README.md              # 프로젝트 소개
```

## 🔧 기술 스택

- Python 3.x
- 객체 지향 프로그래밍 (OOP)
- Harris-Benedict 방정식 (BMR 계산)
- 맞춤형 알고리즘 (운동 플랜 생성)

---

이 프로젝트는 GitHub 저장소와 연동되어 있습니다.

## GitHub 저장소 연동 방법

다음 명령어를 순서대로 실행하세요:

```bash
# 1. Git 저장소 초기화 (아직 초기화하지 않았다면)
git init

# 2. 원격 저장소 추가
git remote add origin https://github.com/wrtn-edu-swu-bootcamp/project_48.git

# 3. 파일 추가
git add .

# 4. 첫 커밋
git commit -m "Initial commit"

# 5. 원격 저장소로 푸시
git branch -M main
git push -u origin main
```

## 참고사항

- Git이 설치되어 있지 않다면 [Git 공식 사이트](https://git-scm.com/download/win)에서 다운로드하세요.
- 이미 원격 저장소에 파일이 있다면 `git pull origin main --allow-unrelated-histories` 명령어를 먼저 실행하세요.
