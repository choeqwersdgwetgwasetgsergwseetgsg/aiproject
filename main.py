import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
name=st.text_input('이름을 적어주세요')
if st.button('인삿말 생성'):
  st.write('name+님 안녕하세요!')
  
