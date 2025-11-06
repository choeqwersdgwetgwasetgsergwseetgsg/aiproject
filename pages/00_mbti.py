import streamlit as st

st.set_page_config(page_title="MBTI별 진로 추천", page_icon="🎯", layout="centered")

st.title("MBTI별 맞춤 진로 추천 🎯")
st.write("MBTI 선택하면 **2가지 진로**, 적합 학과, 성격, 그리고 **평균 연봉**도 알려줄게요! 💼✨")

MBTI_OPTIONS = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

# 연봉 단위: 만원 (예시 기준, 실제와 차이 있음)
MBTI_MAP = {
    "ISTJ": [
        {"career":"회계사 / 세무사", "majors":"경영학(회계), 세무학", "personality":"성실&꼼꼼. 규칙 좋아함.", "salary":"6,500~10,000 만원"},
        {"career":"토목/건축 엔지니어", "majors":"건축공학, 토목공학", "personality":"현실적, 책임감 강함.", "salary":"4,500~8,000 만원"}
    ],
    "ISFJ": [
        {"career":"간호사", "majors":"간호학", "personality":"돌봄 선호, 안정추구.", "salary":"4,000~7,000 만원"},
        {"career":"사회복지사", "majors":"사회복지학", "personality":"타인 지원에 보람 느낌.", "salary":"3,000~5,000 만원"}
    ],
    "INFJ": [
        {"career":"임상심리사/상담사", "majors":"심리학, 상담학", "personality":"공감, 통찰력.", "salary":"3,500~6,000 만원"},
        {"career":"작가/콘텐츠 크리에이터", "majors":"국어국문, 창작학", "personality":"표현력 풍부.", "salary":"수입 편차 큼"}
    ],
    "INTJ": [
        {"career":"연구원(과학/공학)", "majors":"물리/화학/전기/컴공 등", "personality":"전략적 사고.", "salary":"4,500~9,000 만원"},
        {"career":"소프트웨어 아키텍트", "majors":"컴퓨터공학", "personality":"체계 설계 선호.", "salary":"6,000~12,000 만원"}
    ],
    "ISTP": [
        {"career":"기계/산업기술자", "majors":"기계/산업공학", "personality":"실용적 문제 해결.", "salary":"4,000~7,500 만원"},
        {"career":"항공기 정비사/파일럿", "majors":"항공운항/정비", "personality":"실전에 강함.", "salary":"정비: 4,000~8,000 / 파일럿: 8,000~1억 이상"}
    ],
    "ISFP": [
        {"career":"그래픽 디자이너", "majors":"시각/산업디자인", "personality":"미적 감각 우수.", "salary":"3,000~6,000 만원"},
        {"career":"사진/영상 전문가", "majors":"영상/사진학", "personality":"감성적 관찰력.", "salary":"수입 편차 큼"}
    ],
    "INFP": [
        {"career":"상담사/치료사", "majors":"심리학, 상담학", "personality":"공감능력 최고.", "salary":"3,500~6,000 만원"},
        {"career":"인문학 연구자/편집자", "majors":"문학, 철학", "personality":"깊은 사고.", "salary":"3,000~5,500 만원"}
    ],
    "INTP": [
        {"career":"데이터 분석가", "majors":"통계, 컴공", "personality":"분석적, 탐구적.", "salary":"4,500~9,000 만원"},
        {"career":"R&D 엔지니어", "majors":"전자/소프트웨어", "personality":"추상적 설계 강함.", "salary":"5,000~9,500 만원"}
    ],
    "ESTP": [
        {"career":"영업/세일즈", "majors":"경영, 마케팅", "personality":"행동력, 설득력.", "salary":"성과에 따라 매우 다양"},
        {"career":"응급구조/현장기술", "majors":"응급구조학", "personality":"위기대응 최고.", "salary":"3,800~6,500 만원"}
    ],
    "ESFP": [
        {"career":"퍼포머(연예/무대)", "majors":"실용음악, 연극영화", "personality":"표현력, 사교성.", "salary":"편차 큼"},
        {"career":"이벤트/호텔리어", "majors":"호텔경영, 관광", "personality":"현장소통 강함.", "salary":"3,000~5,500 만원"}
    ],
    "ENFP": [
        {"career":"브랜딩/마케팅", "majors":"경영, 광고홍보", "personality":"창의적, 열정적.", "salary":"3,500~8,000 만원"},
        {"career":"커뮤니티 매니저", "majors":"커뮤니케이션", "personality":"소통 잘함.", "salary":"3,200~6,000 만원"}
    ],
    "ENTP": [
        {"career":"스타트업 창업", "majors":"제한 없음", "personality":"도전적, 아이디어 풍부.", "salary":"대성 시 매우 높음, 실패 리스크 큼"},
        {"career":"전략기획/컨설팅", "majors":"경영, 경제", "personality":"문제 해결력.", "salary":"5,000~12,000 만원"}
    ],
    "ESTJ": [
        {"career":"운영/관리 매니저", "majors":"경영, 산업공학", "personality":"리더십, 실무 능력.", "salary":"4,000~9,000 만원"},
        {"career":"공무원/군인", "majors":"행정학, 법학", "personality":"규율 중요.", "salary":"직급 따라 다양"}
    ],
    "ESFJ": [
        {"career":"교사/교육행정", "majors":"교육, 아동학", "personality":"협력적, 친절.", "salary":"3,500~6,500 만원"},
        {"career":"HR/인사", "majors":"경영(인사), 심리", "personality":"사람 이해 잘함.", "salary":"3,800~7,500 만원"}
    ],
    "ENFJ": [
        {"career":"홍보/PR", "majors":"커뮤니케이션", "personality":"동기부여 잘함.", "salary":"4,000~8,000 만원"},
        {"career":"교육 컨설턴트", "majors":"교육학", "personality":"타인 성장 돕기.", "salary":"3,800~7,000 만원"}
    ],
    "ENTJ": [
        {"career":"CEO/경영컨설턴트", "majors":"경영, 경제", "personality":"전략, 리더십.", "salary":"상위권 매우 높음"},
        {"career":"프로젝트 매니저", "majors":"산업공학", "personality":"큰 그림 설계.", "salary":"5,500~10,000 만원"}
    ]
}

st.sidebar.header("설정")
show_details = st.sidebar.checkbox("성격&학과 상세 보기", value=True)

choice = st.selectbox("당신의 MBTI를 골라줘요:", MBTI_OPTIONS)

if st.button("추천 받기 ✨"):
    careers = MBTI_MAP.get(choice, [])
    st.subheader(f"{choice}님을 위한 진로 추천 💡")
    for item in careers:
        with st.expander(item["career"]):
            st.markdown(f"**평균 연봉:** {item['salary']} 💰")
            st.markdown(f"**적합 학과:** {item['majors']}")
            if show_details:
                st.markdown(f"**잘 맞는 성격:** {item['personality']}")
                st.write("Tip: 관련 동아리나 체험활동으로 흥미를 확인해보세요! 😄")
    st.write("---")
    st.info("※ 연봉은 업계/경력에 따라 달라요. 진로는 직접 경험하고 탐색하는 게 가장 중요해요! ✨")

st.caption("학습용 참고 자료이며, 자세한 진로 상담은 전문가에게! 📘")
