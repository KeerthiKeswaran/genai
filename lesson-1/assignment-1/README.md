# Assignment-1: Performance Evaluation of Local LLMs

## Objective & Overview
The objective of this assignment is to establish a **zero-shot baseline** for three local Large Language Models (LLMs) running via Ollama. By querying the models with complex technical prompts across three distinct domains—Application Development (AppDev), Data Science (Data), and DevOps—without providing any organizational guidelines or contextual examples, we evaluate their raw, out-of-the-box coding capabilities, reasoning skills, and format compliance.

The three models evaluated are:
1. **Google Gemma 2 (2.6B)** (`gemma2:2b`)
2. **Microsoft Phi-3 (3.8B)** (`phi3:latest`)
3. **TinyLlama (1.1B)** (`tinyllama:latest`)

---

## Requirements & Prerequisites
Before running the evaluation scripts, ensure you have the following installed:
* **Python**: Version 3.10 or higher.
* **Ollama**: Local runner for large language models.
* **Local Models**: The following models must be pulled in Ollama:
  ```bash
  ollama pull gemma2:2b
  ollama pull phi3:latest
  ollama pull tinyllama:latest
  ```

---

## Setup & Execution Instructions

1. **Install Dependencies**:
   Install the required Python package:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Ollama is Running**:
   Ensure the Ollama daemon is active. You can verify this by listing installed models:
   ```bash
   ollama list
   ```

3. **Run the Evaluations**:
   Navigate to the respective model directories and execute the evaluation scripts:
   * **Gemma 2 Evaluation**:
     ```bash
     python gemma2/gemma2_eval.py
     ```
   * **Phi-3 Evaluation**:
     ```bash
     python phi3/phi3_eval.py
     ```
   * **TinyLlama Evaluation**:
     ```bash
     python tinyllama/tinyllama_eval.py
     ```

Each script will send three prompts (AppDev, Data, and DevOps) to the respective model and save the generated markdown/text responses locally in files like `{model}_{domain}.txt`.

---

## Detailed Performance & Response Comparison

The following table summarizes the performance and code quality metrics observed during the zero-shot baseline run:

| Parameter | Google Gemma 2 (2.6B) | Microsoft Phi-3 (3.8B) | TinyLlama (1.1B) |
| :--- | :--- | :--- | :--- |
| **Syntactic Correctness** | **Excellent**: Python, SQL, and Terraform configurations compile and run with virtually no syntax errors. | **Very Good**: Minor indentation adjustments needed occasionally in YAML/Terraform, but Python is syntactically sound. | **Poor**: Often generates incomplete scripts, mismatched braces, or invalid syntax blocks under complex prompts. |
| **Code Structure & Logic** | **Sophisticated**: Implements robust thread-locks in Python, accounts for performance index tips in SQL, and structures Terraform modules correctly. | **Good**: Logic is highly standard and boilerplate-focused. Lacks some optimization nuances in complex SQL joins. | **Weak**: Struggles to maintain code logic across longer generations. The PostgreSQL pool lacked actual thread-safe logic. |
| **Response Latency (Time-to-First-Token & Generation Speed)** | **Moderate**: Takes slightly longer to process prompts but produces dense, high-quality code chunks at steady speeds. | **Fast**: Highly optimized prompt processing, delivering quick responses with standard structures. | **Extremely Fast**: Almost zero latency, but speed is offset by high rates of repetition and incomplete code. |
| **Instruction Adherence (Formatting/Explanations)** | **High**: Follows formatting instructions (e.g., "code only") accurately, with minimal conversational prefix. | **Medium**: Prone to adding verbose explanations even when requested to output only code blocks. | **Low**: Frequently hallucinates instructions, loops on text generation, or ignores negative constraints. |
| **AppDev Code Quality (PostgreSQL Connection Pool)** | **Excellent**: Used threading locks, defined clear init params, and implemented proper release/get methods. | **Good**: Implemented basic locking, but lacks comprehensive connection validation or cleanup logic. | **Poor**: Simple array manipulation with no thread safety, validation, or actual recycling. |
| **Data SQL Quality (Top 5 Customers)** | **Excellent**: Explicit JOINs, window functions, and well-thought-out suggestions for B-Tree indices. | **Very Good**: Syntactically clean SQL query, though performance analysis was less thorough. | **Poor**: Mismatched columns and invalid aggregation logic inside the subqueries. |
| **DevOps Terraform (VPC & ALB)** | **Very Good**: Proper block layouts, security groups, and correct routing associations. | **Good**: Standard configuration, but missed several required tag fields or security rules. | **Failed**: Produced broken nested syntax that fails HCL validation. |

---

## Key Takeaways from the Baseline
* **Gemma 2 (2.6B)** punches well above its weight class, delivering the most syntactically robust and logically sound outputs.
* **Phi-3 (3.8B)** is a highly reliable general coder but tends to be wordy and sometimes overlooks constraints in prompt requests.
* **TinyLlama (1.1B)** is suitable only for extremely simple text-completion tasks and fails to produce production-grade code or configs in zero-shot settings due to its low parameter capacity.
