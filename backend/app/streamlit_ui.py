import streamlit as st
import requests

API_URL = "http://localhost:8000"

def main():
    st.title("Edris Backend Tester")
    st.sidebar.header("Send a Query")

    prompt = st.text_area("Prompt", "سلام، درباره هوش مصنوعی توضیح بده.")
    query_type = st.selectbox("Type", ["text", "code", "complete"])
    model = st.text_input("Model", "deepseek-r1:latest")
    if st.button("Send /query"):
        payload = {
            "prompt": prompt,
            "type": query_type,
            "model": model
        }
        resp = requests.post(f"{API_URL}/query", json=payload)
        if resp.ok:
            st.write(resp.json()["response"])
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")

    st.sidebar.header("Upload Knowledge")
    uploaded = st.file_uploader("Select files", accept_multiple_files=True)
    if st.button("Upload /knowledge/upload"):
        files = {"files": (f.name, f, "application/octet-stream") for f in uploaded}
        resp = requests.post(f"{API_URL}/knowledge/upload", files=files)
        if resp.ok:
            st.success("Uploaded: " + ", ".join(resp.json().get("files", [])))
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    main()
