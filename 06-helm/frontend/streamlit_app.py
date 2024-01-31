import streamlit as st
import requests

def call_fastapi(endpoint, method='get', data=None, headers=None):
    base_url = 'http://backend-service-clusterip:80'  # Updated to the k8s service name and mapped port for the backend
    url = f'{base_url}/{endpoint}'
    if method == 'post':
        return requests.post(url, json=data, headers=headers).json()
    return requests.get(url, headers=headers).json()

st.title('FastAPI Interaction Client')

with st.form("create_user"):
    st.write("### Create a New User")
    name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Create User")
    if submitted:
        response = call_fastapi('create_user/', 'post', {"name": name, "password": password})
        st.write(response)

with st.form("submit_text"):
    st.write("### Submit Text for Analysis")
    user_name = st.text_input("Username for Text Submission")
    user_password = st.text_input("Password for Text Submission", type="password")
    text = st.text_area("Text to Analyze")
    submitted_text = st.form_submit_button("Submit Text")
    if submitted_text:
        headers = {'name': user_name, 'password': user_password}
        response = call_fastapi('prediction_with_auth/', 'post', {"text": text}, headers)
        st.write(response)

with st.form("list_users"):
    st.write("### Get List of registered Users")
    if st.form_submit_button("Get All Users"):
        users = call_fastapi('users')
        st.write("### All Users")
        st.write(users)

with st.form("get_texts"):
    st.write("### Get Texts for a User")
    user_name_texts = st.text_input("Username to Retrieve Texts")
    user_password_texts = st.text_input("Password to Retrieve Texts", type="password")
    submitted_texts = st.form_submit_button("Get Texts")
    if submitted_texts:
        headers = {'name': user_name_texts, 'password': user_password_texts}
        texts = call_fastapi('texts', headers=headers)
        st.write(texts)
