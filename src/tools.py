import logging
import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools import tool
from src.logger import setup_logging

logger = setup_logging()

class PolicyKnowledgeBase:
    vector_db = None

    @staticmethod
    def initialize():
        """
        Initializes the vector database with policy documents.
        This should be called at application startup.
        It attempts to fetch documents from a Git repository first.
        If that fails or no repo is provided, it falls back to local data.
        """
        if PolicyKnowledgeBase.vector_db is not None:
            logger.info("Knowledge Base already initialized.")
            return

        logger.info("Initializing Knowledge Base...")
        
        # Configuration for Policy Source
        data_source_path = "data/"
        
        logger.info(f"Initializing Knowledge Base from {data_source_path}")
        
        if not os.path.exists(data_source_path):
            os.makedirs(data_source_path, exist_ok=True)
            if not os.listdir(data_source_path):
                with open(os.path.join(data_source_path, "sample_policy.txt"), "w") as f:
                    f.write("This is a sample policy document (fallback).")
                logger.info("Created sample policy document.")

        try:
            docs = []
            # Load Text files
            txt_loader = DirectoryLoader(data_source_path, glob="*.txt", loader_cls=TextLoader)
            docs.extend(txt_loader.load())
            logger.info(f"Loaded {len(docs)} text documents.")

            # Load PDF files
            pdf_loader = DirectoryLoader(data_source_path, glob="*.pdf", loader_cls=PyPDFLoader)
            pdf_docs = pdf_loader.load()
            docs.extend(pdf_docs)
            logger.info(f"Loaded {len(pdf_docs)} PDF documents.")
            
            if not docs:
                 logger.warning("No documents found to index.")
                 return

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = text_splitter.split_documents(docs)
            logger.info(f"Split documents into {len(chunks)} chunks.")
            
            # Check for API key
            if not os.environ.get("OPENAI_API_KEY"):
                 logger.warning("OPENAI_API_KEY not found in environment. Embeddings will fail.")
                 return

            embeddings = OpenAIEmbeddings()
            PolicyKnowledgeBase.vector_db = FAISS.from_documents(chunks, embeddings)
            logger.info(f"Knowledge Base Initialized successfully from {data_source_path}.")
            
        except Exception as e:
            logger.error(f"Error initializing Knowledge Base: {e}")
            raise e



from crewai.tools import BaseTool
from pydantic import Field

class PolicySearchTool(BaseTool):
    name: str = "Policy Search Tool"
    description: str = "Useful to search for company policies, refund rules, SLA details, and other internal documents. Always use this tool when you need to answer questions about company rules or procedures."
    
    def _run(self, query: str) -> str:
        try:
            if PolicyKnowledgeBase.vector_db is None:
                PolicyKnowledgeBase.initialize()
                if PolicyKnowledgeBase.vector_db is None:
                    return "Error: Knowledge Base not initialized. Check API key."
            
            # Search for similar documents
            docs = PolicyKnowledgeBase.vector_db.similarity_search(query, k=3)
            return "\n\n".join([d.page_content for d in docs])
        except Exception as e:
            logger.error(f"Error during policy search: {e}")
            return f"Error occurred during search: {str(e)}"

# Create the tool instance
policy_search_tool = PolicySearchTool()

class FetchUserDetailsTool(BaseTool):
    name: str = "User Details Tool"
    description: str = "Useful to fetch customer details from the database. Input should be a username (e.g., 'John Doe') or email. Returns user profile including plan, billing info, and dues. If user not found, returns 'User not found'."

    def _run(self, identifier: str) -> str:
        try:
            # Clean identifier
            identifier = identifier.strip().strip("'\"")
            
            # If agent passed both (e.g. "John Doe, john.doe@example.com"), try splitting
            identifiers_to_try = [identifier]
            if "," in identifier:
                identifiers_to_try.extend([i.strip() for i in identifier.split(",")])
            if " and " in identifier.lower():
                import re
                identifiers_to_try.extend([i.strip() for i in re.split(r" and ", identifier, flags=re.IGNORECASE)])
            
            # Construct absolute path to DB relative to this file
            db_path = os.path.join(os.path.dirname(__file__), '../data/users.db')
            
            import sqlite3
            
            # Check if DB needs initialization (missing, empty, or missing table)
            should_init = False
            if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
                should_init = True
                logger.warning(f"DB file missing or empty at {db_path}. Re-initializing...")
            else:
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
                    if not cursor.fetchone():
                        should_init = True
                        logger.warning("DB exists but 'users' table missing. Re-initializing...")
                    conn.close()
                except Exception as e:
                    logger.error(f"Error checking DB health: {e}")
                    should_init = True

            if should_init:
                try:
                    from src.db_init import init_db
                    logger.info("Triggering database initialization...")
                    init_db()
                    logger.info("Database re-initialized successfully.")
                except Exception as e:
                    logger.error(f"Failed to re-initialize database: {e}")
                    return "Error: Database initialization failed."

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            row = None
            for idx in identifiers_to_try:
                if not idx: continue
                logger.info(f"DEBUG: Attempting retrieval for identifier: '{idx}'")
                cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (idx, idx))
                row = cursor.fetchone()
                if row:
                    break
            
            conn.close()
            
            if row:
                columns = ['username', 'email', 'address', 'phone', 'service_opted', 'plan', 'start_date', 'end_date', 'monthly_cost', 'dues', 'next_billing_date', 'billing_cycle']
                user_data = dict(zip(columns, row))
                return str(user_data)
            else:
                return "User not found."
        except Exception as e:
            logger.error(f"Error fetching user details: {e}")
            return f"Error fetching user details: {str(e)}"

fetch_user_details = FetchUserDetailsTool()
