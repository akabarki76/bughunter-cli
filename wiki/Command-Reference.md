# Command Reference

This page provides a detailed reference for all `bughunter-cli` commands.

## Global Options

*   `--help`: Show help message and exit.

## `scan`: Perform Security Scans

This is the core group of commands for running security scans.

---

### `scan code <path>`

Scans a file or directory for general vulnerabilities using Semgrep.

*   **Arguments:**
    *   `<path>`: The path to the file or directory to scan.
*   **Options:**
    *   `--autocorrect`: Interactively find and fix vulnerabilities using AI.

---

### `scan web <path>`

Scans a web project for common web vulnerabilities (OWASP Top 10) using a targeted Semgrep ruleset.

*   **Arguments:**
    *   `<path>`: The path to the web project directory.
*   **Options:**
    *   `--autocorrect`: Interactively find and fix web vulnerabilities using AI.

---

### `scan c-cpp <path>`

Scans C/C++ code for common errors like buffer overflows, memory leaks, and undefined behavior using `cppcheck`.

*   **Arguments:**
    *   `<path>`: The path to the C/C++ file or directory.

---

### `scan dependencies <path>`

Scans your project's dependencies for known vulnerabilities against the GitHub Advisory Database using `osv-scanner`.

*   **Arguments:**
    *   `<path>`: The path to the project directory.

---

### `scan subdomains <target>`

Finds subdomains for a target domain using the `crt.sh` database.

*   **Arguments:**
    *   `<target>`: The target domain (e.g., `example.com`).

---

### `scan ports <target>`

Scans for the most common open ports on a target using `nmap`.

*   **Arguments:**
    *   `<target>`: The target IP address or domain.
*   **Options:**
    *   `--top-ports <number>`: The number of top ports to scan (default: 100).

## `ai`: AI-Powered Analysis

Commands for leveraging the power of Large Language Models.

---

### `ai analyze <target>`

Performs a comprehensive AI-powered security analysis of a target domain and its subdomains.

*   **Arguments:**
    *   `<target>`: The target domain.

---

### `ai generate-payloads`

Generates custom attack payloads for specific vulnerability types and technologies.

*   **Options:**
    *   `--type <type>`: The type of payload (e.g., `xss`, `sqli`). (Required)
    *   `--target-tech <tech>`: The target technology stack (e.g., `react`, `php`).

## `vibe`: VibeOps Engineering

Interact with `bughunter-cli` using natural language.

---

### `vibe <prompt>`

Interprets a natural language prompt and executes the corresponding command.

*   **Arguments:**
    *   `<prompt>`: The natural language command (e.g., `"find subdomains for example.com"`).

---

### `tags`

Displays the VibeOps engineering tags and concepts associated with this tool.

## `github`: GitHub Integration

Commands for interacting with GitHub repositories.

---

### `github init`

Initializes the GitHub integration by securely storing your Personal Access Token.

---

### `github issues pull`

Pulls issues from a GitHub repository.

*   **Options:**
    *   `--repo <owner/repo>`: The repository to pull issues from. (Required)
    *   `--state <open|closed|all>`: The state of the issues to pull (default: `open`).

---

### `github pr create`

Creates a new pull request.

*   **Options:**
    *   `--repo <owner/repo>`: The repository. (Required)
    *   `--title <title>`: The title of the pull request. (Required)
    *   `--head <branch>`: The branch where your changes are. (Required)
    *   `--base <branch>`: The branch you want to merge into (default: `main`).

---

### `github comments push`

Pushes a comment to a GitHub issue or pull request.

*   **Options:**
    *   `--repo <owner/repo>`: The repository. (Required)
    *   `--issue <number>`: The issue or PR number. (Required)
    *   `--body <body>`: The content of the comment. (Required)
