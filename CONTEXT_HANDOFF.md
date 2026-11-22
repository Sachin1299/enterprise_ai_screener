# 🚨 MASTER AI CONTEXT & TRANSITION HANDOFF
**Instructions for Antigravity / AI Assistant:** READ THIS FILE IMMEDIATELY ON STARTUP. This document restores 100% of the user's backstory, technical progress, constraints, timeline, and project roadmap.

---

## 👤 User Profile & Career Positioning
* **Name:** Sachin Chourasiya
* **Current Background:** Backend Java / Distributed Systems Developer (~3.4–3.6 years experience).
* **Target Role:** **AI Engineer / Applied GenAI Systems Engineer**
* **Interview Positioning Strategy:** 
  > *"Software Engineer with 3.5+ years of total experience: foundational years building scalable backend microservices, and the last 1.5+ years building enterprise GenAI pipelines, RAG systems, resilient agentic workflows, and LLM observability."*
  *(Do NOT claim 3.5 years pure GenAI—frame it as Backend Evolution into GenAI, which interviewers prize).*

---

## ⏳ Critical Timeline & Strategy
* **Wedding Date:** **December 12, 2026** (Major life milestone!).
* **Preparation Window:** ~6 focused days available right now before wedding commitments take over.
* **Job Application Window:** Starting immediately after wedding (~December 15–16, 2026).
* **Notice Period:** 90 days.
* **Goal for the 6 Days:** Build and package **ONE single, bulletproof, enterprise-grade AI Showcase Project** that anchors all interview discussions and demonstrates senior software engineering rigor.

---

## 💻 Hardware Constraints & Operating Rules
* **User Machine:** 4 GB RAM, Intel Core i3, 256 GB SSD (Windows 11).
* **Strict Rule:** **DO NOT run heavy local LLMs (Ollama 8B/7B) directly on the host machine** (Windows consumes ~2.5GB; running 5GB models locally will thrash swap and freeze the laptop).
* **Execution Strategy:**
  1. Use **Cloud APIs** (Google Gemini `gemini-3.5-flash-lite`, Hugging Face Serverless API) for zero local RAM load.
  2. Use **Google Colab (Free 12GB RAM + T4 GPU in browser)** for any hands-on GPU/Ollama experiments after mid-December.
  3. Master the interview theory for on-premise deployments: **vLLM / Ollama OpenAI-compatible endpoints**, VRAM contention math ($8\text{B} \times 2 = 16\text{GB}$ FP16 vs $4.5\text{GB}$ INT4 quantized), and dynamic model offloading (`keep_alive` eviction).

---

## 📊 Roadmap & Learning Tracker Progress (from `AiEngineer_Plan.xlsx`)
* **Total Roadmap Topics:** 225
* **Mastered / Completed:** **163 / 225 topics (~72%)**

### Completed Waves:
* [x] **Wave 1: GenAI Fundamentals (16/16 topics)**
  * Next-token inference, tokens vs words, context windows, temperature/sampling, model tiers.
  * Production prompt engineering (delimiters, XML tags, negative constraints, few-shot vs zero-shot).
  * Resilient LLM calls (HTTP 429 rate limits, exponential backoff with jitter, fail-fast auth circuit breakers).
* [x] **Wave 2: RAG & Agent Depth (18/18 topics)**
  * Grounded generation & page-level citations.
  * Hybrid Search (BM25 keyword search + Dense Vector Embeddings via RRF).
  * Cross-Encoder Reranking (why bi-encoders are not enough, solving context bloat).
  * RAG Triad Evaluation (Faithfulness, Answer Relevancy, Context Precision via LLM-as-a-Judge, Langfuse evals).
  * LangGraph Persistence & Memory (StateGraph, checkpointers, `thread_id` database lookups).
  * Human-in-the-Loop (HITL) approval (`interrupt_before`, resuming via `invoke(None)`, state editing).
  * Agent Reliability (recursion limits against runaway loops, tool exception recovery into state).
  * Agent Security (Bounded autonomy, least privilege tools, indirect prompt injection defense).
  * Multi-Agent Systems & CrewAI (Sequential vs Hierarchical supervisor processes, when to avoid multi-agent).
  * Model Context Protocol (MCP) (Client/Server JSON-RPC over HTTPS/SSE, Tools vs Resources vs Prompts).

### Active Wave:
* [ ] **Wave 3: Ship & Operate (The Showcase Capstone Build)**
  * 3.1: Python & FastAPI hygiene (Modular APIRouters, structured logging, pytest integration tests).
  * 3.2: Docker containerization (Multi-stage Dockerfile for FastAPI + Chroma, docker-compose).
  * 3.3: AWS essentials (IAM roles, secrets management, CloudWatch/APM).
  * 3.4: CI/CD automation (GitHub Actions pipeline for linting, test, and container build).
  * 3.5: Capstone Showcase polish.

---

## 🏗️ Showcase Project Blueprint: `Enterprise Candidate Intelligence & Screening Agent`
**Directory:** `C:\Users\DELL\Desktop\Programs\Python\enterprise_ai_screener`

### Architectural Pillars:
1. **Core Ingestion & RAG:**
   * PDF ingestion with metadata tagging.
   * ChromaDB vector store + BM25 hybrid retrieval + Cross-encoder reranker.
   * Strict page citations (`[Page 1]`) and anti-hallucination guardrails.
2. **LangGraph Agentic Screening Engine:**
   * ReAct state machine comparing candidate profile against Job Descriptions.
   * Safe read-only tools vs. Mutating side-effect tools (send interview invite / reject).
   * Human-in-the-Loop (HITL) pause before any communication triggers.
   * Recursion limit circuit breakers.
3. **Enterprise Resilience & Observability:**
   * Resilient retry policies with exponential backoff and jitter on all LLM calls.
   * FastAPI global exception handlers (429 RateLimit, 503 Auth/Circuit Breaker, 502 Upstream).
   * End-to-end tracing in Langfuse (tracking latency, token usage, cost, and RAG Triad scores).
4. **Senior Software Engineering Standards:**
   * Clean separation: `routers/`, `services/`, `core/`, `models/`.
   * Automated tests using `pytest` and `httpx`.
   * Single-command `docker-compose up` setup.

