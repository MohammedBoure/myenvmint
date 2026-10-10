# Antigravity CLI & IDE Configuration (`config/antigravity/`)

This directory contains the global guidelines, agent rules, and preferences for Google Antigravity CLI (`agy`) and Antigravity IDE.

## Files & Purposes

- **`GEMINI.md`**:
  The authoritative Global Instructions & Guidelines for AI. Contains mandatory rules for:
  - Communication & Style (language matching, Q&A handling, and Arabic character "٩" to "ج" mapping).
  - Coding Standards & Directory Architecture (clean code, modular structure, mandatory `README.md` per directory, targeted incremental edits).
  - Git Workflow & Version Control (commit on every change with Conventional Commits, main branch standard, git init if missing).
  - Safety & Security Guardrails (preventing destructive commands, protecting secrets).
  - Agent Rules Hierarchy & Markdown Governance (universal markdown ingestion, autonomous conflict resolution).

- **`AGENTS.md`**:
  Mirrors `GEMINI.md` to guarantee discovery across all Antigravity agent tools and hierarchical rules engines.

- **`settings.json`**:
  Saved preferences for Antigravity CLI (`agy`), configuring editor preferences, tool permission policies, and trusted workspace directories.
