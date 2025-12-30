import os
import json
import yaml
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from typing import List

# Initialize Embedding Model
# using a small, fast model for local embeddings
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str) -> List[float]:
    return embed_model.encode(text).tolist()

class PortfolioRAG:
    def __init__(self, data_dir: str = "backend/data"):
        self.data_dir = data_dir
        self.client = chromadb.Client()
        # Create or get collection
        try:
            self.collection = self.client.get_collection(name="portfolio_data")
            self.client.delete_collection(name="portfolio_data") # Rebuild on start for updates
        except:
            pass
        
        self.collection = self.client.create_collection(
            name="portfolio_data", 
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        )
        self.load_data()

    def load_data(self):
        docs = []
        metadatas = []
        ids = []
        
        # Load about.md
        if os.path.exists(os.path.join(self.data_dir, "about.md")):
            with open(os.path.join(self.data_dir, "about.md"), "r", encoding="utf-8") as f:
                content = f.read()
                docs.append(content)
                metadatas.append({"source": "about", "type": "bio"})
                ids.append("about_main")

        # Load projects.json
        if os.path.exists(os.path.join(self.data_dir, "projects.json")):
            with open(os.path.join(self.data_dir, "projects.json"), "r", encoding="utf-8") as f:
                projects = json.load(f)
                for i, p in enumerate(projects):
                    # Chunk each project individually for better retrieval
                    content = f"Project: {p['name']}\nDescription: {p['description']}\nTech Stack: {', '.join(p['tech_stack'])}\nLinks: {p.get('links', {})}"
                    docs.append(content)
                    metadatas.append({"source": "projects", "project_name": p['name']})
                    ids.append(f"project_{i}")

        # Load experience.md
        if os.path.exists(os.path.join(self.data_dir, "experience.md")):
             with open(os.path.join(self.data_dir, "experience.md"), "r", encoding="utf-8") as f:
                content = f.read()
                # Simple chunking by double newline could be better, but treating as one block for now or splitting by large headers if needed
                # Let's split by '##' to separate Education from Experience
                sections = content.split("## ")
                for i, section in enumerate(sections):
                    if section.strip():
                        docs.append("## " + section) # Add header back
                        metadatas.append({"source": "experience", "section": f"section_{i}"})
                        ids.append(f"experience_{i}")

        # Load skills.yaml
        if os.path.exists(os.path.join(self.data_dir, "skills.yaml")):
            with open(os.path.join(self.data_dir, "skills.yaml"), "r", encoding="utf-8") as f:
                skills = yaml.safe_load(f)
                # Flatten skills for embedding
                skill_text = "Skills:\n"
                for category, items in skills.items():
                    skill_text += f"{category.capitalize()}: {', '.join(items)}\n"
                docs.append(skill_text)
                metadatas.append({"source": "skills", "type": "technical"})
                ids.append("skills_all")

        # Add to ChromaDB
        if docs:
            self.collection.add(
                documents=docs,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Indexed {len(docs)} documents.")

    def query(self, user_query: str, n_results: int = 3) -> str:
        results = self.collection.query(
            query_texts=[user_query],
            n_results=n_results
        )
        # Flatten results
        retrieved_docs = results['documents'][0]
        context = "\n\n---\n\n".join(retrieved_docs)
        
        lower_q = user_query.lower()
        
        # Append Dynamic LinkedIn Data if query relates to updates/socials/linkedin
        if "post" in lower_q or "linkedin" in lower_q or "update" in lower_q or "social" in lower_q:
            try:
                from backend.linkedin_client import LinkedInClient
                li_client = LinkedInClient()
                li_data = li_client.get_profile_data()
                context += f"\n\n[LinkedIn Info]\n{li_data['formatted_info']}"
                context += f"\n{li_client.get_latest_posts()}"
            except Exception as e:
                print(f"LinkedIn Integration Error: {e}")

        # Append Dynamic GitHub Data if query relates to repos/github/code
        if "github" in lower_q or "repo" in lower_q or "code" in lower_q or "project" in lower_q or "how many" in lower_q:
            try:
                from backend.github_client import GitHubClient
                gh_client = GitHubClient()
                
                # If asking about count/stats, include full stats
                if "how many" in lower_q or "count" in lower_q or "total" in lower_q or "stats" in lower_q:
                    gh_text = gh_client.get_stats_text()
                else:
                    gh_text = gh_client.get_repos_as_text(limit=5)
                    
                context += f"\n\n[Live GitHub Data]\n{gh_text}"
            except Exception as e:
                print(f"GitHub Integration Error: {e}")

        return context

