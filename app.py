"""
FitPlan AI - 웹 애플리케이션
Streamlit 기반 개인 맞춤형 운동 플랜 생성 서비스
"""

import streamlit as st
import plotly.graph_objects as go
from fitness_plan_demo import UserProfile, FitnessPlanGenerator

# 페이지 설정 (모바일 최적화)
st.set_page_config(
    page_title="FitPlan AI",
    page_icon="💪",
    layout="centered",  # 모바일에 최적화된 레이아웃
    initial_sidebar_state="collapsed"  # 사이드바 기본 접힘
)

# 커스텀 CSS (모바일 최적화)
st.markdown("""
    <style>
    /* 모바일 최적화 */
    .main {
        padding: 0.5rem;
        max-width: 100%;
    }
    
    /* 버튼 스타일 - 터치 친화적 */
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 1rem;
        font-size: 1rem;
        border-radius: 12px;
        font-weight: 600;
        touch-action: manipulation;
        min-height: 50px;
    }
    
    /* 텍스트 크기 조정 */
    body {
        font-size: 16px;
    }
    
    h1 {
        font-size: 1.8rem !important;
        line-height: 1.3;
    }
    
    h2 {
        font-size: 1.4rem !important;
        line-height: 1.3;
    }
    
    h3 {
        font-size: 1.2rem !important;
        line-height: 1.3;
    }
    
    /* 입력 필드 - 터치 친화적 */
    .stNumberInput input, .stSelectbox select, .stSlider, .stTextInput input {
        min-height: 50px !important;
        font-size: 16px !important;
        padding: 0.75rem !important;
        border-radius: 10px !important;
    }
    
    /* 라디오 버튼 - 모바일 최적화 */
    .stRadio > div {
        gap: 0.8rem;
    }
    
    .stRadio label {
        padding: 1rem !important;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        background-color: white;
        font-size: 1rem !important;
        margin: 0.3rem 0;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .stRadio label:hover {
        border-color: #4CAF50;
        background-color: #f1f8f4;
    }
    
    /* 멀티셀렉트 - 터치 친화적 */
    .stMultiSelect {
        font-size: 16px !important;
    }
    
    /* 폼 제출 버튼 */
    button[kind="formSubmit"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-size: 1.2rem !important;
        padding: 1.2rem !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        margin-top: 1rem !important;
        min-height: 60px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* 토글 스위치 크기 증가 */
    .stCheckbox, .stToggle {
        font-size: 1rem !important;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.8rem 1rem;
        font-size: 0.9rem;
        white-space: nowrap;
    }
    
    /* Expander 스타일 */
    .streamlit-expanderHeader {
        font-size: 1rem !important;
        padding: 1rem !important;
    }
    
    /* 박스 스타일 */
    .success-box, .info-box, .warning-box {
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        font-size: 0.95rem;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
    }
    
    /* 메트릭 스타일 */
    [data-testid="stMetricValue"] {
        font-size: 1.2rem;
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    [data-testid="stSidebar"] .stButton>button {
        min-height: 44px;
    }
    
    /* 여백 조정 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* 모바일 전용 스타일 */
    @media (max-width: 768px) {
        .main {
            padding: 0.3rem;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.2rem !important;
        }
        
        /* 컬럼 간격 */
        [data-testid="column"] {
            padding: 0.3rem !important;
        }
        
        /* Plotly 차트 높이 조정 */
        .js-plotly-plot {
            height: 100px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown("""
    <h1 style='text-align: center; color: #2E86AB;'>
        💪 FitPlan AI
    </h1>
    <h3 style='text-align: center; color: #666;'>
        개인 맞춤형 운동 플랜 생성 서비스
    </h3>
    <hr>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'plan_generated' not in st.session_state:
    st.session_state.plan_generated = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'health_conditions' not in st.session_state:
    st.session_state.health_conditions = []
if 'show_input_form' not in st.session_state:
    st.session_state.show_input_form = True

# 입력 폼 데이터 초기화
if 'height' not in st.session_state:
    st.session_state.height = 164
if 'weight' not in st.session_state:
    st.session_state.weight = 57.0
if 'age' not in st.session_state:
    st.session_state.age = 25
if 'gender' not in st.session_state:
    st.session_state.gender = "여성"
if 'goal' not in st.session_state:
    st.session_state.goal = "체중 감량"
if 'environment' not in st.session_state:
    st.session_state.environment = "헬스장"
if 'frequency' not in st.session_state:
    st.session_state.frequency = 4
if 'duration' not in st.session_state:
    st.session_state.duration = 60

# 메인 콘텐츠 - 입력 폼 또는 결과 화면
if not st.session_state.plan_generated or st.session_state.show_input_form:
    # 모바일 스타일 입력 폼
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 1.5rem;'>
            <h2 style='color: white; margin: 0;'>💪 맞춤 운동 플랜</h2>
            <p style='color: white; margin: 0.5rem 0 0 0; opacity: 0.9;'>나만의 건강 파트너</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 폼 시작
    with st.form("user_info_form"):
        st.markdown("### 1️⃣ 신체 정보")
        
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("키 (cm)", min_value=100, max_value=250, value=st.session_state.height, step=1, key="form_height")
        with col2:
            weight = st.number_input("몸무게 (kg)", min_value=30.0, max_value=200.0, value=st.session_state.weight, step=0.1, key="form_weight")
        
        col3, col4 = st.columns(2)
        with col3:
            age = st.number_input("나이", min_value=10, max_value=100, value=st.session_state.age, step=1, key="form_age")
        with col4:
            gender = st.selectbox("성별", ["여성", "남성"], index=0 if st.session_state.gender=="여성" else 1, key="form_gender")
        
        st.markdown("---")
        st.markdown("### 2️⃣ 추가 정보 (선택)")
        
        has_body_fat = st.toggle("체지방률 입력하기", key="toggle_bf")
        body_fat = None
        if has_body_fat:
            body_fat = st.number_input("체지방률 (%)", min_value=5.0, max_value=50.0, value=26.0, step=0.1, key="form_bf")
        
        has_muscle = st.toggle("골격근량 입력하기", key="toggle_muscle")
        skeletal_muscle = None
        if has_muscle:
            skeletal_muscle = st.number_input("골격근량 (kg)", min_value=10.0, max_value=100.0, value=25.0, step=0.1, key="form_muscle")
        
        st.markdown("---")
        st.markdown("### 3️⃣ 운동 목표")
        
        goal = st.radio(
            "목표를 선택하세요",
            ["체중 감량", "근육 증가", "체중 감량 + 근육 증가", "체력 향상", "건강 유지"],
            index=["체중 감량", "근육 증가", "체중 감량 + 근육 증가", "체력 향상", "건강 유지"].index(st.session_state.goal),
            key="form_goal",
            horizontal=False
        )
        
        st.markdown("---")
        st.markdown("### 4️⃣ 운동 환경")
        
        environment = st.radio(
            "운동 장소를 선택하세요",
            ["헬스장", "홈트레이닝 (장비 있음)", "홈트레이닝 (장비 없음)"],
            index=["헬스장", "홈트레이닝 (장비 있음)", "홈트레이닝 (장비 없음)"].index(st.session_state.environment),
            key="form_environment",
            horizontal=False
        )
        
        st.markdown("---")
        st.markdown("### 5️⃣ 운동 계획")
        
        st.write("**주간 운동 빈도**")
        frequency = st.select_slider(
            "일주일에 며칠 운동하시나요?",
            options=[3, 4, 5, 6, 7],
            value=st.session_state.frequency,
            key="form_frequency",
            label_visibility="collapsed"
        )
        st.caption(f"✅ 주 {frequency}회 운동")
        
        st.write("**1회 운동 시간**")
        duration = st.select_slider(
            "한 번에 얼마나 운동하시나요?",
            options=[30, 40, 50, 60, 75, 90, 105, 120],
            value=st.session_state.duration,
            key="form_duration",
            label_visibility="collapsed"
        )
        st.caption(f"✅ 1회 {duration}분")
        
        st.markdown("---")
        st.markdown("### 6️⃣ 건강 상태 (선택)")
        
        st.caption("해당하는 건강 상태가 있으면 선택하세요")
        health_conditions = st.multiselect(
            "건강 상태",
            ["저혈당", "당뇨병", "저혈압", "고혈압", "심장 질환", "천식"],
            default=[],
            key="form_health",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 7️⃣ 통증 부위 (선택)")
        
        st.caption("통증이 있는 부위를 선택하세요")
        pain_areas = st.multiselect(
            "통증 부위",
            ["목/어깨", "허리", "무릎", "손목", "팔꿈치", "발목"],
            default=[],
            key="form_pain",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 제출 버튼 (모바일 친화적)
        submitted = st.form_submit_button("🎯 맞춤 플랜 생성하기", use_container_width=True)
        
        if submitted:
            with st.spinner("✨ 맞춤형 운동 플랜을 생성하고 있습니다..."):
                # 세션 상태에 입력값 저장
                st.session_state.height = height
                st.session_state.weight = weight
                st.session_state.age = age
                st.session_state.gender = gender
                st.session_state.goal = goal
                st.session_state.environment = environment
                st.session_state.frequency = frequency
                st.session_state.duration = duration
                
                # 사용자 프로필 생성
                user = UserProfile(
                    height=height,
                    weight=weight,
                    age=age,
                    gender=gender,
                    body_fat_percentage=body_fat,
                    skeletal_muscle_mass=skeletal_muscle
                )
                
                # 플랜 생성기 초기화
                planner = FitnessPlanGenerator(user, goal, environment, frequency, duration, pain_areas, health_conditions)
                
                # 세션 상태에 저장
                st.session_state.user_profile = user
                st.session_state.planner = planner
                st.session_state.pain_areas = pain_areas
                st.session_state.health_conditions = health_conditions
                st.session_state.recommendations = planner.recommend_goal()
                st.session_state.weekly_plan = planner.generate_weekly_plan()
                st.session_state.plan_generated = True
                st.session_state.show_input_form = False
                
                st.success("✅ 플랜이 생성되었습니다!")
                st.rerun()
    
    # 하단 안내 메시지
    st.markdown("""
        <div style='text-align: center; padding: 1rem; margin-top: 2rem; color: #888;'>
            <p style='font-size: 0.9rem;'>💡 모든 정보는 안전하게 보관되며<br>언제든지 수정할 수 있습니다</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # 플랜이 생성된 경우 - 상단 버튼
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✏️ 정보 수정", use_container_width=True, type="secondary"):
            st.session_state.show_input_form = True
            st.rerun()
    with col_btn2:
        if st.button("🔄 완전 초기화", use_container_width=True, type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    user = st.session_state.user_profile
    planner = st.session_state.planner
    recommendations = st.session_state.recommendations
    weekly_plan = st.session_state.weekly_plan
    
    # 탭 생성
    tabs = ["📊 신체 분석", "💪 운동 플랜", "🍎 영양 가이드", "🍽️ 예시 식단"]
    if st.session_state.pain_areas:
        tabs.append("⚠️ 통증 주의사항")
    
    tab_objects = st.tabs(tabs)
    tab1, tab2, tab3, tab4 = tab_objects[:4]
    if len(tab_objects) > 4:
        tab5 = tab_objects[4]
    
    with tab1:
        st.header("📊 신체 구성 분석")
        
        # 기본 정보
        st.subheader("기본 정보")
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.write(f"**나이:** {user.age}세")
            st.write(f"**키:** {user.height}cm")
            st.write(f"**체지방률:** {user.body_fat_percentage}%")
        with col_info2:
            st.write(f"**성별:** {user.gender}")
            st.write(f"**몸무게:** {user.weight}kg")
            st.write(f"**골격근량:** {user.skeletal_muscle_mass}kg")
        
        st.markdown("---")
        
        # 분석 결과
        analysis = user.analyze_body_composition()
        st.subheader("분석 결과")
        
        # BMI
        st.markdown("**📏 체질량지수**")
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.metric("BMI", analysis["BMI"])
        with col2_2:
            st.metric("카테고리", analysis["BMI 카테고리"])
        
        st.markdown("---")
        
        # 체지방 관련
        st.markdown("**🔥 체지방 분석**")
        col2_3, col2_4 = st.columns(2)
        with col2_3:
            st.metric("체지방률", analysis["체지방률"])
            st.metric("제지방량", analysis["제지방량"])
        with col2_4:
            st.metric("카테고리", analysis["체지방률 카테고리"])
        
        st.markdown("---")
        
        # 골격근 관련
        st.markdown("**💪 골격근 분석**")
        col2_6, col2_7 = st.columns(2)
        with col2_6:
            st.metric("골격근량", analysis["골격근량"])
        with col2_7:
            st.metric("골격근 비율", analysis["골격근 비율"])
        
        st.markdown("---")
        
        # 인바디 스타일 그래프
        st.subheader("📈 체성분 분석 그래프 (InBody 스타일)")
        
        # 데이터 준비
        bmi = user.weight / ((user.height / 100) ** 2)
        body_fat = user.body_fat_percentage
        muscle_ratio = (user.skeletal_muscle_mass / user.weight) * 100
        
        # 성별에 따른 정상 범위
        if user.gender == "남성":
            bmi_ranges = {"낮음": (0, 18.5), "정상": (18.5, 25), "높음": (25, 40)}
            bf_ranges = {"낮음": (0, 10), "정상": (10, 20), "높음": (20, 50)}
            muscle_ranges = {"낮음": (0, 37), "정상": (37, 50), "높음": (50, 100)}
        else:  # 여성
            bmi_ranges = {"낮음": (0, 18.5), "정상": (18.5, 25), "높음": (25, 40)}
            bf_ranges = {"낮음": (0, 18), "정상": (18, 28), "높음": (28, 50)}
            muscle_ranges = {"낮음": (0, 30), "정상": (30, 45), "높음": (45, 100)}
        
        # 그래프 생성 함수
        def create_inbody_chart(value, ranges, title, unit, max_value):
            fig = go.Figure()
            
            # 배경 범위 추가 (낮음 - 노란색, 정상 - 초록색, 높음 - 빨간색)
            colors = {"낮음": "rgba(255, 193, 7, 0.3)", "정상": "rgba(76, 175, 80, 0.3)", "높음": "rgba(244, 67, 54, 0.3)"}
            
            for category, (start, end) in ranges.items():
                fig.add_trace(go.Bar(
                    y=[title],
                    x=[end - start],
                    base=[start],
                    orientation='h',
                    marker=dict(color=colors[category], line=dict(width=0)),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
            # 현재 값 막대
            bar_color = "rgba(33, 150, 243, 0.8)"  # 파란색
            if value < ranges["정상"][0]:
                bar_color = "rgba(255, 152, 0, 0.9)"  # 주황색 (낮음)
            elif value > ranges["정상"][1]:
                bar_color = "rgba(244, 67, 54, 0.9)"  # 빨간색 (높음)
            else:
                bar_color = "rgba(76, 175, 80, 0.9)"  # 초록색 (정상)
            
            fig.add_trace(go.Bar(
                y=[title],
                x=[value],
                orientation='h',
                marker=dict(color=bar_color, line=dict(width=2, color='white')),
                text=[f"{value:.1f}{unit}"],
                textposition='outside',
                textfont=dict(size=12, color='black', family='Arial Black'),  # 모바일에 맞게 텍스트 크기 축소
                showlegend=False,
                hovertemplate=f'<b>{title}</b><br>현재 값: {value:.1f}{unit}<extra></extra>'
            ))
            
            # 레이아웃 설정 (모바일 최적화)
            fig.update_layout(
                title=dict(
                    text=f"<b>{title}</b>",
                    font=dict(size=14, color='#333'),
                    x=0.01,
                    xanchor='left',
                    y=0.95,
                    yanchor='top'
                ),
                barmode='overlay',
                height=120,  # 제목 공간을 위해 높이 약간 증가
                margin=dict(l=5, r=5, t=30, b=5),  # 상단 여백 증가
                xaxis=dict(
                    range=[0, max_value],
                    showgrid=True,
                    gridcolor='lightgray',
                    zeroline=False,
                    showticklabels=True,
                    tickfont=dict(size=9)
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Arial', size=11)
            )
            
            return fig
        
        # BMI 그래프
        st.plotly_chart(
            create_inbody_chart(bmi, bmi_ranges, "BMI (체질량지수)", "", 40),
            use_container_width=True,
            config={'displayModeBar': False}
        )
        
        # 체지방률 그래프
        st.plotly_chart(
            create_inbody_chart(body_fat, bf_ranges, "체지방률", "%", 50),
            use_container_width=True,
            config={'displayModeBar': False}
        )
        
        # 골격근 비율 그래프
        st.plotly_chart(
            create_inbody_chart(muscle_ratio, muscle_ranges, "골격근 비율", "%", 100),
            use_container_width=True,
            config={'displayModeBar': False}
        )
        
        # 범례 추가
        st.caption("🟨 낮음  |  🟩 정상  |  🟥 높음")
        
        st.markdown("---")
        
        # AI 추천 목표
        if recommendations:
            st.subheader("🎯 AI 추천 목표")
            for idx, rec in enumerate(recommendations, 1):
                with st.expander(f"{idx}. {rec['목표']} - 우선순위: {rec['우선순위']}"):
                    st.write(f"**이유:** {rec['이유']}")
    
    with tab2:
        st.header("💪 맞춤형 주간 운동 플랜")
        
        st.info(f"""
        **🎯 운동 목표:** {weekly_plan['목표']}  
        **🏋️ 운동 환경:** {weekly_plan['운동_환경']}  
        **📅 주간 운동일:** {weekly_plan['주간_운동일']}일  
        **⏱ 1회 운동 시간:** {weekly_plan['운동_시간']}
        """)
        
        # 건강 상태 안내사항 표시
        if st.session_state.get('health_conditions'):
            st.markdown("---")
            st.subheader("⚠️ 건강 상태별 운동 주의사항")
            
            precautions = planner.get_medical_precautions()
            
            for condition in st.session_state.health_conditions:
                if condition in precautions:
                    prec = precautions[condition]
                    
                    with st.expander(f"💊 {condition}", expanded=True):
                        # 주요 주의사항 (간략하게)
                        st.warning("**⚠️ 주의사항:**")
                        for item in prec["주의사항"][:3]:  # 상위 3개만 표시
                            st.write(f"• {item}")
                        
                        # 운동 전 섭취 (저혈당/당뇨병의 경우)
                        if "운동_전_섭취" in prec:
                            st.success("**🍎 운동 전 섭취 권장:**")
                            for item in prec["운동_전_섭취"]:
                                st.write(f"• {item}")
                        
                        # 더 자세한 정보는 접기 가능
                        with st.expander("📋 상세 정보 보기"):
                            st.markdown("**✅ 권장 운동:**")
                            for exercise in prec["권장_운동"]:
                                st.write(f"✓ {exercise}")
                            
                            st.markdown("**🚫 피해야 할 운동:**")
                            for exercise in prec["피할_운동"]:
                                st.write(f"✗ {exercise}")
            
            st.markdown("---")
        
        # Day 1 운동 계획 - 하루 일정표 형식
        if len(weekly_plan['주간_계획']) > 0:
            day_plan = weekly_plan['주간_계획'][0]
            st.subheader(f"📌 Day 1 - {day_plan['요일']}: {day_plan['주제']}")
            
            # 운동 순서 안내
            st.info("""
            **⏰ 운동 순서 가이드**
            1️⃣ 워밍업 (5-10분) → 2️⃣ 근력 운동 (대근육 먼저) → 3️⃣ 유산소 운동 → 4️⃣ 쿨다운 (5-10분)
            
            💡 **왜 이 순서일까요?**
            - **근력 먼저**: 에너지가 충분할 때 중량 운동을 해야 부상 위험이 적고 효과적입니다
            - **대근육 먼저**: 하체/등/가슴 같은 큰 근육 → 어깨/팔 같은 작은 근육 순서
            - **유산소 나중**: 근력 운동 후 유산소를 하면 지방 연소가 더 효과적입니다
            """)
            
            st.markdown("---")
            
            # 1️⃣ 워밍업
            st.markdown("### 1️⃣ 워밍업 (5-10분)")
            st.write("""
            **🔥 가벼운 유산소 + 동적 스트레칭**
            - 런닝머신 걷기 (속도 4-5 km/h) 5분
            - 팔 돌리기, 다리 스윙, 몸통 비틀기 등 동적 스트레칭
            - 관절을 풀고 체온을 높여 부상을 예방합니다
            """)
            
            st.markdown("---")
            
            # 2️⃣ 근력 운동
            st.markdown("### 2️⃣ 근력 운동 (대근육 → 소근육 순서)")
            st.caption("큰 근육부터 운동하면 더 많은 에너지를 사용하고 성장 호르몬 분비가 활발합니다")
            
            # 운동을 대근육/소근육으로 분류
            large_muscle_exercises = []
            small_muscle_exercises = []
            
            # 대근육 운동 키워드
            large_muscle_keywords = ['스쿼트', '데드리프트', '레그 프레스', '런지', '벤치 프레스', '풀업', '친업', 
                                     '랫 풀다운', '로우', '힙 쓰러스트', '프론트 스쿼트']
            
            for exercise in day_plan['운동']:
                if "횟수" in exercise:
                    is_large = any(keyword in exercise['이름'] for keyword in large_muscle_keywords)
                    if is_large:
                        large_muscle_exercises.append(exercise)
                    else:
                        small_muscle_exercises.append(exercise)
            
            # 대근육 운동 표시
            if large_muscle_exercises:
                st.markdown("**💪 대근육 운동 (하체, 가슴, 등)**")
                for idx, exercise in enumerate(large_muscle_exercises, 1):
                    st.write(f"**{idx}. {exercise['이름']}**")
                    
                    # 권장 무게 가져오기
                    weights = planner.get_weight_recommendation(exercise['이름'])
                    if weights:
                        st.write(f"   - {exercise['세트']}세트 × {exercise['횟수']}, 휴식 {exercise['휴식']}")
                        st.caption(f"      💡 권장 무게: 초급 {weights['초급']}kg / 중급 {weights['중급']}kg / 고급 {weights['고급']}kg")
                    else:
                        st.write(f"   - {exercise['세트']}세트 × {exercise['횟수']}, 휴식 {exercise['휴식']}")
                    st.write("")
            
            # 소근육 운동 표시
            if small_muscle_exercises:
                st.markdown("**🎯 소근육 운동 (어깨, 팔, 코어)**")
                for idx, exercise in enumerate(small_muscle_exercises, 1):
                    st.write(f"**{idx}. {exercise['이름']}**")
                    
                    # 권장 무게 가져오기
                    weights = planner.get_weight_recommendation(exercise['이름'])
                    if weights:
                        st.write(f"   - {exercise['세트']}세트 × {exercise['횟수']}, 휴식 {exercise['휴식']}")
                        st.caption(f"      💡 권장 무게: 초급 {weights['초급']}kg / 중급 {weights['중급']}kg / 고급 {weights['고급']}kg")
                    else:
                        st.write(f"   - {exercise['세트']}세트 × {exercise['횟수']}, 휴식 {exercise['휴식']}")
                    st.write("")
            
            # 근력 운동이 없는 경우 (전부 표시)
            if not large_muscle_exercises and not small_muscle_exercises:
                for exercise in day_plan['운동']:
                    if "횟수" in exercise:
                        st.write(f"✓ **{exercise['이름']}**")
                        weights = planner.get_weight_recommendation(exercise['이름'])
                        if weights:
                            st.write(f"   - {exercise['세트']}세트 × {exercise['횟수']}, 휴식 {exercise['휴식']}")
                            st.caption(f"      💡 권장 무게: 초급 {weights['초급']}kg / 중급 {weights['중급']}kg / 고급 {weights['고급']}kg")
                        else:
                            st.write(f"   - {exercise['세트']}세트 × {exercise['횟수']}, 휴식 {exercise['휴식']}")
                    elif "시간" in exercise and "라운드" in exercise:
                        st.write(f"✓ **{exercise['이름']}**")
                        st.write(f"   - {exercise['라운드']}라운드, 총 {exercise['총시간']}")
                    elif "시간" in exercise:
                        intensity = f", 강도: {exercise['강도']}" if "강도" in exercise else ""
                        st.write(f"✓ **{exercise['이름']}**")
                        st.write(f"   - 시간: {exercise['시간']}{intensity}")
                    st.write("")
            
            st.markdown("---")
            
            # 운동 방법 영상 가이드
            st.subheader("🎬 운동 방법 영상 가이드")
            st.caption("각 운동의 올바른 자세와 방법을 유튜브 영상으로 확인하세요")
            
            # Day 1의 운동들에 대한 영상 링크 수집
            exercise_videos = []
            
            for exercise in day_plan['운동']:
                exercise_name = exercise['이름']
                # FitnessPlanGenerator의 EXERCISE_VIDEOS에서 링크 가져오기
                if exercise_name in planner.EXERCISE_VIDEOS:
                    exercise_videos.append({
                        'name': exercise_name,
                        'url': planner.EXERCISE_VIDEOS[exercise_name]
                    })
            
            if exercise_videos:
                # 영상 링크를 버튼 형태로 표시
                for idx, video in enumerate(exercise_videos):
                    col_vid1, col_vid2 = st.columns([3, 1])
                    with col_vid1:
                        st.write(f"**{idx+1}. {video['name']}**")
                    with col_vid2:
                        st.link_button("📺 영상보기", video['url'], use_container_width=True)
            else:
                st.info("운동 영상 링크가 준비 중입니다.")
            
            st.markdown("---")
            
            # 3️⃣ 유산소 운동
            st.markdown("### 3️⃣ 유산소 운동 (20-30분)")
            cardio = planner.get_cardio_details()
            st.write(f"""
            **🏃 {cardio['유형']}**
            - 권장 시간: {cardio['권장_시간']}
            - 목표 심박수: {cardio['목표_심박수']}
            - 강도: {cardio['강도']}
            
            💡 근력 운동 후 유산소를 하면 글리코겐이 소진된 상태라 지방 연소가 더 효과적입니다!
            """)
            
            st.markdown("---")
            
            # 4️⃣ 쿨다운
            st.markdown("### 4️⃣ 쿨다운 (5-10분)")
            st.write("""
            **❄️ 가벼운 유산소 + 정적 스트레칭**
            - 걷기 또는 가벼운 사이클 5분
            - 정적 스트레칭 (각 부위 20-30초씩)
            - 심박수를 서서히 낮추고 근육 회복을 돕습니다
            - 스트레칭은 운동한 부위를 중심으로!
            """)
        
        # 유산소 운동 가이드
        st.markdown("---")
        st.subheader("🏃 유산소 운동 가이드")
        
        cardio = planner.get_cardio_details()
        
        # 런닝머신 기준 운동 강도 추출
        equipment_details = cardio.get('기구별_상세설정', {})
        treadmill_info = None
        if "트레드밀 (런닝머신)" in equipment_details:
            treadmill_info = equipment_details["트레드밀 (런닝머신)"]
        elif "트레드밀" in equipment_details:
            treadmill_info = equipment_details["트레드밀"]
        elif "트레드밀 인터벌" in equipment_details:
            treadmill_info = equipment_details["트레드밀 인터벌"]
        
        # 런닝머신 기준 강도 표시
        if treadmill_info:
            st.info(f"""
            **🎯 목표:** {planner.goal}  
            **📊 최대 심박수:** {cardio['최대_심박수']}  
            **💓 목표 심박수:** {cardio['목표_심박수']}  
            **🏃 런닝머신 기준 (중급자):** {treadmill_info['중급']}
            """)
        else:
            st.info(f"""
            **🎯 목표:** {planner.goal}  
            **📊 최대 심박수:** {cardio['최대_심박수']}  
            **💓 목표 심박수:** {cardio['목표_심박수']}  
            **⚡ 강도:** {cardio['강도']}
            """)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("**🏋️ 유형**")
            st.write(cardio['유형'])
            
            st.markdown("**⏱ 권장 시간**")
            st.write(cardio['권장_시간'])
        
        with col_c2:
            st.markdown("**📝 설명**")
            st.write(cardio['설명'])
        
        st.markdown("---")
        st.subheader("🎯 기구별 구체적인 운동 설정")
        st.caption("본인의 체력 수준에 맞는 단계를 선택하세요")
        
        # 기구별 상세 설정 표시 (런닝머신 우선)
        equipment_details = cardio.get('기구별_상세설정', {})
        
        # 런닝머신 관련 키를 찾아서 먼저 표시
        treadmill_keys = [key for key in equipment_details.keys() if '트레드밀' in key or '런닝머신' in key]
        other_keys = [key for key in equipment_details.keys() if key not in treadmill_keys]
        
        # 런닝머신 먼저 표시 (펼쳐진 상태)
        for equipment_name in treadmill_keys:
            settings = equipment_details[equipment_name]
            with st.expander(f"🏃 {equipment_name}", expanded=True):
                st.markdown(f"**🟢 초급자 (운동 경험 3개월 미만)**")
                st.info(settings['초급'])
                
                st.markdown(f"**🟡 중급자 (운동 경험 3-12개월)**")
                st.info(settings['중급'])
                
                st.markdown(f"**🔴 고급자 (운동 경험 1년 이상)**")
                st.info(settings['고급'])
                
                st.success(f"**💡 팁:** {settings['팁']}")
        
        # 나머지 기구 표시 (접힌 상태)
        for equipment_name in other_keys:
            settings = equipment_details[equipment_name]
            with st.expander(f"💪 {equipment_name}", expanded=False):
                st.markdown(f"**🟢 초급자 (운동 경험 3개월 미만)**")
                st.info(settings['초급'])
                
                st.markdown(f"**🟡 중급자 (운동 경험 3-12개월)**")
                st.info(settings['중급'])
                
                st.markdown(f"**🔴 고급자 (운동 경험 1년 이상)**")
                st.info(settings['고급'])
                
                st.success(f"**💡 팁:** {settings['팁']}")
        
        st.markdown("---")
        st.subheader("💡 유산소 운동 팁")
        
        if "체중 감량" in planner.goal and "근육 증가" not in planner.goal:
            st.warning("""
            **체중 감량 유산소:**
            - 대화가 가능한 정도의 강도 유지
            - 너무 힘들면 지방 대신 근육이 분해됩니다
            - 일정한 페이스로 오래 하는 것이 중요
            - 아침 공복 유산소가 효과적 (선택)
            - 심박수 모니터링으로 목표 구간 유지
            """)
        else:
            st.warning("""
            **HIIT (고강도 인터벌):**
            - 전력 질주 20-30초 + 휴식 30-60초 반복
            - 땀이 많이 나고 숨이 가쁜 것이 정상
            - 주 2-3회가 적당 (과훈련 주의)
            - 기초대사량 증가 효과 (운동 후 24-48시간)
            - 워밍업/쿨다운 각 5분씩 필수
            """)
        
        # Day 2부터의 나머지 운동 계획
        if len(weekly_plan['주간_계획']) > 1:
            st.markdown("---")
            st.subheader("📅 나머지 주간 운동 계획")
            
            for idx, day_plan in enumerate(weekly_plan['주간_계획'][1:], 2):
                with st.expander(f"📌 Day {idx} - {day_plan['요일']}: {day_plan['주제']}"):
                    for exercise in day_plan['운동']:
                        if "횟수" in exercise:
                            st.write(f"✓ **{exercise['이름']}**")
                            
                            # 권장 무게 가져오기
                            weights = planner.get_weight_recommendation(exercise['이름'])
                            if weights:
                                st.write(f"   - {exercise['세트']}세트 × {exercise['횟수']}, 휴식 {exercise['휴식']}")
                                st.caption(f"      💡 권장 무게: 초급 {weights['초급']}kg / 중급 {weights['중급']}kg / 고급 {weights['고급']}kg")
                            else:
                                st.write(f"   - {exercise['세트']}세트 × {exercise['횟수']}, 휴식 {exercise['휴식']}")
                                
                        elif "시간" in exercise and "라운드" in exercise:
                            st.write(f"✓ **{exercise['이름']}**")
                            st.write(f"   - {exercise['라운드']}라운드, 총 {exercise['총시간']}")
                        elif "시간" in exercise:
                            intensity = f", 강도: {exercise['강도']}" if "강도" in exercise else ""
                            st.write(f"✓ **{exercise['이름']}**")
                            st.write(f"   - 시간: {exercise['시간']}{intensity}")
                        st.write("")
        
        # 용어 설명과 심박수 측정 방법
        st.markdown("---")
        st.subheader("📖 용어 설명")
        
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.markdown("""
            **RPM** (Revolutions Per Minute)  
            분당 회전수 - 사이클에서 페달을 밟는 속도
            """)
        with col_t2:
            st.markdown("""
            **SPM** (Strokes Per Minute)  
            분당 스트로크 수 - 로잉머신에서 당기는 횟수
            """)
        with col_t3:
            st.markdown("""
            **인클라인**  
            런닝머신 경사도 (% 또는 각도)
            """)
        
        st.markdown("---")
        st.subheader("📌 심박수 측정 방법")
        st.success("""
        1. **스마트워치/밴드** 착용
        2. **운동 기구** 내장 심박수 센서
        3. **목이나 손목** 맥박 직접 측정 (15초 × 4)
        4. **자각적 강도 (RPE)**: 10점 만점에 7-8점 수준
        """)
        
        # 무게 선택 가이드
        st.markdown("---")
        st.subheader("💡 무게 선택 팁")
        
        st.info(f"""
        **💪 성별:** {user.gender} | **📊 체중:** {user.weight}kg | **🎯 권장 반복 횟수:** {planner.rep_description}
        
        💡 각 운동마다 권장 무게가 표시됩니다. 본인의 체력 수준에 맞게 선택하세요.
        """)
        
        if user.gender == "남성":
            st.success("""
            **남성 (고강도 저반복):**
            - 목표 반복 횟수의 마지막 1-2개가 힘들어야 합니다
            - 세트 마지막에 더 이상 들 수 없는 무게가 적절합니다
            - 근력 증가가 목표라면 더 무거운 무게로 도전하세요
            """)
        else:
            st.success("""
            **여성 (저강도 고반복):**
            - 목표 반복 횟수를 완료할 수 있되, 마지막 2-3개가 약간 힘들어야 합니다
            - 세트 후 2-3회 더 할 수 있는 정도의 무게가 적절합니다
            - 근지구력과 탄탄한 근육 라인이 목표입니다
            """)
        
        st.info("""
        **공통 원칙:**
        - 처음에는 가벼운 무게로 시작하여 자세를 익히세요
        - 매주 2.5-5kg씩 점진적으로 증가시키세요
        - 자세가 흐트러지면 무게를 줄이세요
        - 위 무게는 참고용이며, 개인 체력에 맞게 조절하세요
        """)
    
    with tab3:
        st.header("🍎 맞춤 영양 가이드")
        
        # BMR, TDEE 계산
        weight = user.weight
        height = user.height
        age = user.age
        
        if user.gender == "남성":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        activity_multipliers = {3: 1.375, 4: 1.55, 5: 1.725, 6: 1.9, 7: 1.9}
        tdee = bmr * activity_multipliers.get(planner.frequency, 1.55)
        
        # 목표에 따른 칼로리 조정
        if "체중 감량" in planner.goal and "근육 증가" not in planner.goal:
            target_cal = tdee - 500
            calorie_note = "체중 감량을 위한 칼로리 적자"
        elif "근육 증가" in planner.goal and "체중 감량" not in planner.goal:
            target_cal = tdee + 300
            calorie_note = "근육 증가를 위한 칼로리 흑자"
        elif "체중 감량 + 근육 증가" in planner.goal:
            target_cal = tdee - 200
            calorie_note = "바디 리컴포지션"
        else:
            target_cal = tdee
            calorie_note = "체중 유지"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("기초 대사량 (BMR)", f"{int(bmr)} kcal/일")
        with col2:
            st.metric("총 에너지 소비 (TDEE)", f"{int(tdee)} kcal/일")
        with col3:
            st.metric("목표 섭취 칼로리", f"{int(target_cal)} kcal/일")
        
        st.info(f"**💡 {calorie_note}**")
        
        st.markdown("---")
        
        # 영양소 비율
        if "근육 증가" in planner.goal:
            protein_min = weight * 1.8
            protein_max = weight * 2.2
        else:
            protein_min = weight * 1.6
            protein_max = weight * 2.0
        
        if "체중 감량" in planner.goal:
            carb_ratio = 2.0
            fat_ratio = 0.8
        elif "근육 증가" in planner.goal:
            carb_ratio = 4.0
            fat_ratio = 1.0
        else:
            carb_ratio = 3.0
            fat_ratio = 0.9
        
        st.subheader("🥗 영양소 비율")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("단백질", f"{round(protein_min, 1)}-{round(protein_max, 1)}g/일")
            st.caption(f"체중 1kg당 {round(protein_min/weight, 1)}-{round(protein_max/weight, 1)}g")
        
        with col2:
            st.metric("탄수화물", f"{round(weight * carb_ratio, 1)}-{round(weight * (carb_ratio + 0.5), 1)}g/일")
        
        with col3:
            st.metric("지방", f"{round(weight * fat_ratio, 1)}-{round(weight * (fat_ratio + 0.2), 1)}g/일")
        
        st.markdown("---")
        
        st.metric("💧 수분 섭취", f"최소 {round(weight * 0.035, 1)}L/일")
        st.caption("체중 1kg당 35ml")
        
        # 영양 팁
        if "체중 감량" in planner.goal:
            st.markdown("""
                **📌 영양 섭취 팁:**
                - 고단백, 저지방 식품 위주 (닭가슴살, 생선, 두부)
                - 복합 탄수화물 선택 (현미, 고구마, 귀리)
                - 채소를 많이 섭취하여 포만감 유지
            """)
        elif "근육 증가" in planner.goal:
            st.markdown("""
                **📌 영양 섭취 팁:**
                - 운동 전후 단백질 + 탄수화물 섭취
                - 하루 5-6끼로 나눠 먹기
                - 양질의 지방 섭취 (견과류, 아보카도, 올리브유)
            """)
    
    with tab4:
        st.header("🍽️ 예시 식단")
        
        # 목표에 따른 칼로리 계산
        weight = user.weight
        height = user.height
        age = user.age
        gender = user.gender
        
        if gender == "남성":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        activity_multipliers = {3: 1.375, 4: 1.55, 5: 1.725, 6: 1.9, 7: 1.9}
        tdee = bmr * activity_multipliers.get(frequency, 1.55)
        
        if "체중 감량" in goal and "근육 증가" not in goal:
            target_cal = tdee - 500
            meal_type = "체중 감량"
        elif "근육 증가" in goal and "체중 감량" not in goal:
            target_cal = tdee + 300
            meal_type = "근육 증가"
        elif "체중 감량 + 근육 증가" in goal:
            target_cal = tdee - 200
            meal_type = "체중 감량 + 근육 증가"
        else:
            target_cal = tdee
            meal_type = "체중 유지"
        
        st.info(f"""
        **🎯 목표:** {meal_type}  
        **📊 목표 칼로리:** 약 {int(target_cal)}kcal/일
        """)
        
        # 목표에 따른 식단 표시
        if meal_type == "체중 감량":
            st.subheader("예시 하루 식단 (체중 감량)")
            
            with st.expander("🌅 아침 (약 400kcal)", expanded=True):
                st.markdown("""
                - 현미밥 1/2공기 (150kcal)
                - 계란 2개 (삶은 계란 또는 스크램블) (140kcal)
                - 김치찌개 1인분 (80kcal)
                - 샐러드 (오이, 토마토, 양상추) (30kcal)
                
                **➜ 단백질 20g, 탄수화물 45g, 지방 8g**
                """)
            
            with st.expander("☀️ 점심 (약 500kcal)"):
                st.markdown("""
                - 닭가슴살 샐러드 200g (200kcal)
                - 고구마 중 1개 (150g) (150kcal)
                - 브로콜리 100g (30kcal)
                - 올리브유 드레싱 1스푼 (120kcal)
                
                **➜ 단백질 35g, 탄수화물 40g, 지방 14g**
                """)
            
            with st.expander("🌙 저녁 (약 450kcal)"):
                st.markdown("""
                - 현미밥 1/2공기 (150kcal)
                - 생선구이 (고등어 또는 연어) 150g (250kcal)
                - 된장찌개 1인분 (50kcal)
                
                **➜ 단백질 30g, 탄수화물 35g, 지방 12g**
                """)
            
            with st.expander("🍎 간식 (약 200kcal)"):
                st.markdown("""
                - 그릭요거트 무지방 150g (100kcal)
                - 아몬드 10알 (70kcal)
                - 사과 1/2개 (30kcal)
                
                **➜ 단백질 12g, 탄수화물 15g, 지방 8g**
                """)
            
            st.success("**📊 하루 총계:** 약 1,550kcal | 단백질: 97g | 탄수화물: 135g | 지방: 42g")
        
        elif meal_type == "근육 증가":
            st.subheader("예시 하루 식단 (근육 증가)")
            
            with st.expander("🌅 아침 (약 550kcal)", expanded=True):
                st.markdown("""
                - 현미밥 1공기 (300kcal)
                - 계란 3개 (210kcal)
                - 김치찌개 1인분 (80kcal)
                
                **➜ 단백질 28g, 탄수화물 60g, 지방 12g**
                """)
            
            with st.expander("☀️ 점심 (약 700kcal)"):
                st.markdown("""
                - 현미밥 1공기 (300kcal)
                - 닭가슴살 200g (220kcal)
                - 고구마 중 1개 (150kcal)
                - 샐러드 (30kcal)
                
                **➜ 단백질 50g, 탄수화물 85g, 지방 8g**
                """)
            
            with st.expander("🌙 저녁 (약 650kcal)"):
                st.markdown("""
                - 현미밥 1공기 (300kcal)
                - 소고기 등심 150g (300kcal)
                - 된장찌개 1인분 (50kcal)
                
                **➜ 단백질 40g, 탄수화물 55g, 지방 18g**
                """)
            
            with st.expander("🍎 간식/운동 전후 (약 500kcal)"):
                st.markdown("""
                - 단백질 쉐이크 (30g 단백질) (150kcal)
                - 바나나 2개 (200kcal)
                - 땅콩버터 2스푼 (150kcal)
                
                **➜ 단백질 35g, 탄수화물 55g, 지방 12g**
                """)
            
            st.success("**📊 하루 총계:** 약 2,400kcal | 단백질: 153g | 탄수화물: 255g | 지방: 50g")
        
        elif meal_type == "체중 감량 + 근육 증가":
            st.subheader("예시 하루 식단 (바디 리컴포지션)")
            
            with st.expander("🌅 아침 (약 450kcal)", expanded=True):
                st.markdown("""
                - 현미밥 2/3공기 (200kcal)
                - 계란 2개 + 계란흰자 2개 (160kcal)
                - 김치찌개 1인분 (80kcal)
                - 방울토마토 10개 (10kcal)
                
                **➜ 단백질 25g, 탄수화물 50g, 지방 10g**
                """)
            
            with st.expander("☀️ 점심 (약 550kcal)"):
                st.markdown("""
                - 현미밥 2/3공기 (200kcal)
                - 닭가슴살 150g (165kcal)
                - 고구마 중 1개 (150kcal)
                - 샐러드 + 발사믹 드레싱 (35kcal)
                
                **➜ 단백질 40g, 탄수화물 65g, 지방 6g**
                """)
            
            with st.expander("🌙 저녁 (약 500kcal)"):
                st.markdown("""
                - 현미밥 2/3공기 (200kcal)
                - 생선구이 (연어) 150g (250kcal)
                - 된장찌개 1인분 (50kcal)
                
                **➜ 단백질 35g, 탄수화물 45g, 지방 14g**
                """)
            
            with st.expander("🍎 간식 (약 300kcal)"):
                st.markdown("""
                - 그릭요거트 무지방 200g (130kcal)
                - 프로틴바 1개 (150kcal)
                - 블루베리 한줌 (20kcal)
                
                **➜ 단백질 25g, 탄수화물 25g, 지방 8g**
                """)
            
            st.success("**📊 하루 총계:** 약 1,800kcal | 단백질: 125g | 탄수화물: 185g | 지방: 38g")
        
        else:  # 체중 유지
            st.subheader("예시 하루 식단 (체중 유지 / 건강 관리)")
            
            with st.expander("🌅 아침 (약 500kcal)", expanded=True):
                st.markdown("""
                - 현미밥 1공기 (300kcal)
                - 계란 2개 (140kcal)
                - 김치찌개 1인분 (80kcal)
                
                **➜ 단백질 22g, 탄수화물 55g, 지방 10g**
                """)
            
            with st.expander("☀️ 점심 (약 600kcal)"):
                st.markdown("""
                - 현미밥 1공기 (300kcal)
                - 닭가슴살 150g 또는 두부 1모 (180kcal)
                - 고구마 작은것 1개 (100kcal)
                - 샐러드 (20kcal)
                
                **➜ 단백질 35g, 탄수화물 75g, 지방 8g**
                """)
            
            with st.expander("🌙 저녁 (약 550kcal)"):
                st.markdown("""
                - 현미밥 1공기 (300kcal)
                - 생선 또는 고기 150g (200kcal)
                - 된장찌개 1인분 (50kcal)
                
                **➜ 단백질 35g, 탄수화물 50g, 지방 12g**
                """)
            
            with st.expander("🍎 간식 (약 250kcal)"):
                st.markdown("""
                - 과일 (바나나, 사과 등) (100kcal)
                - 견과류 한줌 (100kcal)
                - 우유 200ml (50kcal)
                
                **➜ 단백질 10g, 탄수화물 30g, 지방 10g**
                """)
            
            st.success("**📊 하루 총계:** 약 1,900kcal | 단백질: 102g | 탄수화물: 210g | 지방: 40g")
        
        st.markdown("---")
        st.subheader("💡 식단 팁")
        st.info("""
        - 위 식단은 예시이며, 개인 취향에 맞게 조절하세요
        - 비슷한 영양소를 가진 음식으로 대체 가능합니다
        - 물은 하루 2-2.5L 이상 충분히 섭취하세요
        - 가공식품과 설탕 섭취를 줄이세요
        - 식사 시간은 일정하게 유지하는 것이 좋습니다
        """)
    
    # 통증 주의사항 탭 (통증이 있을 경우에만)
    if st.session_state.pain_areas and len(tab_objects) > 4:
        with tab5:
            st.header("⚠️ 통증 부위 주의사항 및 재활 운동")
            
            st.warning(f"**통증 부위:** {', '.join(st.session_state.pain_areas)}")
            
            modifications, rehab_exercises = planner.get_pain_modifications()
            
            for area in st.session_state.pain_areas:
                if area in modifications:
                    st.markdown(f"### {area} 관련 주의사항")
                    
                    mod = modifications[area]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.error("**🚫 피해야 할 운동**")
                        for exercise in mod["피해야_할_운동"]:
                            st.write(f"✗ {exercise}")
                    
                    with col2:
                        st.warning("**⚠️ 주의가 필요한 운동**")
                        for exercise in mod["주의_운동"]:
                            st.write(f"⚡ {exercise}")
                    
                    with col3:
                        st.success("**✅ 대체 운동**")
                        for exercise in mod["대체_운동"]:
                            st.write(f"✓ {exercise}")
                    
                    if area in rehab_exercises:
                        st.markdown(f"#### 💊 {area} 재활/강화 운동")
                        
                        for exercise in rehab_exercises[area]:
                            with st.expander(f"✓ {exercise['이름']}"):
                                if "시간" in exercise:
                                    st.write(f"**{exercise['세트']}세트** × **{exercise['시간']}**, 휴식 **{exercise['휴식']}**")
                                elif "각" in exercise:
                                    st.write(f"**{exercise['세트']}세트** × **{exercise['각']}**")
                                else:
                                    st.write(f"**{exercise['세트']}세트** × **{exercise['횟수']}**, 휴식 **{exercise['휴식']}**")
                    
                    st.markdown("---")
            
            st.info("""
            **⚠️ 중요 안내**
            - 재활 운동은 매우 가벼운 무게나 맨몸으로 시작하세요
            - 통증이 심하거나 지속되면 전문의 상담이 필요합니다
            - 재활 운동은 주 3-4회, 본 운동 전 또는 휴식일에 수행
            - 운동 중 통증이 느껴지면 즉시 중단하세요
            - 호전되면 점진적으로 강도를 높이세요
            """)
    
    # 하단 버튼 (모바일 최적화 - 세로 배치)
    st.markdown("---")
    
    if st.button("✏️ 정보 수정", use_container_width=True):
        st.session_state.plan_generated = False
        st.rerun()
    
    if st.button("🔄 완전 초기화", use_container_width=True, type="primary"):
        # 모든 세션 상태 초기화
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("✅ 모든 정보가 초기화되었습니다. 새로운 사용자로 시작하세요!")
        st.rerun()
    
    # PDF 다운로드 기능은 추후 구현
    st.button("💾 플랜 저장 (준비 중)", use_container_width=True, disabled=True)

# 푸터 (모바일 최적화)
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem 0.5rem; font-size: 0.85rem;'>
        <p style='margin: 0.3rem 0;'><strong>FitPlan AI v2.0</strong></p>
        <p style='margin: 0.3rem 0;'>개인 맞춤형 운동 플랜 생성 서비스</p>
        <p style='margin: 0.3rem 0; font-size: 0.8rem;'>⚠️ 본 서비스는 참고용이며, 건강 문제가 있는 경우 전문가와 상담하세요.</p>
    </div>
""", unsafe_allow_html=True)
