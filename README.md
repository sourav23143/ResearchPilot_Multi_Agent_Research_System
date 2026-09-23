<div align="center">

# 🔬 ResearchWorks — Multi-Agent AI Research System

### _Four specialized AI agents collaborate to deliver polished research reports on any topic._

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Mistral](https://img.shields.io/badge/Mistral-MistralAI-4611A0?logo=mistral&logoColor=white)](https://mistral.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

<img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="status" />

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture & How It Works](#-architecture--how-it-works)
- [Agent Pipeline Deep Dive](#-agent-pipeline-deep-dive)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the App](#running-the-app)
- [Usage](#-usage)
- [Code Walkthrough](#-code-walkthrough)
- [API Keys Setup](#-api-keys-setup)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [Acknowledgements](#-acknowledgements)
- [License](#-license)

---

## 🌟 Overview

**ResearchWorks** is an AI-powered multi-agent research system that automates the entire research workflow — from searching the web, scraping relevant content, drafting a structured report, to providing critical feedback — all orchestrated through an elegant Streamlit web interface.

Instead of relying on a single LLM prompt, ResearchWorks breaks the research task into **four specialized agents**, each responsible for one phase of the pipeline. This modular approach produces higher-quality, more reliable, and better-structured research output compared to monolithic prompting.

### ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Intelligent Web Search** | Uses Tavily Search API to find the most recent and relevant information |
| 📄 **Smart Web Scraping** | Automatically identifies and scrapes the most relevant URLs for deeper content |
| ✍️ **Structured Report Writing** | Generates professional, well-structured research reports with introduction, findings, conclusions, and sources |
| 🧐 **AI Critic Review** | Provides an honest score (X/10), strengths, improvement areas, and a one-line verdict |
| 🎨 **Premium Dark UI** | Beautifully designed dark-mode interface with glassmorphism, gradients, and micro-animations |
| ⬇️ **Export Reports** | Download the final research report as a Markdown file |
| ⚡ **Real-time Pipeline Tracking** | Visual step-by-step progress indicators showing which agent is currently active |

---

## 🏗 Architecture & How It Works

ResearchWorks follows a **sequential multi-agent pipeline** pattern. Each agent completes its task before passing results downstream to the next agent. This mimics how a real research team operates:

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│                   "Research Topic"                               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1 │ 🔍 SEARCH AGENT                                      │
│         │ • Uses Tavily Search API                              │
│         │ • Finds 5 recent, reliable sources                    │
│         │ • Returns titles, URLs, and content snippets          │
└─────────────────────┬───────────────────────────────────────────┘
                      │ search results
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2 │ 📄 READER AGENT                                      │
│         │ • Receives search results                             │
│         │ • Picks the most relevant URL                         │
│         │ • Scrapes full page content (up to 3000 chars)        │
│         │ • Cleans HTML (strips scripts, styles, nav, footer)   │
└─────────────────────┬───────────────────────────────────────────┘
                      │ scraped content
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3 │ ✍️ WRITER CHAIN                                      │
│         │ • Combines search results + scraped content           │
│         │ • Drafts a structured report:                         │
│         │   - Introduction                                      │
│         │   - Key Findings (minimum 3 points)                   │
│         │   - Conclusion                                        │
│         │   - Sources (all URLs from research)                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │ full report
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4 │ 🧐 CRITIC CHAIN                                      │
│         │ • Reviews the report strictly                         │
│         │ • Provides:                                           │
│         │   - Score (X/10)                                      │
│         │   - Strengths                                         │
│         │   - Areas to Improve                                  │
│         │   - One-line Verdict                                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    📊 RESULTS DISPLAY                            │
│  • Raw search results (expandable)                              │
│  • Raw scraped content (expandable)                             │
│  • Final formatted research report                              │
│  • Critic feedback with score                                   │
│  • Download report as .md file                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why Multi-Agent?

| Approach | Drawback |
|---|---|
| Single prompt | Prone to hallucination, no fact-checking, shallow results |
| **Multi-agent (this project)** | ✅ Each agent specializes in one task → higher quality per step |

By decomposing the task, each agent can be prompted with laser-focused instructions, resulting in more accurate search, deeper content extraction, better-structured writing, and honest critique.

---

## 🔎 Agent Pipeline Deep Dive

### Agent 1: Search Agent (`build_search_agent`)

- **Type**: LangChain ReAct Agent with tool access
- **Model**: Mistral AI via `langchain_mistralai`
- **Tool**: `web_search` — wraps the [Tavily Search API](https://tavily.com/)
- **Behavior**: Given a topic, it autonomously decides to invoke the search tool, processes the results, and returns structured search findings (titles, URLs, snippets) for up to 5 results.

### Agent 2: Reader Agent (`build_reader_agent`)

- **Type**: LangChain ReAct Agent with tool access
- **Model**: Mistral AI via `langchain_mistralai`
- **Tool**: `scrape_url` — uses `requests` + `BeautifulSoup` to scrape & clean web content
- **Behavior**: Receives the search results, identifies the most relevant URL, and scrapes its full content. HTML is cleaned by removing `<script>`, `<style>`, `<nav>`, and `<footer>` tags. Output is capped at 3,000 characters to stay within token limits.

### Chain 3: Writer Chain (`writer_chain`)

- **Type**: LangChain LCEL Chain (Prompt → LLM → Output Parser)
- **Model**: Mistral AI via `langchain_mistralai`
- **Behavior**: Takes the combined research data (search results + scraped content) and produces a detailed, professional research report following a fixed structure: Introduction → Key Findings (≥3 points) → Conclusion → Sources.

### Chain 4: Critic Chain (`critic_chain`)

- **Type**: LangChain LCEL Chain (Prompt → LLM → Output Parser)
- **Model**: Mistral AI via `langchain_mistralai`
- **Behavior**: Reviews the generated report and provides a structured evaluation: a numeric score out of 10, bullet-point strengths, bullet-point improvement areas, and a one-line verdict.

> **Note**: Agents 1 & 2 are LangChain _agents_ (they can autonomously decide when and how to use tools). Chains 3 & 4 are deterministic _chains_ (fixed prompt → LLM → parser pipeline with no tool usage).

---

## 📁 Project Structure

```
Multi_Agent_Research_System/
├── app.py              # Streamlit web UI — main entry point
├── agents.py           # Agent & chain definitions (search, reader, writer, critic)
├── tools.py            # LangChain tools (web_search, scrape_url)
├── pipeline.py         # CLI pipeline runner (alternative to the Streamlit UI)
├── requirements.txt    # Python dependencies
├── .env.example        # Template for required environment variables
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### File-by-File Breakdown

| File | Lines | Purpose |
|---|---|---|
| **`app.py`** | ~508 | The Streamlit web application. Contains all custom CSS styling (dark theme with glassmorphism), UI layout with two columns (input + pipeline tracker), pipeline execution logic with spinners, results display with expanders, and a download button for the final report. |
| **`agents.py`** | ~79 | Defines the LLM (`gpt-4o-mini`), two ReAct agents (`build_search_agent`, `build_reader_agent`), and two LCEL chains (`writer_chain`, `critic_chain`) with their respective prompt templates. |
| **`tools.py`** | ~38 | Implements two LangChain `@tool`-decorated functions: `web_search` (Tavily API wrapper returning top-5 results) and `scrape_url` (HTTP GET + BeautifulSoup HTML cleanup). |
| **`pipeline.py`** | ~76 | A standalone CLI script that runs the same 4-step pipeline without Streamlit, printing results to the terminal. Useful for testing and debugging. |

---

## 🛠 Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **LLM** | [Mistral AI](https://mistral.ai/) | Powers all agents and chains |
| **Agent Framework** | [LangChain](https://www.langchain.com/) | Agent orchestration, prompt templates, LCEL chains |
| **Web Search** | [Tavily API](https://tavily.com/) | Fast, reliable web search optimized for LLMs |
| **Web Scraping** | [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/) + [Requests](https://requests.readthedocs.io/) | HTML parsing and content extraction |
| **Web UI** | [Streamlit](https://streamlit.io/) | Interactive web application framework |
| **Env Management** | [python-dotenv](https://pypi.org/project/python-dotenv/) | Secure environment variable loading |
| **Rich Logging** | [Rich](https://rich.readthedocs.io/) | Beautiful terminal output for CLI mode |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system
- **Mistral API key** — from your Mistral provider dashboard
- **Tavily API key** — [Get one here (free tier available)](https://tavily.com/)
- **Git** installed

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sourav23143/Multi_Agent_Research_System.git
   cd Multi_Agent_Research_System
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: You also need Streamlit. If not in requirements.txt, install separately:
   > ```bash
   > pip install streamlit
   > ```

### Configuration

1. **Copy the environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and fill in your API keys:
   ```env
   MISTRAL_API_KEY=mr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Running the App

#### Option 1: Streamlit Web UI (Recommended)
```bash
streamlit run app.py
```
This opens a beautiful dark-themed web interface at `http://localhost:8501`.

#### Option 2: Command-Line Interface
```bash
python pipeline.py
```
This runs the same pipeline in your terminal with rich-formatted output.

---

## 💡 Usage

1. **Launch** the Streamlit app with `streamlit run app.py`
2. **Enter** a research topic in the input field (e.g., _"Quantum computing breakthroughs in 2026"_)
3. **Click** the "⚡ Run Research Pipeline" button
4. **Watch** the pipeline progress through all four stages in real-time
5. **Review** the results:
   - Expand raw search results and scraped content for transparency
   - Read the full research report
   - Check the critic's score and feedback
6. **Download** the report as a Markdown (`.md`) file

### Example Topics to Try

- `LLM agents 2026`
- `CRISPR gene editing`
- `Fusion energy progress`
- `Climate change solutions 2026`
- `Mars colonization latest developments`

---

## 🔍 Code Walkthrough

### `tools.py` — The Foundation

This module defines the two core tools that agents can invoke:

```python
@tool
def web_search(query: str) -> str:
    """Uses Tavily API to search the web. Returns top-5 results
    with titles, URLs, and 300-char content snippets."""

@tool
def scrape_url(url: str) -> str:
    """Fetches a URL, parses HTML with BeautifulSoup, removes
    non-content elements, returns clean text (max 3000 chars)."""
```

- `web_search` wraps the Tavily client and formats results into a readable string
- `scrape_url` uses `requests.get()` with a custom User-Agent header and an 8-second timeout for robustness

### `agents.py` — The Brain

Defines four AI components:

1. **`build_search_agent()`** — Creates a ReAct agent with the `web_search` tool
2. **`build_reader_agent()`** — Creates a ReAct agent with the `scrape_url` tool
3. **`writer_chain`** — An LCEL chain: `ChatPromptTemplate → MistralAI → StrOutputParser`
4. **`critic_chain`** — An LCEL chain with a structured evaluation prompt

The agents use `langchain.agents.create_agent()` which creates a ReAct-style agent that can reason about when and how to use its tools.

### `pipeline.py` — The Orchestrator (CLI)

A simple sequential executor:

```python
def run_research_pipeline(topic: str) -> dict:
    # Step 1: Search → Step 2: Read → Step 3: Write → Step 4: Critique
    # Each step's output feeds into the next
    return state  # Contains all intermediate + final results
```

### `app.py` — The Interface

The largest file (~508 lines), responsible for:

- **Custom CSS** (~290 lines): Dark theme with orange accents, glassmorphism cards, custom-styled inputs/buttons, step progress indicators, and result panels
- **Step Card Component** (`step_card()`): A reusable function that renders pipeline step indicators with waiting/running/done states
- **Pipeline Execution**: Runs the 4 agents sequentially using Streamlit spinners, with `st.session_state` tracking progress
- **Results Display**: Expandable raw outputs, the final formatted report (rendered as native Markdown), the critic feedback panel, and a download button

---

## 🔑 API Keys Setup

### Mistral AI API Key

1. Go to your Mistral AI provider dashboard
2. Sign in or create an account
3. Create a new API key
4. Copy the key
5. Add it to your `.env` file

> **Note**: This project uses `langchain_mistralai.ChatMistralAI`.

### Tavily API Key

1. Go to [Tavily](https://tavily.com/)
2. Sign up for a free account
3. Navigate to your dashboard to find your API key
4. Copy the key (starts with `tvly-`)
5. Add it to your `.env` file

> **Free Tier**: Tavily offers 1,000 free API calls per month — more than enough for testing and personal use.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes:
   ```bash
   git commit -m "Add: your feature description"
   ```
4. **Push** to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open** a Pull Request

### Ideas for Contribution

- [ ] Add support for more LLM providers (Anthropic, Google Gemini, Ollama)
- [ ] Implement parallel agent execution for faster results
- [ ] Add a "Refine" step where the Writer rewrites based on Critic feedback
- [ ] Support PDF export in addition to Markdown
- [ ] Add conversation history / research session management
- [ ] Implement caching to avoid redundant API calls
- [ ] Add unit tests and integration tests

---

## 🙏 Acknowledgements


- **LangChain**: For the powerful agent and chain abstractions
- **Mistral AI**: For `langchain_mistralai.ChatMistralAI`
- **Tavily**: For the search API
- **Streamlit**: For making web app development effortless

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ using LangChain, Mistral AI, and Streamlit**

_If this project helped you, consider giving it a ⭐!_

</div>
