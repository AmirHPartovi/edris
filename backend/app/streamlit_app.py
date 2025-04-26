import streamlit as st
import requests
import json
import os
from datetime import datetime

# Configure page settings
st.set_page_config(page_title="Backend API Tester & Chat Pipeline", layout="wide")

# Main title
st.title("API Endpoint Tester & Chat Pipeline")

# Define the base URL for your backend
BASE_URL = st.sidebar.text_input("Base URL", value="http://localhost:8000")

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["API Endpoint Testing", "Document Management", "Chat Pipeline"])

# Tab 1: API Endpoint Testing
with tab1:
    st.header("Test Backend Endpoints")
    
    # Endpoints section
    endpoint_options = [
        "Select an endpoint",
        "GET /health",
        "POST /process",
        "GET /documents",
        "GET /documents/{doc_id}",
        "POST /chat",
        # Add more endpoints as needed
    ]
    
    selected_endpoint = st.selectbox("Choose an endpoint", endpoint_options)
    
    if selected_endpoint != "Select an endpoint":
        st.subheader(f"Testing: {selected_endpoint}")
        
        # Parse the endpoint
        method, path = selected_endpoint.split(" ")
        
        # Handle path parameters
        if "{" in path:
            param_name = path[path.find("{")+1:path.find("}")]
            param_value = st.text_input(f"Enter {param_name}")
            path = path.replace(f"{{{param_name}}}", param_value)
        
        # Request body (for POST/PUT methods)
        if method in ["POST", "PUT"]:
            st.subheader("Request Body")
            if path == "/process":
                file_path = st.text_input("File Path (full path to the document)", value="")
                request_body = json.dumps({"file_path": file_path})
            else:
                request_body = st.text_area("JSON Body", height=200)
            
            try:
                if request_body:
                    json_body = json.loads(request_body)
                else:
                    json_body = {}
            except:
                st.error("Invalid JSON format")
                json_body = {}
            
        # Execute the request
        if st.button("Send Request"):
            try:
                url = f"{BASE_URL}{path}"
                
                st.info(f"Sending {method} request to {url}")
                
                if method == "GET":
                    response = requests.get(url)
                elif method == "POST":
                    response = requests.post(url, json=json_body)
                elif method == "PUT":
                    response = requests.put(url, json=json_body)
                elif method == "DELETE":
                    response = requests.delete(url)
                    
                # Display response
                st.subheader("Response")
                st.write(f"Status Code: {response.status_code}")
                
                try:
                    resp_json = response.json()
                    st.json(resp_json)
                except:
                    st.text(response.text)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Tab 2: Document Management
with tab2:
    st.header("Document Management")
    
    # Document processing section
    st.subheader("Process Document")
    file_path = st.text_input("Enter absolute path to document file")
    
    if st.button("Process Document"):
        if file_path:
            try:
                response = requests.post(
                    f"{BASE_URL}/process",
                    json={"file_path": file_path}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Document processed successfully! Document ID: {result.get('document_id')}")
                else:
                    st.error(f"Error: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a file path")
    
    # Document listing section
    st.subheader("Document List")
    if st.button("Refresh Documents"):
        try:
            response = requests.get(f"{BASE_URL}/documents")
            if response.status_code == 200:
                documents = response.json().get("documents", [])
                if documents:
                    # Create a table of documents
                    for doc in documents:
                        with st.expander(f"Document: {doc.get('title', 'Unknown')}"):
                            st.write(f"ID: {doc.get('id')}")
                            st.write(f"Path: {doc.get('source')}")
                            st.write(f"Added: {doc.get('created_at')}")
                            
                            # Button to view document details
                            if st.button(f"View Details", key=f"view_{doc.get('id')}"):
                                doc_response = requests.get(f"{BASE_URL}/documents/{doc.get('id')}")
                                if doc_response.status_code == 200:
                                    doc_details = doc_response.json().get("document")
                                    st.json(doc_details)
                                else:
                                    st.error(f"Failed to get document details: {doc_response.text}")
                else:
                    st.info("No documents found")
            else:
                st.error(f"Failed to get documents: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Tab 3: Chat Pipeline
with tab3:
    st.header("Chat Pipeline")
    
    # Chat settings
    st.sidebar.subheader("Chat Settings")
    model_name = st.sidebar.text_input("Model Name", value="llama3")
    st.sidebar.info("Type 'fullcomplete' in your message to get detailed algorithm explanations")
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input for new message
    user_input = st.chat_input("Message (can be in English or Persian)...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Call chat endpoint
        with st.chat_message("assistant"):
            with st.spinner("Processing your message..."):
                try:
                    # Prepare request with chat history
                    messages = []
                    for msg in st.session_state.chat_messages:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    # Make the request to your backend
                    response = requests.post(
                        f"{BASE_URL}/chat",
                        json={
                            "messages": messages,
                            "model": model_name,
                            "stream": False
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        assistant_response = result["response"]
                        processing_time = result.get("processing_time", 0)
                        
                        # Display the response
                        st.markdown(assistant_response)
                        st.caption(f"Processing time: {processing_time:.2f} seconds")
                        
                        # Add assistant response to chat history
                        st.session_state.chat_messages.append({
                            "role": "assistant", 
                            "content": assistant_response
                        })
                    else:
                        st.error(f"Error: API returned status code {response.status_code}")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"Failed to communicate with the backend: {str(e)}")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_messages = []
        st.experimental_rerun()

# Sidebar - System status
st.sidebar.header("System Status")
if st.sidebar.button("Check Health"):
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            st.sidebar.success("✅ System Healthy")
            st.sidebar.write(f"Vector Store: {health_data.get('vector_store')}")
            st.sidebar.write(f"Last Check: {health_data.get('timestamp')}")
        else:
            st.sidebar.error("❌ System Unhealthy")
            st.sidebar.write(response.text)
    except Exception as e:
        st.sidebar.error(f"❌ Connection Failed: {str(e)}")

# Sidebar info
st.sidebar.header("About")
st.sidebar.info("""
This application helps test your backend API endpoints and interact with your chat pipeline.

The chat pipeline supports:
- Persian and English inputs
- Special command 'fullcomplete' for detailed algorithm explanations
- Automatic translation based on input language
""")
st.sidebar.write(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")