<div align="center">

# 🔬 ResearchPilot — Multi-Agent AI Research System

### _Four specialized AI agents collaborate to deliver polished research reports on any topic._

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o--mini-412991?logo=openai&logoColor=white)](https://openai.com/)
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

**ResearchPilot** is an AI-powered multi-agent research system that automates the entire research workflow — from searching the web, scraping relevant content, drafting a structured report, to providing critical feedback — all orchestrated through an elegant Streamlit web interface.

Instead of relying on a single LLM prompt, ResearchPilot breaks the research task into **four specialized agents**, each responsible for one phase of the pipeline. This modular approach produces higher-quality, more reliable, and better-structured research output compared to monolithic prompting.

### ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Intelligent Web Search** | Uses Tavily Search API to find the most recent and relevant information |
| 📄 **Smart Web Scraping** | Automatically identifies and scrapes the most relevant URLs for deeper content |
| ✍️ **Structured Report Writing** | Generates professional, well-structured research reports with introduction, findings, conclusions, and sources |
| 🧐 **AI Critic Review** | Provides an honest score (X/10), strengths, improvement areas, and a one-line verdict |
| 🎨 **ResearchPilot Dark UI** | Dark Streamlit workspace with a full-width report and critic review, plus collapsible agent details |
| ⬇️ **Export Reports** | Download the final research report as a Markdown file |
| ⚡ **Pipeline Tracking** | Follow the four research stages while a run is in progress |
| 🔎 **Research Transparency** | Open the agent overview and inspect the raw search and scraped page output |

---

## 🏗 Architecture & How It Works

ResearchPilot follows a **sequential multi-agent pipeline** pattern. Each agent completes its task before passing results downstream to the next agent. This mimics how a real research team operates:

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
- **Model**: OpenAI `gpt-4o-mini` via `langchain_openai`
- **Tool**: `web_search` — wraps the [Tavily Search API](https://tavily.com/)
- **Behavior**: Given a topic, it autonomously decides to invoke the search tool, processes the results, and returns structured search findings (titles, URLs, snippets) for up to 5 results.

### Agent 2: Reader Agent (`build_reader_agent`)

- **Type**: LangChain ReAct Agent with tool access
- **Model**: OpenAI `gpt-4o-mini` via `langchain_openai`
- **Tool**: `scrape_url` — uses `requests` + `BeautifulSoup` to scrape & clean web content
- **Behavior**: Receives the search results, identifies the most relevant URL, and scrapes its full content. HTML is cleaned by removing `<script>`, `<style>`, `<nav>`, and `<footer>` tags. Output is capped at 3,000 characters to stay within token limits.

### Chain 3: Writer Chain (`writer_chain`)

- **Type**: LangChain LCEL Chain (Prompt → LLM → Output Parser)
- **Model**: OpenAI `gpt-4o-mini` via `langchain_openai`
- **Behavior**: Takes the combined research data (search results + scraped content) and produces a detailed, professional research report following a fixed structure: Introduction → Key Findings (≥3 points) → Conclusion → Sources.

### Chain 4: Critic Chain (`critic_chain`)

- **Type**: LangChain LCEL Chain (Prompt → LLM → Output Parser)
- **Model**: OpenAI `gpt-4o-mini` via `langchain_openai`
- **Behavior**: Reviews the generated report and provides a structured evaluation: a numeric score out of 10, bullet-point strengths, bullet-point improvement areas, and a one-line verdict.

> **Note**: Agents 1 & 2 are LangChain _agents_ (they can autonomously decide when and how to use tools). Chains 3 & 4 are deterministic _chains_ (fixed prompt → LLM → parser pipeline with no tool usage).

---

## 📁 Project Structure

```
ResearchPilot_Multi_Agent_Research_System/
├── app.py              # Streamlit web UI — main entry point
├── agents.py           # Agent & chain definitions (search, reader, writer, critic)
├── tools.py            # LangChain tools (web_search, scrape_url)
├── pipeline.py         # CLI pipeline runner (alternative to the Streamlit UI)
├── requirements.txt    # Python dependencies
├── .env.example        # Safe template for local API keys
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### File-by-File Breakdown

| File | Lines | Purpose |
|---|---|---|
| **`app.py`** | Streamlit app | The ResearchPilot workspace with run progress, a full-width report and critic review, expandable agent summaries and raw search/scrape output, session history, and Markdown export. |
| **`agents.py`** | Agent and chain definitions | Defines the active OpenAI `gpt-4o-mini` model, two ReAct agents (`build_search_agent`, `build_reader_agent`), and two LCEL chains (`writer_chain`, `critic_chain`). |
| **`tools.py`** | ~38 | Implements two LangChain `@tool`-decorated functions: `web_search` (Tavily API wrapper returning top-5 results) and `scrape_url` (HTTP GET + BeautifulSoup HTML cleanup). |
| **`pipeline.py`** | ~76 | A standalone CLI script that runs the same 4-step pipeline without Streamlit, printing results to the terminal. Useful for testing and debugging. |

---

## 🛠 Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **LLM** | [OpenAI](https://openai.com/) (`gpt-4o-mini`) | Active model for the agents and report/review chains |
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
- **OpenAI API key** — from the [OpenAI API platform](https://platform.openai.com/api-keys)
- **Tavily API key** — [Get one here (free tier available)](https://tavily.com/)
- **Git** installed

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sourav23143/ResearchPilot_Multi_Agent_Research_System.git
   cd ResearchPilot_Multi_Agent_Research_System
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

### Configuration

Copy `.env.example` to `.env` in the project root, then replace the placeholders with your API keys:
   ```powershell
   # Windows PowerShell
   Copy-Item .env.example .env
   ```
   ```bash
   # macOS/Linux
   cp .env.example .env
   ```
   Edit `.env` so it contains:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

The active model is set in `agents.py`. Keep `.env` private; it is excluded by `.gitignore`. The committed `.env.example` contains placeholders only.

### Running the App

#### Option 1: Streamlit Web UI (Recommended)
```bash
streamlit run app.py
```
This opens the ResearchPilot dark-themed web interface at `http://localhost:8501`.

#### Option 2: Command-Line Interface
```bash
python pipeline.py
```
This runs the same pipeline in your terminal with rich-formatted output.

---

## 💡 Usage

1. **Launch** the Streamlit app with `streamlit run app.py`
2. **Enter** a research topic in the input field (e.g., _"Quantum computing breakthroughs in 2026"_)
3. **Click** **Start research**
4. **Follow** the four-stage pipeline as it searches, reads, writes, and reviews
5. **Read** the full-width final report and critic review
6. **Expand** **Agent overview and raw research** to see all four agents, their summaries, and raw search and scrape output
7. **Download** the report as a Markdown (`.md`) file

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
3. **`writer_chain`** — An LCEL chain: `ChatPromptTemplate → ChatOpenAI → StrOutputParser`
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

The Streamlit interface is responsible for:

- **Dark ResearchPilot styling** and the research question form
- **Pipeline progress** while the search, reader, writer, and critic stages run
- **Results display** with the full-width report first and the critic review below it
- **Expandable research details** with all four agent cards, summaries, raw search and scrape output, and source links
- **Session history** and Markdown report downloads

---

## 🔑 API Keys Setup

### OpenAI API Key

1. Open the [OpenAI API keys page](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Create and copy an API key
4. Add it to `OPENAI_API_KEY` in your local `.env` file

The active model is `gpt-4o-mini`, configured in `agents.py` through `langchain_openai.ChatOpenAI`.

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

- [ ] Enable and document alternative LLM providers
- [ ] Implement parallel agent execution for faster results
- [ ] Add a "Refine" step where the Writer rewrites based on Critic feedback
- [ ] Support PDF export in addition to Markdown
- [ ] Add conversation history / research session management
- [ ] Implement caching to avoid redundant API calls
- [ ] Add unit tests and integration tests

---

## 🙏 Acknowledgements


- **LangChain**: For the powerful agent and chain abstractions
- **OpenAI**: For the active `langchain_openai.ChatOpenAI` model integration
- **Tavily**: For the search API
- **Streamlit**: For making web app development effortless

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ using LangChain, OpenAI, Tavily, and Streamlit**

_If this project helped you, consider giving it a ⭐!_

</div>
