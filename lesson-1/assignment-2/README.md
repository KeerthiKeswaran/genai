# Assignment-2: In-Context Learning (ICL) Coding Evaluation of Local LLMs

## Objective & Overview
The objective of this assignment is to evaluate the **In-Context Learning (ICL)** capabilities of local Large Language Models (LLMs) when provided with specific organizational guidelines, context documents, and constraints. By comparing these results against the zero-shot baseline established in Assignment-1, we assess how effectively the models can parse, respect, and apply strict rules (e.g., naming conventions, explicit security patterns, and schema regulations) injected into their prompt contexts.

The evaluation utilizes three reference context documents located in the `contexts/` directory:
1. `coding_standards.txt`: Python naming conventions, database locks, connection recycling, and docstring guidelines.
2. `schema_rules.txt`: Indexing rules, explicit table joins, and strict date extraction limitations for SQL.
3. `troubleshooting_guide.txt`: Specific route table definitions and security group rules to prevent ALB target group health-check failures.

---

## Requirements & Prerequisites
Before running the evaluation:
* Ensure **Python** (version 3.10+) is installed.
* Make sure **Ollama** is running locally with the following pulled models:
  ```bash
  ollama pull gemma2:2b
  ollama pull phi3:latest
  ollama pull tinyllama:latest
  ```

---

## Setup & Execution Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Context Files**:
   Confirm that the reference files (`coding_standards.txt`, `schema_rules.txt`, `troubleshooting_guide.txt`) are present in the `contexts/` directory:
   `lesson-1/assignment-2/contexts/`

3. **Run the Evaluations Orchestrator**:
   An orchestrator script `main.py` is provided to run all three evaluations sequentially:
   ```bash
   python main.py
   ```
   Alternatively, you can run individual scripts:
   ```bash
   python gemma2/gemma2_eval.py
   python phi3/phi3_eval.py
   python tinyllama/tinyllama_eval.py
   ```

Outputs will be saved as `{model}_{domain}.txt` inside each model's subdirectory.

---

## In-Context Learning vs. Zero-Shot Baseline Comparison

Injecting context significantly altered the behavior of all models. Below is an analysis of how each model adapted to guidelines in Assignment-2 compared to their raw zero-shot responses in Assignment-1:

### 1. Adherence to Rules & Guidelines

* **Google Gemma 2 (2.6B)**:
  * **Zero-Shot (A-1)**: Implemented a generic pool with normal Python conventions. No validation query, no connection age checks.
  * **In-Context (A-2)**: **Excellent adherence**. Correctly structured private members starting with an underscore (e.g., `_pool`), used PascalCase for `ConnectionPool`, added class docstrings, and utilized context-manager locks (`with self._lock:`). It attempted to incorporate lazy connection initialization, showcasing a strong capacity to adhere to in-context rules.
* **Microsoft Phi-3 (3.8B)**:
  * **Zero-Shot (A-1)**: Wrote standard code but with heavy verbose output and conversational filler.
  * **In-Context (A-2)**: **Very Good adherence**. Highly compliant with coding standards (implemented class-level docstrings, private helper methods, and strict sql constraints). However, it occasionally omitted validation queries (`SELECT 1`), showing slightly lower attention to minor sub-rules compared to Gemma 2.
* **TinyLlama (1.1B)**:
  * **Zero-Shot (A-1)**: Produced simple, mostly broken scripts with no standard styling.
  * **In-Context (A-2)**: **Struggled**. The model attempted to mirror the style and naming conventions (such as copying docstring headers), but the increased prompt length degraded its reasoning. It suffered from syntax fragmentation, proving that 1.1B models are easily overwhelmed by long context windows.

---

### 2. Parameter Comparison Table

| Metric | Assignment-1 (Zero-Shot) | Assignment-2 (In-Context Learning) |
| :--- | :--- | :--- |
| **Instruction Adherence Rate** | **Low (25%-45%)**: Models output standard public code but completely miss company-specific naming, security, or schema rules. | **High (75%-95%)**: Larger models (Gemma 2, Phi-3) strictly implement the naming constraints, structure requirements, and troubleshooting fixes. |
| **SQL Strictness (Data Domain)** | **Generic**: Generated standard queries. Joins were often implicit, and index considerations were generic. | **Highly Structured**: Applied explicit JOINs, avoided restricted date functions, and reference-matched the indexes mentioned in the `schema_rules.txt` context. |
| **Terraform Validity (DevOps)** | **Boilerplate**: Wrote simple VPC structures, often missing security details. | **Targeted Security**: Configured specific security group ingress rules and route table mappings to prevent the health check blockages described in the context guide. |
| **Average Latency & Prompt Processing** | **Low (0.5s - 1.5s)**: Fast initialization because prompts were short and simple. | **High (2.0s - 5.0s)**: Higher prompt tokens (due to reference document injections) increased prompt processing latency, especially on CPU-bound Ollama systems. |
| **Hallucination Rate** | **Moderate**: Occasional creation of invalid parameters or methods. | **Low**: Output was tightly bound to the context files. However, TinyLlama hallucinated parts of the guidelines itself. |

---

## Technical Insights
1. **Context Size Limitation**: In-context learning relies heavily on the model's attention mechanism. As contexts expand, smaller models (under 3B parameters) experience degradation in token retrieval accuracy (needle-in-a-haystack problem).
2. **System Prompts**: Injecting reference guides as System Prompts (`{"role": "system"}`) rather than User Prompts ensures the model processes constraints as instructions rather than raw queries, maximizing rule compliance.
