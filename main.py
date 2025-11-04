import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
name=st.text_input('이름을 적어주세요')
st.selctbox('좋아하는 음식을 선택해 주세요')['치킨','볶음밥','짬뽕'])
if st.button('인삿말 생성'):
  st.write(name+'님 안녕하세요!')
