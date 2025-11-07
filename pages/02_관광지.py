# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="서울 인기 관광지 Top10", layout="wide")

st.title("🇰🇷 서울 인기 관광지 Top 10")
st.write("지도 마커를 클릭하거나 왼쪽에서 선택해 보세요!")

# Top10 데이터
PLACES = [
    {
        "name": "경복궁",
        "eng": "Gyeongbokgung Palace",
        "lat": 37.579617,
        "lon": 126.977041,
        "why": "조선의 법궁으로서 한국 전통 궁궐 문화를 대표합니다. 수문장 교대식과 한복체험으로 유명합니다.",
        "how": "지하철 3호선 경복궁역 5번 출구 도보 5분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Gyeongbokgung_Palace_2016.jpg",
    },
    {
        "name": "북촌한옥마을",
        "eng": "Bukchon Hanok Village",
        "lat": 37.582604,
        "lon": 126.985402,
        "why": "600년 역사 한옥이 잘 보존된 곳. 사진 명소로 외국인 여행객 필수코스.",
        "how": "지하철 3호선 안국역 2번 출구 도보 10분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Bukchon_Hanok_Village_2016.jpg",
    },
    {
        "name": "N서울타워",
        "eng": "N Seoul Tower",
        "lat": 37.5511694,
        "lon": 126.9882266,
        "why": "서울 전경을360°로 조망할 수 있는 랜드마크. 야경 명소!",
        "how": "명동역 3번 출구 → 남산케이블카 탑승",
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/1a/N_Seoul_Tower_2013.jpg",
    },
    {
        "name": "명동",
        "eng": "Myeongdong",
        "lat": 37.560970,
        "lon": 126.985433,
        "why": "쇼핑과 길거리음식 성지. 화장품 브랜드 밀집 지역.",
        "how": "명동역 6~8번 출구 바로",
        "img": "https://upload.wikimedia.org/wikipedia/commons/5/58/Myeongdong_2015.jpg",
    },
    {
        "name": "인사동",
        "eng": "Insadong",
        "lat": 37.574403,
        "lon": 126.985135,
        "why": "전통 공예품·다도 체험·갤러리 탐방으로 유명.",
        "how": "안국역 6번 출구 도보 5분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/5/58/Insadong_2013.jpg",
    },
    {
        "name": "홍대",
        "eng": "Hongdae",
        "lat": 37.556264,
        "lon": 126.922512,
        "why": "젊은 예술 거리, 버스킹과 개성 있는 카페가 가득.",
        "how": "홍대입구역 9번 출구 바로",
        "img": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Hongdae_Street_2015.jpg",
    },
    {
        "name": "동대문 디자인 플라자(DDP)",
        "eng": "Dongdaemun Design Plaza",
        "lat": 37.5662952,
        "lon": 127.0090646,
        "why": "자하하디드 설계의 미래형 건축물. 전시·야경 유명.",
        "how": "동대문역사문화공원역 1번 출구 바로",
        "img": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Dongdaemun_Design_Plaza_2013.jpg",
    },
    {
        "name": "청계천",
        "eng": "Cheonggyecheon Stream",
        "lat": 37.570409,
        "lon": 126.977962,
        "why": "도심 속 힐링 산책로. 야간 조명과 축제도 인기.",
        "how": "광화문역 5번 출구 도보 5분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/4/45/Cheonggyecheon_2014.jpg",
    },
    {
        "name": "롯데월드타워 / 서울스카이",
        "eng": "Lotte World Tower",
        "lat": 37.513148,
        "lon": 127.102615,
        "why": "세계 5위 초고층 빌딩. 전망대·쇼핑몰·아쿠아리움!",
        "how": "잠실역 2번 출구 바로 연결",
        "img": "https://upload.wikimedia.org/wikipedia/commons/2/22/Lotte_World_Tower_2016.jpg",
    },
    {
        "name": "남대문시장",
        "eng": "Namdaemun Market",
        "lat": 37.559408,
        "lon": 126.977041,
        "why": "한국 최대 전통시장. 의류·기념품·먹거리 가득!",
        "how": "회현역 5번 출구 도보 3분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/3/35/Namdaemun_market_2014.jpg",
    }
]

# Sidebar
st.sidebar.header("📍 장소 선택")
place_names = [p["name"] for p in PLACES]
selected = st.sidebar.selectbox("원하는 장소를 선택하세요", ["전체 보기"] + place_names)

if selected != "전체 보기":
    sel = next((i for i in PLACES if i["name"] == selected), None)
    st.sidebar.subheader(sel["eng"])
    st.sidebar.image(sel["img"], width=200)
    st.sidebar.markdown(f"**📌 왜 유명해?** <br>{sel['why']}", unsafe_allow_html=True)
    st.sidebar.markdown(f"**🚇 가장 빠르게 가는 방법** <br>{sel['how']}", unsafe_allow_html=True)

# Map
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

for p in PLACES:
    html_popup = f"""
    <h4>{p['name']} ({p['eng']})</h4>
    <img src="{p['img']}" style="width:250px;border-radius:5px;">
    <p>📌 {p['why']}</p>
    <p>🚇 {p['how']}</p>
    """
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=folium.Popup(html_popup, max_width=300),
        tooltip=p["name"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(marker_cluster)

if selected != "전체 보기" and sel:
    m.location = [sel["lat"], sel["lon"]]
    m.zoom_start = 16
    folium.CircleMarker([sel["lat"], sel["lon"]], radius=45,
                        color="crimson", fill=True, fill_opacity=0.1).add_to(m)

st_folium(m, width=1200, height=720)

st.write("✔ 관광지 클릭 👉 상세 설명과 교통 안내 표시")
