from fastapi import APIRouter, Depends, HTTPException, Request, Body
import ollama
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import re
import logging
from langdetect import detect
import requests
from datetime import datetime
import os
import sys
import json
from pathlib import Path
import uuid
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.schema.document import Document

# Import your existing modules
sys.path.append(str(Path(__file__).parent.parent))
from knowledge.loader import load_file, build_vectorstore
from .config import VECTORSTORE_PATH

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Document database file path
DOCUMENT_DB_PATH = os.path.join(os.path.dirname(VECTORSTORE_PATH), "documents.json")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "deepseek-r1"
    stream: bool = False
    options: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    processing_time: float

# Database operations - Implement directly instead of using db_manager
def get_vectorstore(vectorstore_path=VECTORSTORE_PATH):
    """Load or create a vector store"""
    try:
        if os.path.exists(vectorstore_path):
            # Choose the embeddings model you're using
            embeddings = HuggingFaceEmbeddings()  # or OpenAIEmbeddings() if you're using that
            return FAISS.load_local(vectorstore_path, embeddings)
        else:
            logger.warning(f"Vector store not found at {vectorstore_path}")
            return None
    except Exception as e:
        logger.error(f"Error loading vector store: {str(e)}")
        return None

def get_documents():
    """Get list of all documents"""
    try:
        if os.path.exists(DOCUMENT_DB_PATH):
            with open(DOCUMENT_DB_PATH, 'r') as f:
                return json.load(f)
        else:
            # If documents.json doesn't exist yet, create it
            with open(DOCUMENT_DB_PATH, 'w') as f:
                json.dump([], f)
            return []
    except Exception as e:
        logger.error(f"Error getting documents: {str(e)}")
        return []

def get_document_by_id(doc_id):
    """Get document by ID"""
    docs = get_documents()
    for doc in docs:
        if doc.get('id') == doc_id:
            return doc
    return None

def save_document_metadata(doc_id, title, source_path, metadata=None):
    """Save document metadata to the documents database"""
    try:
        docs = get_documents()
        
        # Check if document already exists
        for i, doc in enumerate(docs):
            if doc.get('id') == doc_id:
                # Update existing document
                docs[i].update({
                    'title': title,
                    'source': source_path,
                    'metadata': metadata or {},
                    'updated_at': datetime.now().isoformat()
                })
                break
        else:
            # Add new document
            docs.append({
                'id': doc_id,
                'title': title,
                'source': source_path,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
        
        # Save to file
        with open(DOCUMENT_DB_PATH, 'w') as f:
            json.dump(docs, f, indent=2)
        
        return True
    except Exception as e:
        logger.error(f"Error saving document metadata: {str(e)}")
        return False

def delete_document(doc_id):
    """Delete a document from the database"""
    try:
        docs = get_documents()
        docs = [doc for doc in docs if doc.get('id') != doc_id]
        
        # Save updated list
        with open(DOCUMENT_DB_PATH, 'w') as f:
            json.dump(docs, f, indent=2)
        
        return True
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        return False

# Translation functions
def translate_persian_to_english(text: str) -> str:
    """Translates Persian text to English using expert P2E function"""
    try:
        # Here you would call your actual P2E service/function
        # This is a placeholder - implement your actual translation method
        response = ollama.chat(model="deepseek-r1", 
                              messages=[
                                  {"role": "system", "content": "You are an expert Persian to English translator. Translate the following Persian text to English."},
                                  {"role": "user", "content": text}
                              ])
        return response['message']['content']
    except Exception as e:
        logger.error(f"Translation P2E error: {str(e)}")
        # Return original text if translation fails
        return text

def translate_english_to_persian(text: str) -> str:
    """Translates English text to Persian using expert E2P function"""
    try:
        # Here you would call your actual E2P service/function
        # This is a placeholder - implement your actual translation method
        response = ollama.chat(model="deepseek-r1", 
                              messages=[
                                  {"role": "system", "content": "You are an expert English to Persian translator. Translate the following English text to Persian."},
                                  {"role": "user", "content": text}
                              ])
        return response['message']['content']
    except Exception as e:
        logger.error(f"Translation E2P error: {str(e)}")
        # Return original text if translation fails
        return text

def detect_language(text: str) -> str:
    """Detect the language of input text"""
    try:
        # Persian language is detected as 'fa'
        lang = detect(text)
        return lang
    except:
        # Default to English if detection fails
        return "en"

def format_algorithm_explanation(algorithm_name: str, algorithm_data: dict) -> str:
    """Format the algorithm explanation with all required details"""
    explanation = f"# {algorithm_name} Algorithm\n\n"
    
    # Step-by-step explanation
    explanation += "## Step-by-Step Explanation\n"
    explanation += algorithm_data.get("explanation", "No detailed explanation available") + "\n\n"
    
    # Pseudocode
    explanation += "## Pseudocode\n```\n"
    explanation += algorithm_data.get("pseudocode", "No pseudocode available") + "\n```\n\n"
    
    # Diagrams and visuals (referencing them)
    if algorithm_data.get("diagrams"):
        explanation += "## Diagrams and Visualizations\n"
        explanation += algorithm_data.get("diagrams", "No diagrams available") + "\n\n"
    
    # Complexity analysis
    explanation += "## Complexity Analysis\n"
    explanation += "### Time Complexity\n"
    explanation += algorithm_data.get("time_complexity", "Not specified") + "\n\n"
    explanation += "### Space Complexity\n"
    explanation += algorithm_data.get("space_complexity", "Not specified") + "\n\n"
    
    # Advantages and disadvantages
    explanation += "## Advantages\n"
    advantages = algorithm_data.get("advantages", ["No specific advantages listed"])
    for adv in advantages:
        explanation += f"- {adv}\n"
    explanation += "\n"
    
    explanation += "## Disadvantages\n"
    disadvantages = algorithm_data.get("disadvantages", ["No specific disadvantages listed"])
    for dis in disadvantages:
        explanation += f"- {dis}\n"
    explanation += "\n"
    
    return explanation

async def process_fullcomplete_request(query: str):
    """Process request with fullcomplete command to explain algorithms in detail"""
    # Extract the actual query without the fullcomplete command
    base_query = query.replace("fullcomplete", "").strip()
    
    # Get the vector store
    vectorstore = get_vectorstore()
    if not vectorstore:
        return "Vector store not found. Please ensure documents have been processed."
    
    # Get relevant documents from the vector store
    docs = vectorstore.similarity_search(base_query, k=5)
    
    # Extract algorithm names from retrieved documents
    algorithm_names = []
    for doc in docs:
        # This regex pattern looks for algorithm names - adjust based on your document structure
        matches = re.findall(r'Algorithm:\s*([A-Za-z0-9\s\-_]+)', doc.page_content)
        algorithm_names.extend(matches)
    
    # Remove duplicates and clean names
    algorithm_names = list(set([name.strip() for name in algorithm_names]))
    
    # If no algorithms found, return a helpful message
    if not algorithm_names:
        return "No specific algorithms were found related to your query. Please try a different query."
    
    # For each algorithm, get detailed information and format it
    response_text = f"# Detailed Algorithm Explanations for: {base_query}\n\n"
    
    for alg_name in algorithm_names:
        # Get detailed info about this algorithm
        alg_query = f"Provide detailed explanation, pseudocode, diagrams, complexity analysis, advantages and disadvantages of {alg_name} algorithm"
        
        # Query your vector store for detailed information
        alg_docs = vectorstore.similarity_search(alg_query, k=3)
        
        # Extract and process the information
        algorithm_data = {
            "explanation": "\n".join([doc.page_content for doc in alg_docs]),
            "pseudocode": "",
            "time_complexity": "",
            "space_complexity": "",
            "advantages": [],
            "disadvantages": []
        }
        
        # Get LLM to generate structured information about the algorithm
        prompt = f"""
        Based on the following content about the {alg_name} algorithm, please provide:
        1. A clear step-by-step explanation
        2. Pseudocode representation
        3. Time and space complexity analysis
        4. List of advantages
        5. List of disadvantages
        
        Content:
        {algorithm_data['explanation']}
        """
        
        try:
            # Here you would call your LLM to structure the algorithm information
            llm_response = ollama.chat(model="deepseek-r1", 
                                      messages=[{"role": "user", "content": prompt}])
            
            # Parse the LLM response to extract structured information
            response_text_llm = llm_response['message']['content']
            
            # Extract sections from the response
            sections = re.split(r'##?\s+', response_text_llm)
            
            if len(sections) > 1:
                for section in sections[1:]:  # Skip the first empty section
                    if section.startswith("Step-by-Step"):
                        algorithm_data["explanation"] = section.replace("Step-by-Step Explanation:", "").strip()
                    elif section.startswith("Pseudocode"):
                        algorithm_data["pseudocode"] = section.replace("Pseudocode:", "").strip()
                    elif section.startswith("Time Complexity"):
                        algorithm_data["time_complexity"] = section.replace("Time Complexity:", "").strip()
                    elif section.startswith("Space Complexity"):
                        algorithm_data["space_complexity"] = section.replace("Space Complexity:", "").strip()
                    elif section.startswith("Advantages"):
                        advantages = section.replace("Advantages:", "").strip()
                        algorithm_data["advantages"] = [adv.strip() for adv in advantages.split("\n- ") if adv.strip()]
                    elif section.startswith("Disadvantages"):
                        disadvantages = section.replace("Disadvantages:", "").strip()
                        algorithm_data["disadvantages"] = [dis.strip() for dis in disadvantages.split("\n- ") if dis.strip()]
        
        except Exception as e:
            logger.error(f"Error processing algorithm information: {str(e)}")
        
        # Format the algorithm explanation
        formatted_explanation = format_algorithm_explanation(alg_name, algorithm_data)
        response_text += formatted_explanation + "\n\n---\n\n"
    
    return response_text

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    start_time = datetime.now()
    
    try:
        # Get the latest user message
        if not request.messages or len(request.messages) == 0:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        latest_message = request.messages[-1].content
        original_language = detect_language(latest_message)
        is_persian = original_language == 'fa'
        
        # Step 1: Language Detection and Translation
        working_text = latest_message
        if is_persian:
            logger.info("Detected Persian input, translating to English")
            working_text = translate_persian_to_english(latest_message)
        
        # Step 2: Check for fullcomplete command
        is_fullcomplete = "fullcomplete" in working_text.lower()
        
        # Process the request
        if is_fullcomplete:
            logger.info("Processing fullcomplete request")
            response_text = await process_fullcomplete_request(working_text)
        else:
            # Standard chat processing
            logger.info(f"Processing regular chat with model: {request.model}")
            # Modify messages to use translated content if needed
            processed_messages = []
            for msg in request.messages:
                if msg.role == "user" and msg.content == latest_message and is_persian:
                    # Only translate the latest user message
                    processed_messages.append({"role": msg.role, "content": working_text})
                else:
                    processed_messages.append({"role": msg.role, "content": msg.content})
            
            # For a basic retrieval-augmented approach, get relevant context
            vectorstore = get_vectorstore()
            if vectorstore:
                try:
                    context_docs = vectorstore.similarity_search(working_text, k=3)
                    context = "\n\n".join([doc.page_content for doc in context_docs])
                    
                    # Add context to the system message
                    context_message = {
                        "role": "system", 
                        "content": f"The following information may be helpful for answering the user's question:\n\n{context}"
                    }
                    processed_messages.insert(0, context_message)
                except Exception as e:
                    logger.error(f"Error retrieving context: {str(e)}")
            
            # Call Ollama for regular chat
            print(f"Trying to chat with model: {processed.model}")
            print(f"Messages: {processed.messages}")
            ollama_response = ollama.chat(
                model=request.model,
                messages=processed_messages,
                stream=request.stream,
                options=request.options
            )
            
            response_text = ollama_response['message']['content']
        
        # Step 4: Translate response back if original was Persian
        if is_persian:
            logger.info("Translating response back to Persian")
            response_text = translate_english_to_persian(response_text)
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        return {
            "response": response_text,
            "processing_time": processing_time
        }
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Document processing endpoint
@router.post("/process")
async def process_document_endpoint(file_path: str = Body(...)):
    """Process a document at the given file path and add to vector store"""
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        # Use your loader module to load and process the document
        doc = load_file(file_path)
        if not doc:
            raise HTTPException(status_code=400, detail="Failed to load document")
        
        # Generate a document ID if not already in the database
        file_name = os.path.basename(file_path)
        doc_id = str(uuid.uuid4())
        
        # Process document with your existing function or use a custom implementation
        try:
            # Use existing process_document function if it fits your needs
            processed_id = build_vectorstore(doc, file_path,VECTORSTORE_PATH)
            doc_id = processed_id or doc_id  # Use returned ID if available
        except Exception as e:
            # If process_document doesn't work as expected, implement alternative
            logger.error(f"Error using build_vectorstore: {str(e)}")
            # Implement manual processing if needed
            # This is a fallback if your process_document function has different parameters
            
            # Here you would implement manual processing:
            # 1. Split document into chunks
            # 2. Create embeddings
            # 3. Store in vector store
            # This depends on how your document processing is implemented
        
        # Save document metadata
        title = getattr(doc, 'metadata', {}).get('title', file_name)
        save_document_metadata(doc_id, title, file_path)
        
        return {
            "status": "success",
            "document_id": doc_id,
            "message": f"Document processed and added to vector store with ID: {doc_id}"
        }
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

# Get all documents endpoint
@router.get("/documents")
async def get_all_documents_endpoint():
    """Get list of all processed documents"""
    try:
        documents = get_documents()
        return {
            "status": "success",
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error getting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting documents: {str(e)}")

# Get document by ID endpoint
@router.get("/documents/{doc_id}")
async def get_document_endpoint(doc_id: str):
    """Get specific document by ID"""
    try:
        document = get_document_by_id(doc_id)
        if not document:
            raise HTTPException(status_code=404, detail=f"Document with ID {doc_id} not found")
        
        return {
            "status": "success",
            "document": document
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting document: {str(e)}")

# Delete document endpoint
@router.delete("/documents/{doc_id}")
async def delete_document_endpoint(doc_id: str):
    """Delete a document by ID"""
    try:
        document = get_document_by_id(doc_id)
        if not document:
            raise HTTPException(status_code=404, detail=f"Document with ID {doc_id} not found")
        
        success = delete_document(doc_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete document")
        
        return {
            "status": "success",
            "message": f"Document with ID {doc_id} deleted successfully"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if vector store exists
        vectorstore_exists = os.path.exists(VECTORSTORE_PATH)
        documents_db_exists = os.path.exists(DOCUMENT_DB_PATH)
        
        return {
            "status": "healthy",
            "vector_store": "available" if vectorstore_exists else "not found",
            "documents_db": "available" if documents_db_exists else "not found",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")