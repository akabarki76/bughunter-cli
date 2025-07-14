# `bughunter-cli` 🐞

**A powerful, all-in-one command-line interface designed for modern bug hunting, security analysis, and streamlined development workflows.**

`bughunter-cli` combines essential security scanning tools with AI-powered analysis and robust GitHub integration, making it the perfect companion for security researchers, penetration testers, and developers who prioritize a secure development lifecycle.

## VibeOps Engineering

`bughunter-cli` is designed with the principles of **VibeOps** in mind. VibeOps is an emerging engineering culture that uses AI and natural language to automate and simplify the entire software development lifecycle. This tool embodies the VibeOps philosophy by:

- **Enhancing Developer Experience (DevEx):** Providing a seamless, conversational interface to complex security and development tasks.
- **AI-Assisted Workflow:** Leveraging Large Language Models (LLMs) to automate reconnaissance, vulnerability analysis, and payload generation.
- **CI/CD and Automation:** Automating routine tasks like project cleanup, package publishing, and eventually, CI/CD pipeline integration.
- **AI SRE:** Using AI to move towards a future of AI-driven Site Reliability Engineering, where monitoring and remediation are increasingly automated.

## Overview

This tool is built to be your go-to utility for a variety of tasks, from initial reconnaissance to reporting and development automation. It replaces the need for multiple disparate scripts and tools by providing a single, consistent interface for:

*   **Reconnaissance:** Discover subdomains and scan for open ports.
*   **Code Scanning:** Scan code for vulnerabilities using Semgrep.
*   **Dependency Scanning:** Scan project dependencies for known vulnerabilities against the GitHub Advisory Database.
*   **AI-Powered Security Analysis:** Leverage Google's Gemini Pro to analyze targets, identify potential vulnerabilities, and generate custom attack payloads.
*   **Development Workflow:** Seamlessly interact with GitHub to manage issues, pull requests, and comments directly from your terminal.
*   **Project Maintenance:** Automate cleanup tasks, manage releases, and publish Python packages with ease.

## Key Features

*   **Subdomain Enumeration:** Quickly find subdomains for a target domain using `crt.sh`.
*   **Port Scanning:** Integrated `nmap` for scanning top open ports.
*   **Code Scanning:** Language-agnostic code scanning with Semgrep.
*   **Dependency Scanning:** Uses `osv-scanner` to find vulnerabilities in your dependencies.
*   **AI-Driven Vulnerability Analysis:** Get an AI-generated security report on a target and its subdomains.
*   **AI Payload Generation:** Create tailored payloads (XSS, SQLi, etc.) for specific technology stacks.
*   **Full GitHub Integration:**
    *   Initialize and authenticate with your GitHub account.
    *   Create and manage Pull Requests.
    *   Pull and view repository Issues.
    *   Push comments to Issues and PRs.
*   **Package Publishing:** Built-in commands to build and publish your Python package to PyPI or a private repository.
*   **Project Cleanup:** A simple `autoclean` command to remove temporary files, build artifacts, and virtual environments.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/bughunter-cli.git
    cd bughunter-cli
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install the CLI in editable mode:**
    This makes the `bughunter` command available in your terminal.
    ```bash
    pip install -e .
    ```

5.  **Install External Scanners:**
    `bughunter-cli` relies on powerful external tools for some of its scanning capabilities.

    *   **Install `osv-scanner` (for dependency scanning):**
        Follow the official installation instructions at [google.github.io/osv-scanner/](https://google.github.io/osv-scanner/).

    *   **Install `nmap` (for port scanning):**
        `nmap` is a system dependency. Install it using your system's package manager (e.g., `sudo apt-get install nmap` on Debian/Ubuntu).

## Configuration

`bughunter-cli` requires a few API keys to unlock its full potential.

### 1. Gemini API Key (for AI features)

The AI analysis and payload generation features are powered by Google Gemini.

1.  Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Create a `.env` file in the root of the project directory.
3.  Add your API key to the `.env` file:
    ```
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```

### 2. GitHub Personal Access Token (for GitHub integration)

To interact with GitHub, you need to provide a Personal Access Token (PAT).

1.  Generate a PAT from your GitHub account settings. Ensure it has the necessary scopes (`repo`, `read:org`).
2.  Run the `github init` command and paste your token when prompted. The token will be stored securely in a local configuration file (`~/.bughunter_config`).
    ```bash
    bughunter github init
    ```

## Usage

Here is a detailed breakdown of all available commands.

### VibeOps Commands

---

#### `vibe`: Natural Language Interface

Interact with `bughunter-cli` using conversational language. The AI will interpret your request and execute the appropriate command.

*   **Examples:**
    ```bash
    bughunter vibe "find subdomains for example.com"
    bughunter vibe "scan ports on example.com"
    bughunter vibe "look for xss payloads for a php app"
    ```

#### `tags`: List VibeOps Engineering Tags

Displays the VibeOps concepts and tags associated with this tool.

```bash
bughunter tags
```

### General Commands

---

#### `scan`: Perform Reconnaissance and Scanning

Commands for scanning and enumerating targets.

*   **Find Subdomains:**
    ```bash
    bughunter scan subdomains --target example.com
    ```

*   **Scan Open Ports:**
    Uses `nmap` to scan the most common ports.
    ```bash
    bughunter scan ports example.com --top-ports 100
    ```

*   **Scan Code:**
    Scans a file or directory for vulnerabilities using Semgrep.
    ```bash
    bughunter scan code ./path/to/your/code
    ```

*   **Scan Dependencies:**
    Scans project dependencies for known vulnerabilities.
    ```bash
    bughunter scan dependencies ./path/to/your/project
    ```

---

#### `ai`: AI-Powered Security Analysis

Leverage AI to enhance your security workflow.

*   **Analyze a Target:**
    Performs subdomain enumeration and then sends the results to the AI for a comprehensive security analysis.
    ```bash
    bughunter ai analyze --target example.com
    ```

*   **Generate Attack Payloads:**
    Create context-aware payloads for various vulnerability types.
    ```bash
    bughunter ai generate-payloads --type xss --target-tech "React with Node.js backend"
    ```

---

### GitHub Integration

---

#### `github`: Interact with GitHub Repositories

*   **Initialize GitHub Token:**
    (Required before using other GitHub commands)
    ```bash
    bughunter github init
    ```

*   **Pull Issues:**
    Fetch issues from a repository.
    ```bash
    bughunter github issues pull --repo owner/repo --state open
    ```

*   **Create a Pull Request:**
    ```bash
    bughunter github pr create --repo owner/repo --title "My New Feature" --head feature-branch --base main
    ```

*   **Push a Comment:**
    Add a comment to an issue or pull request.
    ```bash
    bughunter github comments push --repo owner/repo --issue 123 --body "This looks great!"
    ```

---

### Project & Package Management

---

#### `publish`: Build and Publish Your Package

*   **Initialize Credentials:**
    Displays instructions on how to set up your PyPI credentials using environment variables.
    ```bash
    bughunter publish init
    ```

*   **Publish the Package:**
    Builds the package using `build` and uploads it to PyPI using `twine`.
    ```bash
    # Publish to PyPI
    bughunter publish do

    # Publish to TestPyPI
    bughunter publish do --repository testpypi
    ```

---

#### `autoclean`: Clean Your Project Directory

Removes temporary files and build artifacts. Asks for confirmation before deleting the virtual environment.

```bash
bughunter autoclean
```

---

### Other Commands

*   **`hello`**: A simple command to test the CLI.
*   **`tag`**: Create a tag.
*   **`label`**: Add or remove a label from an item.
*   **`onboard`**: Simulate an onboarding process.

## Development

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
3.  Make your changes and commit them (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
