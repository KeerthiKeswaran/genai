# Assignment: Workflow vs. Agent Integration

This document outlines two approaches to automating a client scheduling process: one using a structured workflow, and another using a dynamic AI agent.

---

## Scenario: Client Form Submission & Meeting Scheduler

When a potential client submits an interest form, the system captures their name, email, query, meeting preference (Yes/No), and preferred time slot (if any).

---

## Approach 1: The Predictable Workflow

A series of fixed, hardcoded steps connected by logical gates.

```text
[ Google Form Submitted ]
          │
          ▼
[ Save to Google Sheets ]
          │
          ▼
  / Willing to Meet? \
 ├─────── No ────────► [ Send Welcoming Email ]
 └─────── Yes ───────► [ Check Google Calendar ]
                             │
                      / Slot Available? \
                     ├────── Yes ───────► [ Create Calendar Event ] ──► [ Send Email with Meeting Link ]
                     └────── No ────────► [ Send Email: Slot Unavailable ]
```

### Explanation
- **How it works:** Each action strictly triggers the next based on predefined logic (if/else conditions).
- **Limitation:** The client's preferred slot must be in a strict format (e.g., `YYYY-MM-DD HH:MM`). If a client writes *"Monday around 3 PM"*, the workflow cannot parse it and fails.

---

## Approach 2: The Dynamic Agent

An LLM-driven assistant that evaluates the input and determines which tools to use.

```text
[ Google Form Submitted ]
          │
          ▼
[ Save to Google Sheets ]
          │
          ▼
[ LLM Agent Evaluates Client Input ]
          │
     (Agent decides tools to use)
          │
          ├── Client wants meeting ──► Tool 1: Google Calendar (Search & Book) ──► Tool 2: Gmail (Send confirmation/update)
          └── Client does not want ──► Tool 2: Gmail (Draft and send customized welcome email)
```

### Explanation
- **How it works:** Instead of rigid rules, the LLM reads the form submission (even if written in conversational language like *"sometime Tuesday morning"*), interprets the intent, and chooses the right tools (Calendar, Sheets, Gmail) to resolve the request.
- **Strength:** Extremely flexible. If the client asks a question instead of just requesting a meeting, the Agent can draft a response answering the query directly.

---

## Comparison & Justification

| Feature | Predictable Workflow | Dynamic Agent |
| :--- | :--- | :--- |
| **Logic** | Fixed, deterministic paths | Flexible, reasoning-based paths |
| **Input Handling** | Requires strict, formatted data | Handles natural, conversational text |
| **Complexity** | Simple to debug and test | More complex, non-deterministic outputs |
| **Error Rate** | Very low (except for format mismatches) | Variable (dependent on LLM accuracy) |

### When to use a Predictable Workflow
- When the business process is highly standardized, repeatable, and has clear binary decisions.
- When formatting can be enforced at the input level (e.g., standard drop-downs and calendar selectors).
- When a 100% guarantee of execution behavior is required (e.g., billing or database insertion).

### When to use a Dynamic Agent
- When user inputs are open-ended or conversational.
- When the steps depend on semantic understanding (e.g., analyzing a client's message tone or answering a specific question).
- When the sequence of tools might change based on the situation (e.g., choosing to email, schedule, or escalate to support).
