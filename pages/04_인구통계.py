# streamlit_population_app.py

"""
Streamlit population visualization app

사용법:
1. population.csv 파일을 같은 폴더에 두거나 업로드하세요.
2. 로컬 실행: `streamlit run streamlit_population_app.py`
3. Streamlit Cloud 배포 시, 이 파일과 requirements.txt를 같은 GitHub repo에 올리세요.

requirements.txt 내용:
streamlit
pandas
matplotlib
numpy
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 페이지 설정
st.set_page_config(page_title="행정구별 연령별 인구 그래프", layout="wide")

st.title("행정구 선택 — 연령별 인구수 (꺾은선 그래프)")
st.write("CSV 파일에서 행정구를 선택하면 가로축=나이, 세로축=인구수(10살 단위)로 꺾은선 그래프를 그립니다.")

# 공통 열 이름 후보
COMMON_ADMIN = ['행정구', '행정구역', '구', '시군구', 'adm', 'district', 'area']
COMMON_AGE = ['나이', '연령', 'age', '연령대', 'age_group']
COMMON_POP = ['인구', '인구수', 'population', 'pop', 'count']

# 열 탐지 함수
def find_column(cols, candidates):
    cols_lower = {c.lower(): c for c in cols}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    for col in cols:
        low = col.lower()
        for cand in candidates:
            if cand.lower() in low:
                return col
    return None

# 나이를 숫자로 변환
def age_to_numeric(age_series):
    s = age_series.astype(str).str.strip()
    nums = []
    for v in s:
        if v == '' or v.lower() in ['nan', 'none']:
            nums.append(np.nan)
            continue
        try:
            nums.append(float(v))
            continue
        except:
            pass
        if '-' in v:
            parts = v.replace(' ', '').split('-')
            try:
                a = float(parts[0])
                b = float(parts[-1])
                nums.append((a + b) / 2.0)
                continue
            except:
                pass
        if '대' in v:
            try:
                num = ''.join([c for c in v if c.isdigit()])
                if num != '':
                    nums.append(float(num) + 5.0)
                    continue
            except:
                pass
        nums.append(np.nan)
    return pd.Series(nums)

# CSV 파일 불러오기
uploaded = st.file_uploader("CSV 파일 업로드 (선택, 없으면 기본 경로 시도)", type=['csv'])

df = None
if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.success("업로드된 파일을 불러왔습니다.")
    except Exception as e:
        st.error(f"업로드된 파일을 불러오는 중 오류: {e}")
else:
    default_path = '/mnt/data/popuiation.csv'
    if os.path.exists(default_path):
        try:
            df = pd.read_csv(default_path)
            st.info(f"기본 경로에서 '{default_path}' 파일을 불러왔습니다.")
        except Exception as e:
            st.error(f"기본 경로의 CSV를 읽는 중 오류: {e}")
    else:
        st.warning("CSV 파일을 업로드하거나 '/mnt/data/popuiation.csv' 경로에 파일을 추가해주세요.")

if df is None:
    st.stop()

st.write("**데이터 미리보기**")
st.dataframe(df.head())

# 열 자동 탐지
cols = df.columns.tolist()
admin_col = find_column(cols, COMMON_ADMIN)
age_col = find_column(cols, COMMON_AGE)
pop_col = find_column(cols, COMMON_POP)

if admin_col is None or age_col is None or pop_col is None:
    st.warning("자동 탐지 실패 — 직접 열을 선택하세요.")
    admin_col = st.selectbox("행정구 열 선택", options=[None] + cols)
    age_col = st.selectbox("나이 열 선택", options=[None] + cols)
    pop_col = st.selectbox("인구수 열 선택", options=[None] + cols)

if not admin_col or not age_col or not pop_col:
    st.error("모든 열(행정구, 나이, 인구수)을 선택해야 합니다.")
    st.stop()

# 데이터 정리
working = df[[admin_col, age_col, pop_col]].copy()
working.columns = ['admin', 'age', 'pop']
working['pop'] = pd.to_numeric(working['pop'], errors='coerce')
working['age_num'] = age_to_numeric(working['age'])

if working['age_num'].isna().all():
    st.error("나이 데이터를 숫자로 변환할 수 없습니다.")
    st.stop()

# 행정구 선택
admins = sorted(working['admin'].dropna().unique().tolist())
sel_admin = st.selectbox("행정구 선택", options=admins)

sub = working[working['admin'] == sel_admin].copy()
if sub.empty:
    st.error("선택한 행정구 데이터가 없습니다.")
    st.stop()

sub = sub.dropna(subset=['age_num', 'pop'])
sub['age_int'] = sub['age_num'].astype(int)
age_pop = sub.groupby('age_int', as_index=False)['pop'].sum()

if age_pop.empty:
    st.error("연령별 인구 데이터를 찾을 수 없습니다.")
    st.stop()

# 10살 단위로 묶기
max_age = int(age_pop['age_int'].max())
bins = list(range(0, max_age + 11, 10))
labels = [f"{b}-{b+9}" for b in bins[:-1]]
age_pop['age_bin'] = pd.cut(age_pop['age_int'], bins=bins, labels=labels, include_lowest=True)

bin_agg = age_pop.groupby('age_bin', observed=True)['pop'].sum().reindex(labels, fill_value=0).reset_index()

# 그래프 생성
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#dcdcdc')
ax.set_facecolor('#dcdcdc')
ax.plot(bin_agg['age_bin'], bin_agg['pop'], marker='o', linewidth=2)
ax.set_xlabel('연령대 (10살 단위)')
ax.set_ylabel('인구수')
ax.set_title(f"{sel_admin} — 연령대별 인구수")
ax.grid(True, linestyle='--', alpha=0.6)

st.pyplot(fig)

st.caption("⚙️ CSV 열 이름이 다를 경우 자동 탐지가 실패할 수 있습니다. 문제가 생기면 열 이름을 확인해주세요.")
