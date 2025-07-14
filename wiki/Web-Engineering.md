# Guide: Web Engineering Security

This guide provides best practices and examples for using `bughunter-cli` to secure your web applications and APIs.

## Philosophy

Modern web applications are complex systems with many moving parts. Securing them requires a multi-layered approach, from analyzing the frontend code to hardening the backend APIs and server configurations. `bughunter-cli` is designed to be your trusted companion throughout this process.

## Core Workflow

A typical web security workflow with `bughunter-cli` looks like this:

1.  **Scan for Dependencies:** Start by checking your project for known vulnerabilities in your third-party libraries.
    ```bash
    bughunter scan dependencies .
    ```

2.  **Run a Targeted Web Scan:** Use the `scan web` command to find common web vulnerabilities like XSS, SQL Injection, and insecure configurations.
    ```bash
    bughunter scan web /path/to/your/project
    ```

3.  **Use AI-Powered Autocorrection:** For any vulnerabilities found, run the scan again with the `--autocorrect` flag to get AI-generated patches.
    ```bash
    bughunter scan web /path/to/your/project --autocorrect
    ```

4.  **Analyze Your API (if applicable):** If your project has an API, use the `ai analyze` command to get a high-level security assessment.
    ```bash
    # (Future command)
    # bughunter scan api --spec /path/to/openapi.json
    ```

5.  **Generate Payloads for Testing:** If you want to manually test a potential vulnerability, use `ai generate-payloads` to create custom payloads.
    ```bash
    bughunter ai generate-payloads --type xss --target-tech "react with a nodejs backend"
    ```

## Example: Securing a React Application

Let's say you have a React application that communicates with a Node.js backend. Here's how you could use `bughunter-cli` to secure it:

1.  **Check for vulnerable npm packages:**
    ```bash
    bughunter scan dependencies ./
    ```

2.  **Scan the frontend code for common React vulnerabilities:**
    ```bash
    bughunter scan web ./src --autocorrect
    ```
    This will look for issues like insecure use of `dangerouslySetInnerHTML`, missing security headers, and other common pitfalls.

3.  **Scan the backend Node.js code:**
    ```bash
    bughunter scan web ./server --autocorrect
    ```
    This will check for vulnerabilities like NoSQL injection, insecure middleware configuration, and potential prototype pollution.

## Best Practices

*   **Integrate into CI/CD:** Run `bughunter-cli` as part of your continuous integration pipeline to catch vulnerabilities before they reach production.
*   **Regularly Scan Dependencies:** The world of software dependencies is constantly changing. Run `scan dependencies` regularly to stay on top of new vulnerabilities.
*   **Don't Trust User Input:** Always treat input from users as untrusted. Use the findings from `bughunter-cli` to help you validate, sanitize, and encode all user-provided data.
*   **Stay Informed:** Use the `bughunter-cli` blog and other resources to stay up-to-date on the latest web security threats.
