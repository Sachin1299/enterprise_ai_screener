# AI Engineer Transition — Progress Tracker

This document tracks current standing, completed modules, active sessions, and upcoming waves as defined in `AiEngineer_Plan.xlsx`.

---

## 📌 Overall Summary
- **Total Roadmap Topics:** 225
- **Already Learned / Marked Done:** 163 / 225 (~72%)
- **Active Wave:** Wave 3 — Ship and Operate
- **Primary Project:** [`chat_app`](file:///c:/Users/DELL/Desktop/Programs/Python/chat_app) (FastAPI + LangChain + ChromaDB + Gemini + Langfuse)

---

## 🌊 Wave Breakdown & Status

### Wave 1: GenAI Fundamentals (Must) — *COMPLETED*
- [x] **1.1: How LLMs work + API parameters** *(Inference, tokens, context windows, temperature/sampling, max tokens)*
- [x] **1.2: Hallucination, grounding, model selection** *(Hallucination causes, grounding strategies, cost/latency tradeoffs, model tiers)*
- [x] **1.3: Production Prompt Engineering** *(Role, instruction, context design, delimiters, structured output, negative constraints)*
- [x] **1.4: Resilient LLM calls** *(Error handling, retries with exponential backoff + jitter, rate limits 429, auth fail-fast, FastAPI exception handlers)*

---

### Wave 2: RAG & Agent Depth (Must) — *COMPLETED*
- [x] **2.1: RAG answer quality** *(Citations, page-level attribution, BM25 vs Vector search trade-offs, Cross-Encoder reranking)*
- [x] **2.2: RAG evaluation & Langfuse evals** *(RAG Triad, Faithfulness, Answer Relevancy, Golden dataset, LLM-as-a-judge, Langfuse score logging)*
- [x] **2.3: LangGraph persistence** *(StateGraph, checkpointers, thread_id, interrupt_before for Human-in-the-Loop approvals)*
- [x] **2.4: LangGraph reliability** *(Error handling, cycle breakers, maximum recursion limits)*
- [x] **2.5: Agentic concepts & security** *(Agent vs deterministic DAG, planning/decomposition, prompt injection, guardrails)*
- [x] **2.6: Multi-Agent Systems & CrewAI** *(Sequential vs hierarchical processes, agent handoffs, failure modes)*
- [x] **2.7: Model Context Protocol (MCP)** *(MCP architecture, client-server lifecycle, tools, resources, and prompts)*

---

### Wave 3: Ship and Operate (Must) — *IN PROGRESS*
- [ ] **3.1: Python & FastAPI hygiene** *(Structured logging, pytest testing suite, APIRouter modularization)*
- [ ] **3.2: Docker containerization** *(Multi-stage Dockerfile for FastAPI, compose networking, volume mounts)*
- [ ] **3.3: AWS Essentials** *(IAM least-privilege roles, Parameter Store/Secrets Manager, CloudWatch)*
- [ ] **3.4: CI/CD Pipelines** *(GitHub Actions automated test & Docker build/push)*
- [ ] **3.5: Capstone Deployment** *(Resume RAG + Agent deployed on AWS EC2 with Langfuse monitoring)*
- [ ] **3.1: Python & FastAPI hygiene** *(Structured logging, pytest testing suite, APIRouter modularization)*
- [ ] **3.2: Docker containerization** *(Multi-stage Dockerfile for FastAPI, compose networking, volume mounts)*
- [ ] **3.3: AWS Essentials** *(IAM least-privilege roles, Parameter Store/Secrets Manager, CloudWatch)*
- [ ] **3.4: CI/CD Pipelines** *(GitHub Actions automated test & Docker build/push)*
- [ ] **3.5: Capstone Deployment** *(Resume RAG + Agent deployed on AWS EC2 with Langfuse monitoring)*

---

### Wave 4: Interview Packaging (Must) — *QUEUED*
- [ ] **4.1: GenAI System Design** *(End-to-end whiteboard architecture of an enterprise RAG assistant)*
- [ ] **4.2: Mock Interview Drills** *(Resume walkthrough + 40 core GenAI technical questions)*

---

### Waves 5 & 6 (Should / Optional)
- [ ] **Wave 5: Model Ecosystem & Vector DBs** *(Ollama/Llama local models, Hugging Face Hub, Weaviate, Pinecone, Qwen/DeepSeek)*
- [ ] **Wave 6: Awareness & Enterprise Integrations** *(N8N, ServiceNow API, SharePoint integration, Postgres JSONB/SQS)*

---

## 📝 Codebase Mapping (`chat_app/src`)
| Topic | Relevant File(s) in Repo | Current Implementation |
| :--- | :--- | :--- |
| **Prompt Template & Roles** | [`src/prompts.py`](file:///c:/Users/DELL/Desktop/Programs/Python/chat_app/src/prompts.py) | ChatPromptTemplate with System/User roles and `{context}` / `{question}` variables |
| **Structured Output / Constraints** | [`src/models.py`](file:///c:/Users/DELL/Desktop/Programs/Python/chat_app/src/models.py), [`src/llm_config.py`](file:///c:/Users/DELL/Desktop/Programs/Python/chat_app/src/llm_config.py) | Pydantic `ResumeStructure` + `with_structured_output` |
| **RAG Pipeline & Execution** | [`src/rag_chain.py`](file:///c:/Users/DELL/Desktop/Programs/Python/chat_app/src/rag_chain.py) | LangChain LCEL pipeline (`retriever | prompt | structured_llm`) |
| **Vector Store & Ingestion** | [`src/chroma_config.py`](file:///c:/Users/DELL/Desktop/Programs/Python/chat_app/src/chroma_config.py) | PyPDFLoader + RecursiveCharacterTextSplitter + Chroma vector store |
| **FastAPI & Langfuse Tracing** | [`src/main.py`](file:///c:/Users/DELL/Desktop/Programs/Python/chat_app/src/main.py) | `/upload`, `/ask`, `/ask-stream` with Langfuse callback handler and tags |

