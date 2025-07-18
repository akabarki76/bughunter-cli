DEFAULT_TEMPLATE = "Analyze the following code for security vulnerabilities:\n\n{code_snippet}"

PROMPT_TEMPLATES = {
    "web": "Analyze {language} web app for OWASP Top 10 vulnerabilities. Pay special attention to {entry_points}",
    "api": "Check API endpoints {endpoints} for improper authz, injection, and mass assignment",
    "c-cpp": "Inspect memory handling in {file}: look for buffer overflows, UAF, and integer overflows"
}

def build_prompt(context):
    template = PROMPT_TEMPLATES.get(context["scan_type"], DEFAULT_TEMPLATE)
    # Use a dictionary for formatting to avoid errors with missing keys
    return template.format(**context) + f"\n\nCode:\n{context.get('code_snippet', '')[:2000]}"

if __name__ == '__main__':
    # Example usage
    web_context = {
        "scan_type": "web",
        "language": "Python",
        "entry_points": "/login, /users",
        "code_snippet": "def login(request):\n    # ..."
    }

    api_context = {
        "scan_type": "api",
        "endpoints": "/api/v1/users, /api/v1/data",
        "code_snippet": "@app.route('/api/v1/users')\ndef get_users():\n    # ..."
    }

    cpp_context = {
        "scan_type": "c-cpp",
        "file": "memory.c",
        "code_snippet": "int main() {\n    char *buf = malloc(10);\n    // ...\n}"
    }

    default_context = {
        "scan_type": "generic",
        "code_snippet": "print('Hello, World!')"
    }

    print("--- Web Prompt ---")
    print(build_prompt(web_context))
    print("\n--- API Prompt ---")
    print(build_prompt(api_context))
    print("\n--- C/C++ Prompt ---")
    print(build_prompt(cpp_context))
    print("\n--- Default Prompt ---")
    print(build_prompt(default_context))
