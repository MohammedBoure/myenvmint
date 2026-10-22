# Antigravity Multi-Agent Role Templates (`config/antigravity/roles/`)

This directory houses the foundational system prompt and instruction templates assigned to autonomous Antigravity CLI (`agy`) instances based on their deterministic ID ranges.

## Files & Purposes

- **`orchestrator.md`**:
  Template for Lead Orchestrators / Project Managers (`agy1` – `agy10`). Defines the `-mind` exception mode, oversees the 200-agent fleet, enforces high-level strategic reasoning, prohibits direct source-code reading, manages MCP inter-agent communications, dynamic agent governance, and executes final release merges into `main`.

- **`backend.md`**:
  Template for Backend Logic & Systems Engineers (`agy11` – `agy50`). Specializes in business logic, database structures, computations, API design, mandatory English `README.md` maintenance, strict feature branching (`backend/agy[x]-<feature>`), and test handoffs.

- **`frontend.md`**:
  Template for Frontend & Interface Auditors (`agy51` – `agy100`). Focuses on reusable UI components, layout structures, state bindings, responsive design, accessibility, and strict alignment with backend API contracts (`frontend/agy[x]-<component>`).

- **`test.md`**:
  Template for Quality Gatekeepers & Pragmatic Test Engineers (`agy101` – `agy150`). Holds exclusive merge authority for integrating feature branches into `develop`. Mandates pragmatic, high-value verification without artificial coverage chasing (`test/agy[x]-<scope>`).

- **`ux.md`**:
  Template for UX Finishing, Polish & Performance Specialists (`agy151` – `agy200`). Specializes in non-invasive styling polish, micro-interactions, responsive refinements, asset optimization, and loading states (`ux/agy[x]-<polish>`).
