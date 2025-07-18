# Command Reference

This document provides a comprehensive reference for all `bughunter-cli` commands.

## Core Commands

### `scan`

Analyzes code, dependencies, and infrastructure for security vulnerabilities.

**Usage:**
```bash
bughunter scan <subcommand> [options]
```

**Subcommands:**

*   `code <path>`: Scans a directory for code vulnerabilities.
    *   `--autocorrect`: Automatically apply AI-generated patches.
*   `dependencies <path>`: Scans a dependency file (e.g., `requirements.txt`).
*   `subdomains <domain>`: Discovers subdomains for a given domain.
*   `ports <ip_address>`: Scans for open ports on a given IP address.

### `vibe`

Uses a natural language interface to perform security tasks.

**Usage:**
```bash
bughunter vibe "<prompt>"
```

**Examples:**
```bash
bughunter vibe "Find XSS vulnerabilities in the auth module"
bughunter vibe "Explain CVE-2023-12345 in simple terms"
bughunter vibe "Generate a patch for the SQLi in userService.py"
```

### `github`

Integrates with GitHub to manage security issues.

**Usage:**
```bash
bughunter github <subcommand> [options]
```

**Subcommands:**

*   `init`: Initializes the GitHub integration.
*   `create-issue "<title>"`: Creates a new GitHub issue for a security finding.

## Roadmap Commands

These commands are planned for future releases.

### `refactor`

AI-assisted code refactoring.

**Usage:**
```bash
bughunter refactor <file_path> --prompt "<description>"
```

### `learn`

Interactive vulnerability learning modules.

**Usage:**
```bash
bughunter learn "<vulnerability_name>"
```

### `forecast`

Dependency impact forecasting.

**Usage:**
```bash
bughunter forecast <dependency_name>@<version>
```

### `config`

Configuration for `bughunter-cli`.

**Usage:**
```bash
bughunter config set llm.provider <provider_name>
```

### `map`

Visual vulnerability mapping.

**Usage:**
```bash
bughunter map vulnerabilities --output <file_path.html>
```