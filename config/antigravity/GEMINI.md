# Global Instructions & Guidelines for AI

> These rules and guidelines will be automatically applied to every task requested in **Antigravity CLI (agy)** and **Antigravity IDE**.

## 1. Communication & Style
- Communicate in the exact language used in the user's prompt.
- If the prompt contains both a question and an action/task, answer the question and ignore the task.
- **Character Mapping / Typo Correction**: Whenever the Arabic character "٩" (Arabic-Indic digit 9, U+0669) is received in user prompts or text input, treat and understand it as the Arabic letter "ج" (jeem) (e.g., "أ٩ل" -> "أجل"), and output/write it as "ج" in all Arabic responses and generated files.

## 2. Coding Standards & Directory Architecture
- Write clean, well-structured, and reusable code.
- Use meaningful and descriptive names for variables and functions.
- Add explanatory comments for complex logic.
- Avoid large source files; break down any large codebase into modular sub-files.
- Every code directory must include a `README.md` file briefly explaining each file within that directory and its purpose (ignore system and build directories such as `.git`, `node_modules`, `dist`, `build`, `venv`, and `target`).
- When inspecting or accessing a directory for the first time, check for and read its `README.md` first to quickly understand the directory structure and file purposes before scanning other files.
- Automatically update the relevant directory's `README.md` whenever files within it are added, removed, or significantly altered.
- Perform targeted, incremental edits rather than rewriting entire large files whenever possible.

## 3. Git Workflow & Version Control
- Every request that involves modifying code or text files must include a Git commit describing the changes made.
- Follow the Conventional Commits format for commit messages (e.g., `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`).
- If the project does not contain a `./.git` directory, run `git init` first, then commit.
- The default initial branch for any repository/project must always be named `main`.
- If the project is linked to a remote repository and work is done on the main branch, run `git push origin main`.

## 4. Safety & Security Guardrails
- Never execute destructive or irreversible commands (such as `rm -rf`, `git reset --hard`, `git push --force`, or deleting databases) without explicit user confirmation.
- Never hardcode or commit sensitive credentials, API keys, private tokens, or secrets into source files or commit messages; ensure they remain isolated in environment variables (`.env`).

## Agent Rules Hierarchy & Markdown Governance

- **Universal Markdown Ingestion & Enforcement:**
  - Before executing any task, proactively discover, read, and ingest all Markdown (`*.md`) files present within the project (including root docs, sub-directory `README.md` files, and any files located inside `.agent/`).
  - Every operation, modification, and architectural decision within the project is strictly subordinate to the instructions defined across these Markdown files.

- **Conflict Prevention & Autonomous Resolution:**
  - Instructions and configurations must not intentionally conflict.
  - If a conflict arises between general instructions and project-level specifications (or between overlapping Markdown guides), prioritize project-specific `.agent/` guidelines first.
  - In all other conflict scenarios, the agent must autonomously evaluate the context and resolve the discrepancy in the most pragmatic, safe, and robust manner suitable for the project workflow—without blocking execution or requiring manual user intervention
