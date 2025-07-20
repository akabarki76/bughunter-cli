# Getting Started with `bughunter-cli`

Welcome to the `bughunter-cli` community! This guide will walk you through the process of installing, configuring, and running your first scan.

## 1. Installation

`bughunter-cli` is designed to be easy to install. It relies on a few external tools for its powerful scanning capabilities, so we'll install those as well.

### Step 1: Clone the Repository

First, clone the `bughunter-cli` repository to your local machine:
```bash
git clone https://github.com/AKA-NETWORK/bughunter-cli.git
cd bughunter-cli
```

### Step 2: Create a Virtual Environment

It is highly recommended to use a Python virtual environment to avoid conflicts with system-wide packages.
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

### Step 4: Install `bughunter-cli`

Install the tool in editable mode. This makes the `bughunter` command available in your terminal and ensures that any changes you pull from the repository are immediately reflected.
```bash
pip install -e .
```

### Step 5: Install External Scanners

`bughunter-cli` uses specialized external tools for some of its scans. Please install them using your system's package manager.

*   **For Web and General Code Scanning:**
    *   `semgrep`: `pip install semgrep` (should be handled by `requirements.txt`)
*   **For Dependency Scanning:**
    *   `osv-scanner`: Follow the official instructions at [google.github.io/osv-scanner/](https://google.github.io/osv-scanner/)
*   **For Embedded Systems (C/C++):**
    *   `cppcheck`: `sudo apt-get install cppcheck` (or your system's equivalent)
*   **For Network Reconnaissance:**
    *   `nmap`: `sudo apt-get install nmap` (or your system's equivalent)

## 2. Configuration

To unlock the full power of `bughunter-cli`, you need to configure your API keys.

### Gemini API Key (for AI features)

1.  Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Create a `.env` file in the root of the project directory.
3.  Add your API key to the `.env` file:
    ```
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```

### GitHub Personal Access Token (for GitHub integration)

1.  Generate a Personal Access Token (PAT) from your GitHub account settings.
2.  Ensure your PAT has the `repo` and `read:org` scopes.
3.  Run the `init` command and paste your token when prompted:
    ```bash
    bughunter github init
    ```
    Your token will be stored securely in a local configuration file.

## 3. Running Your First Scan

You are now ready to run your first scan!

*   **To scan a web project for vulnerabilities:**
    ```bash
    bughunter scan web /path/to/your/web-project
    ```

*   **To scan a C/C++ project for common errors:**
    ```bash
    bughunter scan c-cpp /path/to/your/embedded-project
    ```

*   **To scan your project's dependencies for known vulnerabilities:**
    ```bash
    bughunter scan dependencies .
    ```

*   **To try the AI-powered autocorrection:**
    ```bash
    bughunter scan code /path/to/your/code --autocorrect
    ```

## Next Steps

You are now ready to explore the full capabilities of `bughunter-cli`. We recommend you check out the following pages:
*   **[Command Reference](./Command-Reference.md):** For a detailed list of all commands.
*   **[Web Engineering](./Web-Engineering.md):** For guides on securing web applications.
*   **[Embedded Systems Security](./Embedded-Systems-Security.md):** For guides on securing embedded systems.
