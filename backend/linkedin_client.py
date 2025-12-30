import requests
import os

class LinkedInClient:
    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID", "")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET", "")
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
        self.profile_url = "https://www.linkedin.com/in/grharsha777/"
        self.api_url = "https://api.linkedin.com/v2"

    def get_latest_posts(self):
        """
        Fetches latest posts. 
        Note: LinkedIn API requires OAuth 2.0 Access Token.
        Without it, we return static info with the profile link.
        """
        if not self.access_token:
            return f'For the latest LinkedIn updates, visit <a href="{self.profile_url}" target="_blank">Harsha\'s LinkedIn Profile</a>.'

        try:
            return f'For the latest LinkedIn updates, visit <a href="{self.profile_url}" target="_blank">Harsha\'s LinkedIn Profile</a>.'
        except Exception as e:
            return f"Error fetching LinkedIn posts: {e}"

    def get_profile_data(self):
        """
        Returns profile data with hyperlinks.
        """
        return {
            "name": "G R Harsha",
            "education": [
                "NIAT & Yenepoya University (B.Tech CSE AI, 2025-2029)"
            ],
            "linkedin_url": self.profile_url,
            "formatted_info": f'''
<b>LinkedIn Profile</b>: <a href="{self.profile_url}" target="_blank">G R Harsha</a>
<b>Current</b>: B.Tech CSE (AI) Student at NIAT & Yenepoya University
<b>Roles</b>: Mentor @ GSSoC, Campus Ambassador @ GUESSS India
<b>Focus</b>: AI Engineering, Agentic Systems, DevOps Automation
'''
        }
