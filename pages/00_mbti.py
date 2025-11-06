import streamlit as st

st.set_page_config(page_title="MBTI별 진로 추천", page_icon="🎯", layout="centered")

st.title("MBTI별 맞춤 진로 추천 🎯")
st.write("원하는 MBTI를 선택하면, 해당 유형에 맞는 **2가지 진로**와 각 진로에 적합한 학과 및 성격을 알려줘요.")

MBTI_OPTIONS = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

# 각 MBTI마다 진로(2개)와 설명을 담은 데이터
MBTI_MAP = {
    "ISTJ": [
        {"career":"회계사 / 세무사", "majors":"경영학(회계), 세무학", "personality":"성실하고 꼼꼼하며 규칙을 잘 지키는 타입. 숫자와 규칙을 좋아함."},
        {"career":"토목/건축 엔지니어", "majors":"건축공학, 토목공학", "personality":"현실적이고 계획적으로 일하며 책임감이 강함."}
    ],
    "ISFJ": [
        {"career":"간호사", "majors":"간호학", "personality":"사려 깊고 돌보는 것을 좋아함. 꼼꼼하고 책임감이 강함."},
        {"career":"사회복지사", "majors":"사회복지학", "personality":"타인을 돕는 데 만족감을 느끼며 안정적인 환경을 선호함."}
    ],
    "INFJ": [
        {"career":"임상심리사/상담사", "majors":"심리학, 상담학", "personality":"타인의 감정을 잘 읽고 깊은 통찰을 가진다. 의미 있는 일을 추구."},
        {"career":"작가/콘텐츠 크리에이터", "majors":"국어국문, 창작학", "personality":"내면 세계가 풍부하고 표현을 통해 영향력을 발휘하고 싶어함."}
    ],
    "INTJ": [
        {"career":"연구원(과학/공학)", "majors":"전공에 따라 물리/화학/전기/컴공 등", "personality":"전략적이고 독립적으로 문제를 해결하는 것을 즐김."},
        {"career":"소프트웨어 아키텍트", "majors":"컴퓨터공학, 소프트웨어학", "personality":"체계적 사고와 장기 설계를 좋아함."}
    ],
    "ISTP": [
        {"career":"기계/산업기술자", "majors":"기계공학, 산업공학", "personality":"손으로 만드는 일, 실용적 문제 해결을 즐김."},
        {"career":"항공기 정비사/파일럿", "majors":"항공운항, 항공정비", "personality":"침착하고 실전에 강하며 기술적 능력이 뛰어남."}
    ],
    "ISFP": [
        {"career":"그래픽 디자이너", "majors":"시각디자인, 산업디자인", "personality":"감성적이고 미적 감각이 뛰어나며 실용적 창작을 좋아함."},
        {"career":"사진작가/영상편집자", "majors":"영상학, 사진학", "personality":"관찰력이 좋고 순간을 포착하는 감각이 뛰어남."}
    ],
    "INFP": [
        {"career":"상담사/치료사", "majors":"심리학, 상담학", "personality":"공감능력이 높고 사람들의 가치를 지지하는 일을 선호함."},
        {"career":"인문학 연구자/편집자", "majors":"문학, 철학, 인문학", "personality":"사색적이고 깊이 있는 사고를 즐김."}
    ],
    "INTP": [
        {"career":"데이터 사이언티스트/분석가", "majors":"통계학, 컴퓨터공학, 산업공학", "personality":"호기심이 많고 개념적 문제를 분석하는 걸 좋아함."},
        {"career":"시스템 설계자/연구개발", "majors":"전산/전자/소프트웨어 관련 학과", "personality":"논리적이고 추상적인 설계에 강함."}
    ],
    "ESTP": [
        {"career":"영업/세일즈", "majors":"경영학, 마케팅", "personality":"즉흥적이고 행동력이 강하며 사람을 설득하는 데 능함."},
        {"career":"응급구조사/현장기술자", "majors":"응급구조학, 각종 실무기술 전공", "personality":"위기 대응 능력이 뛰어나고 실전에서 강함."}
    ],
    "ESFP": [
        {"career":"연예/무대예술(퍼포머)", "majors":"연극영화, 실용음악", "personality":"사교적이고 표현력이 풍부하며 즉각적인 피드백을 즐김."},
        {"career":"이벤트 플래너/호텔리어", "majors":"호텔경영, 관광학, 이벤트전공", "personality":"사람을 즐겁게 하는 걸 좋아하고 현장 관리에 능함."}
    ],
    "ENFP": [
        {"career":"마케팅 전략가/브랜딩", "majors":"광고/홍보, 경영학", "personality":"창의적이고 아이디어가 풍부하며 사람을 연결하는 역량이 큼."},
        {"career":"콘텐츠 크리에이터/커뮤니티 매니저", "majors":"미디어학, 커뮤니케이션", "personality":"열정적이고 소통을 즐기며 트렌드에 민감함."}
    ],
    "ENTP": [
        {"career":"창업가/스타트업 창업자", "majors":"경영학, 컴퓨터공학 등 다양", "personality":"아이디어가 많고 도전적인 성향, 리스크를 즐김."},
        {"career":"컨설턴트/전략기획", "majors":"경영학, 경제학", "personality":"문제해결과 설득에 능하며 빠른 사고를 선호."}
    ],
    "ESTJ": [
        {"career":"기업 관리자/운영 매니저", "majors":"경영학, 산업경영공학", "personality":"조직을 이끄는 실무 능력이 뛰어나고 책임감이 강함."},
        {"career":"군인/공무원(행정)", "majors":"행정학, 법학, 공공관리", "personality":"규율을 중시하고 안정된 시스템에서 능력을 발휘함."}
    ],
    "ESFJ": [
        {"career":"교사/교육행정", "majors":"교육학, 아동학", "personality":"사교적이고 타인을 돕는 데에서 만족을 느끼며 협력적임."},
        {"career":"인사/HR", "majors":"심리학, 경영학(인사)", "personality":"사람을 이해하고 조직을 돌보는 역할에 잘 맞음."}
    ],
    "ENFJ": [
        {"career":"PR/홍보 전문가", "majors":"커뮤니케이션, 광고홍보", "personality":"사람을 이끌고 동기를 부여하는 데 능숙함."},
        {"career":"상담교사/교육 컨설턴트", "majors":"교육학, 상담학", "personality":"타인의 성장을 돕는 데 큰 보람을 느낌."}
    ],
    "ENTJ": [
        {"career":"경영컨설턴트/CEO", "majors":"경영학, 경제학", "personality":"목표지향적이고 리더십이 강하며 전략적 사고를 함."},
        {"career":"프로젝트 매니저/전략기획", "majors":"산업공학, 경영학", "personality":"큰 그림을 보고 조직을 운영하는 데 능함."}
    ]
}

st.sidebar.header("설정")
show_details = st.sidebar.checkbox("진로 설명 더 보기", value=True)

choice = st.selectbox("당신의 MBTI를 골라줘요:", MBTI_OPTIONS)

if st.button("추천 받기 ✨"):
    careers = MBTI_MAP.get(choice, [])
    st.subheader(f"{choice}님의 추천 진로")
    for item in careers:
        with st.expander(item["career"]):
            st.markdown(f"**적합 학과:** {item['majors']}")
            if show_details:
                st.markdown(f"**어떤 성격이 잘 맞을까?** {item['personality']}")
                # 짧은 친근한 조언
                st.write("조언: 학교에서 관련 동아리나 체험활동을 해보고 흥미를 확인해보자! 😊")

    st.write("---")
    st.info("Tip: 위 추천은 일반적인 성향을 기준으로 한 제안이에요. 관심과 경험이 가장 중요하니 꼭 직접 체험해보세요!")

st.caption("※ 이 앱은 학습용이며, 보다 구체적인 진로 상담은 진로상담가와 상담하세요.")
