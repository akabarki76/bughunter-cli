# bughunter-cli 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![GitHub Stars](https://img.shields.io/github/stars/akabarki76/bughunter-cli)](https://github.com/akabarki76/bughunter-cli/stargazers)

> **The AI-powered command-line sentinel for modern security workflows**

bughunter-cli is an intelligent security toolkit that fuses cutting-edge vulnerability scanners with Large Language Models to revolutionize bug hunting, security analysis, and development workflows. Built on **VibeOps** principles, it transforms security from a chore into a seamless, conversational experience.

##  Why bughunter-cli?

| Traditional Tools               | bughunter-cli Advantage          |
|---------------------------------|----------------------------------|
| Siloed scanners                 | Unified AI-powered workflow      |
| Manual interpretation           | Natural language insights        |
| Reactive fixes                  | Proactive AI autocorrection      |
| Toolchain complexity            | Single-command simplicity        |
| Static capabilities             | Continuously evolving with AI    |

##  Key Features

###  AI-Powered Intelligence
- **Conversational Interface**: `bughunter vibe "Find XSS vulnerabilities in auth module"`
- **Autocorrection**: AI-generated patches for identified vulnerabilities
- **Contextual Analysis**: LLM-powered vulnerability interpretation

###  Comprehensive Scanning Suite
```bash
# Code scanning (Semgrep-powered)
bughunter scan code ./src --autocorrect

# Dependency analysis (OSV-scanner)
bughunter scan dependencies ./requirements.txt

# Infrastructure recon
bughunter scan subdomains example.com
bughunter scan ports 192.168.1.1
```

###  GitHub Integration
```bash
# Initialize GitHub integration
bughunter github init

# Manage security findings as issues
bughunter github create-issue "SQLi vulnerability detected"
```

### ️ Extensible Architecture
- Language-agnostic scanning
- Plugin system for new scanners
- Future-proof AI integration points

##  Getting Started

### Prerequisites
- Python 3.9+
- [Gemini API Key](https://aistudio.google.com/)
- [GitHub PAT](https://github.com/settings/tokens)

### Installation
```bash
git clone https://github.com/akabarki76/bughunter-cli.git
cd bughunter-cli
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Install security scanners
brew install nmap cppcheck    # macOS
sudo apt-get install nmap cppcheck  # Debian/Ubuntu
```

### Configuration
```bash
# Set Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Configure GitHub integration
bughunter github init
```

##  Usage Examples

### Basic Scanning
```bash
# Scan Python project with autocorrection
bughunter scan code ./project --autocorrect

# Find vulnerable dependencies
bughunter scan dependencies ./project
```

### Natural Language Interface
```bash
bughunter vibe "Audit authController.js for injection flaws"
bughunter vibe "Explain CVE-2023-12345 in simple terms"
bughunter vibe "Generate patch for the SQLi in userService.py"
```

### Advanced Workflows
```bash
# Full security audit pipeline
bughunter vibe "Scan entire project, fix critical issues, and create GitHub tickets"

# CI/CD integration (example)
- name: Security Audit
  run: |
    bughunter scan code ./src
    bughunter scan dependencies
```

##  VibeOps Philosophy

bughunter-cli embodies our core engineering principles:
1. **AI-First Automation** - Machines handle routine tasks, humans solve hard problems
2. **Conversational DevEx** - Natural language as primary interface
3. **Continuous Evolution** - Always integrating cutting-edge AI research
4. **Inclusive Security** - Democratizing security expertise

## ️ Roadmap
- [ ] AI-assisted refactoring engine
  - `bughunter refactor <file_path> --prompt "Refactor this code to be more performant"`
- [ ] Interactive vulnerability learning modules
  - `bughunter learn "sql-injection"`
- [ ] Dependency impact forecasting
  - `bughunter forecast <dependency_name>@<version>`
- [ ] Multi-LLM support (Claude, GPT, OSS models)
  - `bughunter config set llm.provider openai`
- [ ] Visual vulnerability mapping
  - `bughunter map vulnerabilities --output <file_path.html>`

##  Contributing
We welcome contributions from developers of all backgrounds! See our:
- [Contributor Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

Special encouragement for contributions from underrepresented groups in security.

##  License
MIT © [Your Name] - See [LICENSE](LICENSE) for details
