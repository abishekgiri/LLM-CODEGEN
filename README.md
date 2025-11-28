# LLM-CODEGEN
LLM-CODEGEN
Multi-Strategy Evaluation of LLM-Driven Code Generation & Automated Self-Repair

Using Groq LLaMA-3.1-8B-Instant

This repository contains a complete research framework for evaluating how different prompting and repair strategies affect the correctness of LLM-generated code. The system automatically generates code, tests it, repairs it, analyzes performance, and logs results across multiple tasks and strategies.

This project was developed for a research study titled:
“Multi-Strategy Evaluation of LLM-Driven Code Generation and Automated Repair Using Groq LLaMA Models.”

Features
Automated Code Generation

Uses Groq’s LLaMA-3.1-8B-Instant model to generate Python functions from natural-language task descriptions.

Automated Testing

Each generated function is evaluated against multiple test cases.

Three Repair Loops + One Reviewer Strategy

The framework supports:

no_repair – only generate once

repair_3 – up to 3 iterative self-repairs

repair_5 – up to 5 iterative repairs

review_then_repair_3 – a dedicated reviewer agent critiques code before repairs

Static Analysis (flake8)

Counts code-quality issues before and after repairs.

12 Task Benchmark

Tasks range from simple to advanced:

Reverse string

Sum list (ignore non-numbers)

Safe divide

Longest word extraction

Character frequency

Unique list

Email validation

Running average

Second largest number

Balanced parentheses

CSV user parser

Door Finite State Machine (FSM)

Experiment Pipeline

run.py → run a single test suite

run_experiments.py → multi-run simple strategies

run_experiments_advanced.py → multi-run + reviewer + static analysis

analyze_experiments.py → statistics for simple runs

analyze_experiments_advanced.py → cross-strategy statistical review

Key Findings (Your Research Results)
1. Simple Tasks = Perfect Performance

Reverse string, safe divide, running average, and character frequency achieved 100% pass rate across all strategies.

2. Moderate Tasks Benefit From Repair

Tasks like “unique list” and “sum list (ignore invalid values)” improved when repair strategies or reviewer strategies were applied.

 3. Hard Reasoning Tasks Fail Completely

Even after 5 repair attempts and reviewer help, the model failed:

Longest word

Email validation

Second-largest detection

Balanced parentheses
These tasks require multi-step logical reasoning — an area where 8B models struggle.

4. Reviewer Agent Unlocks New Capabilities

Only the review_then_repair_3 strategy successfully solved the door finite-state machine (FSM) task —
no other strategy solved this task even once.

5. CSV Parsing Remains Unsolved

The model repeatedly generated brittle or incorrect parsing logic.
Neither repair strategies nor reviewer scaffolding solved the task.

6. Token Limits Matter

repair_5 sometimes triggered Groq rate-limit / token-limit errors, showing practical constraints of iterative repair with smaller context windows.

Technical Architecture
├── run.py
├── run_experiments.py
├── run_experiments_advanced.py
├── analyze_experiments.py
├── analyze_experiments_advanced.py
├── src/
│   ├── code_generator.py
│   ├── repair_loop.py
│   ├── reviewer.py
│   ├── evaluator.py
│   ├── analyzer.py
│   ├── static_analysis.py
│   └── task_loader.py
├── tasks.json
└── results/

 How to Run
1. Install dependencies
pip install -r requirements.txt

2. Set your Groq API key
export GROQ_API_KEY="your_key_here"

3. Run a single task suite
python3 run.py

4. Run multi-run experiments
python3 run_experiments.py

5. Run advanced multi-strategy experiments
python3 run_experiments_advanced.py

6. Analyze results
python3 analyze_experiments.py
python3 analyze_experiments_advanced.py

Research Summary

This project evaluates how well the Groq LLaMA-3.1-8B-Instant model generates and repairs Python code across different difficulties. The results show that:

Small LLMs excel at simple transformations.

They struggle with algorithmic reasoning.

Repair cycles alone don’t fix deep reasoning failures.

Reviewer-augmented prompting dramatically improves results on complex logic tasks like FSMs.

This suggests that multi-agent systems may be necessary for LLM-assisted programming in real engineering environments.

Future Work

Try larger LLMs (70B+) to compare reasoning abilities

Add symbolic tools (regex engines, AST evaluators, etc.)

Integrate CI/CD pipeline execution

Explore memory-augmented models

Expand dataset to 50–100 algorithmic tasks
