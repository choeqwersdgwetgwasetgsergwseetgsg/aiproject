# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="서울 인기 관광지 Top10", layout="wide")

st.title("🇰🇷 서울 인기 관광지 Top 10")
st.write("외국인이 좋아하는 서울의 주요 관광지를 지도와 함께 안내합니다!")

PLACES = [
    {
        "name": "경복궁",
        "eng": "Gyeongbokgung Palace",
        "lat": 37.579617,
        "lon": 126.977041,
        "why": "조선의 법궁으로 전통 건축미를 감상할 수 있는 대표 궁궐.",
        "how": "지하철 3호선 경복궁역 5번 출구 도보 5분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Gyeongbokgung_Palace_2016.jpg",
    },
    {
        "name": "북촌한옥마을",
        "eng": "Bukchon Hanok Village",
        "lat": 37.582604,
        "lon": 126.985402,
        "why": "600년 한옥이 보존된 전통마을. 사진 촬영 명소.",
        "how": "3호선 안국역 2번 출구 도보 10분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Bukchon_Hanok_Village_2016.jpg",
    },
    {
        "name": "N서울타워",
        "eng": "N Seoul Tower",
        "lat": 37.5511694,
        "lon": 126.9882266,
        "why": "서울 전경을360°로 볼 수 있는 야경 명소.",
        "how": "명동역 3번 출구 → 남산케이블카 탑승",
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/1a/N_Seoul_Tower_2013.jpg",
    },
    {
        "name": "명동",
        "eng": "Myeongdong",
        "lat": 37.560970,
        "lon": 126.985433,
        "why": "쇼핑과 길거리 음식의 중심지.",
        "how": "명동역 6~8번 출구",
        "img": "https://upload.wikimedia.org/wikipedia/commons/5/58/Myeongdong_2015.jpg",
    },
    {
        "name": "인사동",
        "eng": "Insadong",
        "lat": 37.574403,
        "lon": 126.985135,
        "why": "전통 공예품과 다도 체험을 즐길 수 있는 전통거리.",
        "how": "안국역 6번 출구 도보 5분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/5/58/Insadong_2013.jpg",
    },
    {
        "name": "홍대",
        "eng": "Hongdae",
        "lat": 37.556264,
        "lon": 126.922512,
        "why": "버스킹 문화, 쇼핑, 카페 거리로 유명한 핫플.",
        "how": "홍대입구역 9번 출구",
        "img": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Hongdae_Street_2015.jpg",
    },
    {
        "name": "동대문 디자인 플라자(DDP)",
        "eng": "Dongdaemun Design Plaza",
        "lat": 37.5662952,
        "lon": 127.0090646,
        "why": "자하 하디드 설계의 곡선 디자인 건축 랜드마크.",
        "how": "동대문역사문화공원역 1번 출구",
        "img": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Dongdaemun_Design_Plaza_2013.jpg",
    },
    {
        "name": "청계천",
        "eng": "Cheonggyecheon Stream",
        "lat": 37.570409,
        "lon": 126.977962,
        "why": "도심 속 산책로. 야경이 매우 아름다움.",
        "how": "광화문역 5번 출구 도보 5분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/4/45/Cheonggyecheon_2014.jpg",
    },
    {
        "name": "롯데월드타워 / 서울스카이",
        "eng": "Lotte World Tower",
        "lat": 37.513148,
        "lon": 127.102615,
        "why": "세계 5위 초고층 전망대. 쇼핑·아쿠아리움 등 명소 모음.",
        "how": "잠실역 2번 출구 연결",
        "img": "https://upload.wikimedia.org/wikipedia/commons/2/22/Lotte_World_Tower_2016.jpg",
    },
    {
        "name": "남대문시장",
        "eng": "Namdaemun Market",
        "lat": 37.559408,
        "lon": 126.977041,
        "why": "한국 최대 전통시장. 먹거리·기념품 천국.",
        "how": "회현역 5번 출구 도보 3분",
        "img": "https://upload.wikimedia.org/wikipedia/commons/3/35/Namdaemun_market_2014.jpg",
    },
]

# ---- Sidebar ----
st.sidebar.header("📍 관광지 선택")
place_names = [p["name"] for p in PLACES]
selected = st.sidebar.selectbox("장소를 선택하세요", ["전체 보기"] + place_names)

if selected != "전체 보기":
    sel = next(p for p in PLACES if p["name"] == selected)
    st.sidebar.subheader(sel["eng"])
    st.sidebar.image(sel["img"], width=180)
    st.sidebar.write(f"📌 왜 유명해? → {sel['why']}")
    st.sidebar.write(f"🚇 가는 방법 → {sel['how']}")

# ---- Map ----
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
cluster = MarkerCluster().add_to(m)

for p in PLACES:
    popup = f"""
    <h4>{p['name']} ({p['eng']})</h4>
    <img src="{p['img']}" width="230" style="border-radius:5px;">
    <p>📌 {p['why']}</p>
    <p>🚇 {p['how']}</p>
    """
    folium.Marker(
        [p["lat"], p["lon"]],
        tooltip=p["name"],
        popup=folium.Popup(popup, max_width=300),
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(cluster)

if selected != "전체 보기":
    m.location = [sel["lat"], sel["lon"]]
    m.zoom_start = 16
    folium.CircleMarker([sel["lat"], sel["lon"]],
                        radius=50, color="crimson",
                        fill=True, fill_opacity=0.15).add_to(m)

st_folium(m, width=1200, height=700)
