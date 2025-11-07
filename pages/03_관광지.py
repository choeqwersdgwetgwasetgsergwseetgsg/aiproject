# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="서울 인기 관광지 (Top10) — Folium", layout="wide")

st.title("🇰🇷 서울 방문객 인기 관광지 Top 10")
st.write("외국인들에게 인기 있는 서울의 주요 관광지 Top10을 지도에 표시합니다. 왼쪽에서 장소를 선택하면 지도로 이동합니다.")

# 데이터: 장소명, 위도, 경도, 간단설명, 이미지(웹 URL)
PLACES = [
    {
        "name": "경복궁 (Gyeongbokgung Palace)",
        "lat": 37.579617,
        "lon": 126.977041,
        "desc": "조선의 대표 궁궐. 수문장 교대식과 한복 체험으로 유명합니다.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Gyeongbokgung_Palace_2016.jpg"
    },
    {
        "name": "북촌한옥마을 (Bukchon Hanok Village)",
        "lat": 37.582604,
        "lon": 126.985402,
        "desc": "전통 한옥이 모여 있는 포토·체험 명소.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Bukchon_Hanok_Village_2016.jpg"
    },
    {
        "name": "N서울타워 (N Seoul Tower / Namsan)",
        "lat": 37.5511694,
        "lon": 126.9882266,
        "desc": "서울 전경을 한눈에 — 전망대·야경 명소.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/1a/N_Seoul_Tower_2013.jpg"
    },
    {
        "name": "명동 (Myeongdong)",
        "lat": 37.560970,
        "lon": 126.985433,
        "desc": "쇼핑·길거리음식의 중심가 — 특히 뷰티 쇼핑으로 유명.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/5/58/Myeongdong_2015.jpg"
    },
    {
        "name": "인사동 (Insadong)",
        "lat": 37.574403,
        "lon": 126.985135,
        "desc": "전통 공예·찻집·갤러리. 기념품 구입에 좋음.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/5/58/Insadong_2013.jpg"
    },
    {
        "name": "홍대 (Hongdae / Hongik Univ.)",
        "lat": 37.556264,
        "lon": 126.922512,
        "desc": "젊음의 거리, 스트리트 퍼포먼스·카페·클럽이 밀집.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Hongdae_Street_2015.jpg"
    },
    {
        "name": "동대문 디자인 플라자 (DDP)",
        "lat": 37.5662952,
        "lon": 127.0090646,
        "desc": "독특한 건축물·전시·야간 쇼핑의 중심.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Dongdaemun_Design_Plaza_2013.jpg"
    },
    {
        "name": "청계천 (Cheonggyecheon Stream)",
        "lat": 37.570409,
        "lon": 126.977962,
        "desc": "도심 속 하천 산책로 — 야간 조명이 아름답습니다.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/4/45/Cheonggyecheon_2014.jpg"
    },
    {
        "name": "롯데월드타워 / 서울스카이 (Lotte World Tower / Seoul Sky)",
        "lat": 37.513148,
        "lon": 127.102615,
        "desc": "초고층 전망대와 쇼핑몰, 아쿠아리움.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/2/22/Lotte_World_Tower_2016.jpg"
    },
    {
        "name": "남대문시장 (Namdaemun Market)",
        "lat": 37.559408,
        "lon": 126.977041,
        "desc": "전통 재래시장 — 기념품·의류·길거리 음식이 풍성.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/3/35/Namdaemun_market_2014.jpg"
    },
]

# 좌측 사이드바: 장소 선택 & 설명 표시
st.sidebar.header("장소 선택")
place_names = [p["name"] for p in PLACES]
selected = st.sidebar.selectbox("장소 선택 (또는 지도를 드래그)", options=["전체 보기"] + place_names)

st.sidebar.markdown("---")
st.sidebar.write("데이터 출처: 여행정보 및 관광 통계 종합.")
st.sidebar.write("앱: Folium + streamlit-folium 사용 — Streamlit Cloud에 배포 가능")

# 기본 지도 생성 (서울 중심)
center_lat, center_lon = 37.5665, 126.9780
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# 마커 추가
for p in PLACES:
    html_popup = f"""
    <div style="width:200px">
      <h4>{p['name']}</h4>
      <img src="{p['img']}" alt="{p['name']}" style="width:100%;height:110px;object-fit:cover;border-radius:4px"/>
      <p style="font-size:12px">{p['desc']}</p>
      <a href="https://www.google.com/maps/search/?api=1&query={p['lat']},{p['lon']}" target="_blank">길찾기 (Google Maps)</a>
    </div>
    """
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=folium.Popup(html_popup, max_width=260),
        tooltip=p["name"]
    ).add_to(marker_cluster)

# 선택한 장소로 이동(zoom & pan)
if selected != "전체 보기":
    sel = next((x for x in PLACES if x["name"] == selected), None)
    if sel:
        m.location = [sel["lat"], sel["lon"]]
        m.zoom_start = 16
        # 강조용 원 추가
        folium.CircleMarker(location=[sel["lat"], sel["lon"]],
                            radius=50, color="#3186cc", fill=True, fill_opacity=0.1).add_to(m)

# 지도를 스트림릿에 렌더링
st_data = st_folium(m, width=1200, height=700)

# 장소 리스트와 간단 설명
st.markdown("### 📍 Top 10 장소 리스트")
cols = st.columns(2)
for i, p in enumerate(PLACES):
    with cols[i % 2]:
        st.markdown(f"**{i+1}. {p['name']}**")
        st.write(p["desc"])
        st.image(p["img"], width=240)
