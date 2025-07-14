# `bughunter-cli` 🐞

**An AI-native command-line interface for advanced bug hunting, security analysis, and automated development workflows.**

`bughunter-cli` is a next-generation tool that integrates powerful security scanners with Large Language Models (LLMs) to provide a seamless, intelligent, and future-proof solution for developers, security researchers, and penetration testers.

## VibeOps Engineering

`bughunter-cli` is built on the principles of **VibeOps**, an engineering culture that leverages AI and natural language to automate and simplify the entire software development lifecycle. This tool embodies the VibeOps philosophy by:

- **Enhancing Developer Experience (DevEx):** Providing a seamless, conversational interface to complex security and development tasks.
- **AI-Assisted Workflow:** Using LLMs to automate reconnaissance, vulnerability analysis, and even code patching.
- **CI/CD and Automation:** Automating routine tasks to streamline development and security operations.
- **AI SRE:** Moving towards a future of AI-driven Site Reliability Engineering, where monitoring and remediation are increasingly automated.

## Key Features

*   **AI-Powered Autocorrection:** Automatically find and fix vulnerabilities in your code with AI-generated patches.
*   **Natural Language Interface:** Interact with the tool using conversational language via the `vibe` command.
*   **Comprehensive Scanning:**
    *   **Code Scanning:** Language-agnostic vulnerability scanning with Semgrep.
    *   **Dependency Scanning:** Find known vulnerabilities in your project's dependencies using `osv-scanner`.
    *   **Reconnaissance:** Discover subdomains and scan for open ports.
*   **Full GitHub Integration:** Manage issues, pull requests, and comments directly from your terminal.
*   **Extensible and Future-Proof:** Designed to be a constantly evolving platform that will integrate new AI and security technologies as they emerge.

## Future-Proofing `bughunter-cli`

The world of AI and cybersecurity is evolving at an unprecedented pace. `bughunter-cli` is designed to be a living project that will continuously adapt and integrate the latest advancements. Our commitment is to keep this tool at the forefront of technology, ensuring it remains an essential part of any modern development workflow.

We are actively exploring and developing features in areas such as:

*   **AI-Driven Refactoring:** Suggesting improvements to code structure, readability, and performance.
*   **Advanced Dependency Management:** Proactively managing dependency updates and assessing their security impact.
*   **Interactive Learning:** Creating a more engaging and educational experience by teaching users about the vulnerabilities found in their code.

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
    ```bash
    pip install -e .
    ```

5.  **Install External Scanners:**
    *   **`osv-scanner`:** [google.github.io/osv-scanner/](https://google.github.io/osv-scanner/)
    *   **`nmap`:** `sudo apt-get install nmap` (or your system's equivalent)
    *   **`cppcheck`:** `sudo apt-get install cppcheck` (or your system's equivalent)


## Configuration

`bughunter-cli` requires API keys for its AI and GitHub features.

*   **Gemini API Key:** Obtain a key from [Google AI Studio](https://aistudio.google.com/app/apikey) and set it as `GEMINI_API_KEY` in a `.env` file.
*   **GitHub Personal Access Token:** Run `bughunter github init` and provide a PAT with `repo` and `read:org` scopes.

## Usage

### VibeOps Commands

*   **`vibe <prompt>`:** Interact with the tool using natural language.
    *   `bughunter vibe "find subdomains for example.com"`
*   **`tags`:** List the VibeOps engineering tags.

### Scanning Commands

*   **`scan code <path> [--autocorrect]`:** Scan code for vulnerabilities and optionally apply AI-powered fixes.
*   **`scan web <path> [--autocorrect]`:** Scan a web project for vulnerabilities and optionally apply AI-powered fixes.
*   **`scan c-cpp <path>`:** Scan C/C++ code for vulnerabilities using `cppcheck`.
*   **`scan dependencies <path>`:** Scan project dependencies for known vulnerabilities.
*   **`scan subdomains <target>`:** Find subdomains for a target.
*   **`scan ports <target>`:** Scan for open ports.

---

*For a full list of commands and options, run `bughunter --help`.*

## Our Community

**This project is more than just code; it's a community.** We are committed to building a welcoming, inclusive, and safe environment for everyone.

Our most important task is to create a space where engineers from all backgrounds, especially those from ethnic minorities and other underrepresented groups in technology, can thrive. We believe that the best tools are built by diverse teams, and we are dedicated to making that a reality.

Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) and our [Contributing Guide](./CONTRIBUTING.md) to learn more about our values and how you can get involved.

## Development

Contributions are welcome! Please see `CONTRIBUTING.md` for more details.

## License

This project is licensed under the MIT License.