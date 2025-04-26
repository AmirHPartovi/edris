import streamlit as st
import requests
import time

# Config
def get_api_url():
    return st.secrets.get("API_URL", "http://localhost:8000")

# Utility
def fetch_spaces():
    resp = requests.get(f"{get_api_url()}/spaces")
    return resp.json().get("spaces", [])

# Main App
def main():
    st.set_page_config(page_title="Edris RAG UI", layout="wide")
    st.title("📚 Edris RAG System")

    # Sidebar: Space Management
    st.sidebar.header("Spaces")
    spaces = fetch_spaces()
    space_names = [s["name"] for s in spaces]
    selected = st.sidebar.selectbox("Select space", [None] + space_names)

    new_space = st.sidebar.text_input("New space name")
    if st.sidebar.button("Create Space"):
        if new_space:
            with st.spinner("Creating space..."):
                r = requests.post(f"{get_api_url()}/spaces/{new_space}", json={})
            if r.ok:
                st.sidebar.success(f"Space '{new_space}' created.")
            else:
                st.sidebar.error(f"Error: {r.text}")
            time.sleep(1)
            spaces = fetch_spaces()
            space_names = [s["name"] for s in spaces]

    if selected:
        if st.sidebar.button("Delete Space"):
            with st.spinner(f"Deleting space {selected}..."):
                r = requests.delete(f"{get_api_url()}/spaces/{selected}")
            if r.ok:
                st.sidebar.success(f"Space '{selected}' deleted.")
            else:
                st.sidebar.error(f"Error: {r.text}")
            time.sleep(1)
            spaces = fetch_spaces()
            selected = None

    # Main Tabs
    tab1, tab2, tab3 = st.tabs(["Upload & Build", "Search Knowledge", "Search Algorithms"])

    if tab1:
        tab1.header("Upload Documents & Build Vectorstore")
        if not selected:
            tab1.info("Select a space to upload.")
        else:
            files = tab1.file_uploader("Choose documents", type=["md","txt","csv","pdf","docx","pptx","ppt"], accept_multiple_files=True)
            if tab1.button("Upload & Build", key="upload_build") and files:
                with st.spinner("Uploading files..."):
                    multipart = [("files", (f.name, f, "application/octet-stream")) for f in files]
                    r = requests.post(f"{get_api_url()}/knowledge/upload/{selected}", files=multipart)
                if r.ok:
                    tab1.success("Upload scheduled. Build in progress!")
                else:
                    tab1.error(f"Error: {r.text}")

    if tab2:
        tab2.header("Search Knowledge")
        if not selected:
            tab2.info("Select a space to search.")
        else:
            q = tab2.text_input("Enter query", key="search_q")
            k = tab2.slider("Top K", 1, 20, 5, key="search_k")
            if tab2.button("Search", key="search_button") and q:
                with st.spinner("Searching..."):
                    r = requests.get(f"{get_api_url()}/knowledge/search/{selected}", params={"q": q, "k": k})
                if r.ok:
                    res = r.json().get("results", [])
                    for i, doc in enumerate(res, 1):
                        tab2.subheader(f"Result {i}")
                        tab2.write(doc)
                else:
                    tab2.error(f"Error: {r.text}")

    if tab3:
        tab3.header("Search Algorithms")
        if not selected:
            tab3.info("Select a space to search algorithms.")
        else:
            q_algo = tab3.text_input("Algorithm query", key="algo_q")
            k_algo = tab3.slider("Top K Algos", 1, 20, 5, key="algo_k")
            if tab3.button("Search Algo", key="algo_button") and q_algo:
                with st.spinner("Searching algorithms..."):
                    r = requests.get(f"{get_api_url()}/algorithms/search/{selected}", params={"q": q_algo, "k": k_algo})
                if r.ok:
                    algos = r.json().get("algorithms", [])
                    for algo in algos:
                        tab3.success(algo)
                else:
                    tab3.error(f"Error: {r.text}")

if __name__ == "__main__":
    main()