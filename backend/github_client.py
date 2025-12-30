import requests
import os

class GitHubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.username = "grharsha777"
        self.api_url = "https://api.github.com"
        self._cached_repos = None
        self._repo_count = None

    def get_all_repos(self):
        """
        Fetches ALL public repositories (handles pagination).
        """
        if self._cached_repos:
            return self._cached_repos
            
        try:
            headers = {
                "Accept": "application/vnd.github.v3+json"
            }
            if self.token:
                headers["Authorization"] = f"token {self.token}"
            
            all_repos = []
            page = 1
            per_page = 100  # Max allowed by GitHub API
            
            while True:
                response = requests.get(
                    f"{self.api_url}/users/{self.username}/repos?per_page={per_page}&page={page}",
                    headers=headers
                )
                response.raise_for_status()
                repos = response.json()
                
                if not repos:
                    break
                    
                all_repos.extend(repos)
                page += 1
                
                # Safety check to avoid infinite loop
                if page > 10:
                    break
            
            self._cached_repos = all_repos
            self._repo_count = len(all_repos)
            return all_repos
            
        except Exception as e:
            print(f"GitHub API Error: {e}")
            return []

    def get_repo_count(self):
        """
        Returns total number of repositories.
        """
        if self._repo_count is None:
            self.get_all_repos()
        return self._repo_count or 0

    def get_repos(self, limit=5, sort_by="updated"):
        """
        Fetches repositories with sorting options.
        sort_by: "updated", "stars", "name"
        """
        all_repos = self.get_all_repos()
        
        if sort_by == "updated":
            sorted_repos = sorted(all_repos, key=lambda x: x.get("updated_at", ""), reverse=True)
        elif sort_by == "stars":
            sorted_repos = sorted(all_repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)
        else:
            sorted_repos = sorted(all_repos, key=lambda x: x.get("name", "").lower())
        
        repo_list = []
        for repo in sorted_repos[:limit]:
            repo_list.append({
                "name": repo.get("name"),
                "description": repo.get("description") or "No description",
                "url": repo.get("html_url"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "updated_at": repo.get("updated_at")
            })
        return repo_list

    def get_repos_as_text(self, limit=5):
        """
        Returns repos as formatted text for RAG context.
        """
        repos = self.get_repos(limit)
        total_count = self.get_repo_count()
        
        if not repos:
            return "Unable to fetch GitHub repositories at this time."
        
        text = f"GitHub Stats: **{total_count} total repositories**\n\n"
        text += "Latest/Top Repositories:\n"
        for repo in repos:
            text += f"- **{repo['name']}**: {repo['description']} | Language: {repo['language']} | Stars: {repo['stars']} | <a href=\"{repo['url']}\" target=\"_blank\">View Repo</a>\n"
        text += f"\nView all {total_count} repos at: <a href=\"https://github.com/{self.username}\" target=\"_blank\">GitHub Profile</a>"
        return text

    def get_stats_text(self):
        """
        Returns GitHub statistics as formatted text.
        """
        all_repos = self.get_all_repos()
        total_count = len(all_repos)
        
        # Calculate stats
        languages = {}
        total_stars = 0
        for repo in all_repos:
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
            total_stars += repo.get("stargazers_count", 0)
        
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        lang_text = ", ".join([f"{lang} ({count})" for lang, count in top_languages])
        
        text = f"""
**GitHub Statistics for G R Harsha:**
- Total Repositories: **{total_count}**
- Total Stars: **{total_stars}**
- Top Languages: {lang_text}
- Profile: <a href="https://github.com/{self.username}" target="_blank">github.com/{self.username}</a>
"""
        return text
