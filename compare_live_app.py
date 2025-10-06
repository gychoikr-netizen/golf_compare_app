
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

st.set_page_config(page_title="골프장 예약 비교", layout="wide")
st.title("⛳ 골프장 예약 비교 앱")

st.markdown("""
이 앱은 **골프장 예약 사이트**와 **내 데이터를 비교**해줍니다.  
- 예약 사이트 URL 입력  
- 내 데이터(CSV) 붙여넣기  
- 비교 결과 확인
""")

# 1️⃣ 예약 사이트 URL 입력
url = st.text_input("골프장 예약 페이지 URL을 입력하세요:")

# 2️⃣ 내 데이터 입력
st.markdown("### 내 데이터 입력 (CSV 형식, 헤더 포함)")
my_data = st.text_area("여기에 CSV 데이터를 붙여넣으세요:")

# 3️⃣ 비교 버튼
if st.button("비교 시작"):

    if not url or not my_data:
        st.warning("URL과 내 데이터를 모두 입력해주세요!")
    else:
        try:
            # 3-1. 예약 사이트 데이터 가져오기
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            # HTML 테이블 가져오기
            tables = pd.read_html(res.text)
            if tables:
                site_df = tables[0]
            else:
                site_df = pd.DataFrame()
                st.warning("사이트에서 테이블 데이터를 찾을 수 없습니다.")

            # 3-2. 내 데이터 읽기
            my_df = pd.read_csv(StringIO(my_data))

            # 3-3. 비교
            common_cols = my_df.columns.intersection(site_df.columns)
            if len(common_cols) == 0:
                st.warning("공통 열이 없습니다. 열 이름을 확인해주세요.")
            else:
                merged = pd.merge(my_df, site_df, on=list(common_cols), how='outer', indicator=True)
                st.markdown("### 비교 결과")
                st.dataframe(merged)

        except Exception as e:
            st.error(f"오류 발생: {e}")
