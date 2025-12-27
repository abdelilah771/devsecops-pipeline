class PromptService:
    def generate_prompt(self, vulnerability: dict, provider: str = "github"):
        context = vulnerability.get("description", "")
        code_snippet = vulnerability.get("code", "")
        
        provider_syntax = {
            "github": "GitHub Actions YAML",
            "gitlab": "GitLab CI",
            "jenkins": "Jenkins Groovy"
        }
        
        syntax = provider_syntax.get(provider, "General")
        
        return f"""
        You are a security expert. Fix the following vulnerability.
        
        Context: {context}
        Provider Syntax: {syntax}
        
        Vulnerable Code:
        ```
        {code_snippet}
        ```
        
        Return a JSON response with:
        - fixed_code: The corrected code
        - explanation: 2 line explanation
        - steps: List of configuration steps
        """
