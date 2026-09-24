import html
import re
from datetime import datetime

import streamlit as st

from agents import build_reader_agent, build_search_agent, critic_chain, writer_chain


st.set_page_config(
    page_title="ResearchPilot | AI Research Workspace",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #eaf0f8;
        --muted: #91a0b5;
        --line: rgba(159, 183, 215, .14);
        --panel: rgba(19, 29, 47, .76);
        --blue: #66b8ff;
        --mint: #85e0c1;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }
    .stApp {
        color: var(--ink);
        background:
            radial-gradient(ellipse 70% 40% at 85% -10%, rgba(48, 124, 195, .20), transparent 68%),
            radial-gradient(ellipse 48% 32% at 0% 30%, rgba(59, 203, 171, .09), transparent 70%),
            #0a101b;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101a2a 0%, #0c1421 100%);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.3rem; }
    .block-container { max-width: 1500px; padding: 2.2rem 2.6rem 4rem; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.025em; }
    h1 { font-size: clamp(2.4rem, 5vw, 4rem) !important; line-height: 1.04 !important; }
    h2 { font-size: 1.65rem !important; }
    p, li { color: #c3cede; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 18px;
    }
    [data-testid="stTextInput"] input {
        background: rgba(7, 13, 23, .74);
        color: var(--ink);
        border: 1px solid rgba(159, 183, 215, .22);
        border-radius: 11px;
        min-height: 3rem;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--blue);
        box-shadow: 0 0 0 1px var(--blue);
    }
    [data-testid="stTextInput"] label, [data-testid="stTextArea"] label {
        color: #c3cede;
        font-weight: 600;
    }
    .stButton > button, [data-testid="stFormSubmitButton"] button {
        min-height: 2.7rem;
        border-radius: 10px;
        border: 1px solid rgba(102, 184, 255, .4);
        color: #06111d;
        background: linear-gradient(135deg, #87d0ff, #66b8ff 58%, #83e0c2);
        font-weight: 700;
        transition: transform .15s ease, filter .15s ease;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        filter: brightness(1.06);
        border-color: var(--blue);
    }
    [data-testid="stBaseButton-secondary"] {
        color: #c6d5e9 !important;
        background: rgba(255,255,255,.035) !important;
        border-color: var(--line) !important;
    }
    [data-testid="stTabs"] button {
        color: #aebbd0;
        font-weight: 600;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--blue);
        border-bottom-color: var(--blue);
    }
    [data-testid="stMetric"] {
        background: rgba(17, 29, 47, .72);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: .9rem 1rem;
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); }
    [data-testid="stStatusWidget"] {
        background: rgba(19, 29, 47, .72);
        border: 1px solid var(--line);
        border-radius: 14px;
    }
    [data-testid="stDownloadButton"] button {
        border: 1px solid rgba(133, 224, 193, .42);
        color: #d9fff1;
        background: rgba(67, 164, 135, .12);
        border-radius: 10px;
    }
    a { color: var(--blue) !important; }
    hr { border-color: var(--line); }
    .brand-lockup { display:flex; align-items:center; gap:.75rem; margin:0 0 1rem; }
    .brand-mark {
        width:2.45rem; height:2.45rem; display:grid; place-items:center;
        border-radius:12px; color:#071421; font-size:1.25rem; font-weight:800;
        background:linear-gradient(145deg,#9bdcff,#62b6ff 55%,#83e0c2);
        box-shadow:0 8px 28px rgba(80,174,237,.2);
    }
    .brand-name { font:700 1.08rem 'Space Grotesk',sans-serif; color:#f0f5fc; }
    .brand-caption { color:#8494ab; font-size:.72rem; margin-top:.1rem; }
    .eyebrow {
        color:var(--mint); font:600 .72rem 'Space Grotesk',sans-serif;
        letter-spacing:.17em; text-transform:uppercase; margin-bottom:.65rem;
    }
    .hero-copy { color:#aab8cc; font-size:1.06rem; line-height:1.65; max-width:720px; }
    .hero-accent { color:#91d5ff; }
    .soft-label { color:#8292a8; font-size:.78rem; letter-spacing:.11em; text-transform:uppercase; font-weight:700; }
    .sidebar-step { color:#a9b8cd; padding:.38rem 0; font-size:.9rem; }
    .sidebar-step span { color:var(--mint); font-weight:700; margin-right:.5rem; }
    .result-heading { color:#ecf4ff; font:700 1.08rem 'Space Grotesk',sans-serif; margin-bottom:.5rem; }
    .agent-card {
        min-height: 142px; padding: 1rem 1rem .9rem; border-radius: 15px;
        background: rgba(19, 29, 47, .82); border: 1px solid var(--line);
        border-top: 2px solid rgba(159,183,215,.18);
    }
    .agent-card.running { border-top-color: #66b8ff; box-shadow: 0 0 25px rgba(74,156,220,.08); }
    .agent-card.complete { border-top-color: #85e0c1; }
    .agent-card.failed { border-top-color: #ff8b8b; }
    .agent-number { color:#8092aa; font:600 .7rem 'Space Grotesk',sans-serif; letter-spacing:.12em; }
    .agent-title { color:#edf4fc; font:700 1rem 'Space Grotesk',sans-serif; margin:.45rem 0 .28rem; }
    .agent-state { color:#91a0b5; font-size:.72rem; text-transform:uppercase; letter-spacing:.1em; }
    .agent-state.running { color:#83ceff; }
    .agent-state.complete { color:#85e0c1; }
    .agent-state.failed { color:#ff9a9a; }
    .agent-preview { color:#9aabc1; font-size:.79rem; line-height:1.45; margin-top:.65rem; }
    .raw-caption { color:#8192a8; font-size:.82rem; }
    .empty-state {
        padding:2rem; border:1px dashed rgba(159,183,215,.22); border-radius:16px;
        text-align:center; color:#8e9db2; background:rgba(17,29,47,.38);
    }
    .run-meta { color:#8494ab; font-size:.82rem; }
    @media (max-width: 760px) {
        .block-container { padding:1.2rem 1rem 3rem; }
        [data-testid="stSidebar"] { min-width: 0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def content_to_text(content):
    """Convert LangChain text blocks into plain text without metadata/signatures."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        chunks = []
        for block in content:
            if isinstance(block, str):
                chunks.append(block)
            elif isinstance(block, dict) and block.get("type") in {"text", "output_text"}:
                text = block.get("text")
                if isinstance(text, str):
                    chunks.append(text)
        return "\n".join(chunk for chunk in chunks if chunk.strip())
    return str(content) if content is not None else ""


def find_urls(*texts):
    urls = []
    for text in texts:
        for url in re.findall(r"https?://[^\s)\]>]+", text or ""):
            cleaned = url.rstrip(".,;:'\"}")
            if cleaned and cleaned not in urls:
                urls.append(cleaned)
    return urls


def friendly_error(error, stage):
    message = str(error)
    lowered = message.lower()
    if "429" in message or "resource_exhausted" in lowered or "quota" in lowered:
        return f"{stage} paused because the model or search service reached its usage limit. Check the provider quota, then retry when it resets."
    if "503" in message or "unavailable" in lowered:
        return f"{stage} paused because the AI provider is temporarily busy. Wait a little and try again."
    if "401" in message or "403" in message or "api key" in lowered or "authentication" in lowered:
        return f"{stage} could not connect. Check the API key in your .env file."
    return f"{stage} stopped because one of its services returned an error. You can retry after checking the details below."


def tool_output(agent_result, expected_tool):
    """Return the raw content from a named tool message in an agent result."""
    messages = agent_result.get("messages", []) if isinstance(agent_result, dict) else []
    outputs = []
    for message in messages:
        if isinstance(message, dict):
            message_type = message.get("type") or message.get("role")
            name = message.get("name")
            content = message.get("content")
        else:
            message_type = getattr(message, "type", None)
            name = getattr(message, "name", None)
            content = getattr(message, "content", None)
        if message_type == "tool" and name == expected_tool:
            text = content_to_text(content)
            if text.strip():
                outputs.append(text)
    return "\n\n".join(outputs)


AGENT_INFO = [
    ("search", "01", "Search Agent", "Finds relevant web sources"),
    ("reader", "02", "Reader Agent", "Scrapes a useful source"),
    ("writer", "03", "Writer Agent", "Drafts the research report"),
    ("critic", "04", "Critic Agent", "Reviews the report"),
]


def render_agent_cards(container, states, results):
    previews = {
        "search": content_to_text(results.get("search_summary", "")),
        "reader": content_to_text(results.get("reader_summary", "")),
        "writer": content_to_text(results.get("writer", "")),
        "critic": content_to_text(results.get("critic", "")),
    }
    labels = {
        "waiting": "Waiting",
        "running": "Working now",
        "complete": "Complete",
        "failed": "Needs attention",
    }
    with container.container():
        columns = st.columns(4)
        for column, (key, number, title, description) in zip(columns, AGENT_INFO):
            state = states.get(key, "waiting")
            preview = re.sub(r"\s+", " ", previews.get(key, "")).strip()
            if len(preview) > 120:
                preview = preview[:117].rstrip() + "…"
            summary = html.escape(preview or description)
            css_state = state if state in {"running", "complete", "failed"} else ""
            with column:
                st.markdown(
                    f"<div class='agent-card {css_state}'>"
                    f"<div class='agent-number'>STAGE {number}</div>"
                    f"<div class='agent-title'>{title}</div>"
                    f"<div class='agent-state {css_state}'>{labels.get(state, 'Waiting')}</div>"
                    f"<div class='agent-preview'>{summary}</div></div>",
                    unsafe_allow_html=True,
                )


for key, default in {
    "topic_input": "",
    "active_topic": "",
    "results": {},
    "history": [],
    "run_error": None,
    "run_error_details": None,
    "agent_states": {"search": "waiting", "reader": "waiting", "writer": "waiting", "critic": "waiting"},
}.items():
    st.session_state.setdefault(key, default)


with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
            <div class="brand-mark">R</div>
            <div><div class="brand-name">ResearchPilot</div>
            <div class="brand-caption">AI research workspace</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Your research, in four steps")
    st.markdown(
        """
        <div class="sidebar-step"><span>01</span> Search the web</div>
        <div class="sidebar-step"><span>02</span> Read a useful source</div>
        <div class="sidebar-step"><span>03</span> Draft a clear report</div>
        <div class="sidebar-step"><span>04</span> Review and improve</div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    if st.session_state.history:
        st.markdown("#### Recent research")
        for index, item in enumerate(st.session_state.history[:5]):
            label = item["topic"]
            if len(label) > 34:
                label = label[:31] + "..."
            if st.button(label, key=f"history_{index}", use_container_width=True):
                st.session_state.topic_input = item["topic"]
                st.session_state.active_topic = item["topic"]
                st.session_state.results = item["results"]
                st.session_state.agent_states = {
                    "search": "complete", "reader": "complete", "writer": "complete", "critic": "complete"
                }
                st.session_state.run_error = None
                st.session_state.run_error_details = None
                st.rerun()


st.markdown('<div class="eyebrow">A clearer path from question to insight</div>', unsafe_allow_html=True)
st.title("ResearchPilot")
st.markdown(
    '<div class="hero-copy">Turn a research question into a <span class="hero-accent">source-backed report</span>. '
    'ResearchPilot searches, reads, writes, and reviews in one guided workflow.</div>',
    unsafe_allow_html=True,
)
st.write("")

st.markdown('<div class="soft-label">Try a starting point</div>', unsafe_allow_html=True)
examples = [
    "How is AI changing drug discovery?",
    "India's renewable energy outlook",
    "Impact of remote work on productivity",
]
example_columns = st.columns(3)
for index, (column, example) in enumerate(zip(example_columns, examples)):
    with column:
        if st.button(example, key=f"example_{index}", use_container_width=True):
            st.session_state.topic_input = example
            st.rerun()

with st.container(border=True):
    with st.form("research_form"):
        topic = st.text_input(
            "Research question",
            placeholder="e.g. How could new battery technology reshape electric transport?",
            key="topic_input",
        )
        left, right = st.columns([4, 1])
        with left:
            st.caption("ResearchPilot will search the web, read a relevant page, draft a report, and critique it.")
        with right:
            submitted = st.form_submit_button("Start research  →", use_container_width=True)

agent_display = st.empty()

if submitted:
    if not topic.strip():
        st.warning("Enter a research question to get started.")
    else:
        st.session_state.active_topic = topic.strip()
        st.session_state.results = {}
        st.session_state.run_error = None
        st.session_state.run_error_details = None
        st.session_state.agent_states = {
            "search": "waiting", "reader": "waiting", "writer": "waiting", "critic": "waiting"
        }
        render_agent_cards(agent_display, st.session_state.agent_states, {})
        results = {}
        stage = "Search"
        progress = st.progress(0, text="Preparing your research workspace…")
        try:
            with st.status("01 · Searching the web", expanded=False) as status:
                st.session_state.agent_states["search"] = "running"
                render_agent_cards(agent_display, st.session_state.agent_states, results)
                search_agent = build_search_agent()
                search_result = search_agent.invoke({
                    "messages": [(
                        "user",
                        f"Find recent, reliable, detailed information about: {st.session_state.active_topic}",
                    )]
                })
                results["search_raw"] = tool_output(search_result, "web_search")
                results["search_summary"] = content_to_text(search_result["messages"][-1].content)
                if not results["search_raw"] and not results["search_summary"].strip():
                    raise RuntimeError("The search agent returned no readable text.")
                st.session_state.agent_states["search"] = "complete"
                st.session_state.results = dict(results)
                render_agent_cards(agent_display, st.session_state.agent_states, results)
                status.update(label="01 · Web research gathered", state="complete")
            progress.progress(25, text="Web research gathered")

            stage = "Reader"
            with st.status("02 · Reading a relevant source", expanded=False) as status:
                st.session_state.agent_states["reader"] = "running"
                render_agent_cards(agent_display, st.session_state.agent_states, results)
                reader_agent = build_reader_agent()
                search_context = results.get("search_raw") or results.get("search_summary", "")
                reader_result = reader_agent.invoke({
                    "messages": [(
                        "user",
                        f"For the topic '{st.session_state.active_topic}', choose the most relevant URL "
                        f"from these results and scrape it for useful detail.\n\n"
                        f"Search results:\n{search_context[:5000]}",
                    )]
                })
                results["scraped_raw"] = tool_output(reader_result, "scrape_url")
                results["reader_summary"] = content_to_text(reader_result["messages"][-1].content)
                st.session_state.agent_states["reader"] = "complete"
                st.session_state.results = dict(results)
                render_agent_cards(agent_display, st.session_state.agent_states, results)
                status.update(label="02 · Source read", state="complete")
            progress.progress(50, text="Source read")

            stage = "Writer"
            with st.status("03 · Drafting your report", expanded=False) as status:
                st.session_state.agent_states["writer"] = "running"
                render_agent_cards(agent_display, st.session_state.agent_states, results)
                research = (
                    f"RAW SEARCH TOOL RESULTS:\n{results.get('search_raw', '')[:5000]}\n\n"
                    f"SEARCH AGENT SUMMARY:\n{results.get('search_summary', '')[:2500]}\n\n"
                    f"RAW SCRAPED PAGE TEXT:\n{results.get('scraped_raw', '')[:4000]}\n\n"
                    f"READER AGENT SUMMARY:\n{results.get('reader_summary', '')[:2500]}"
                )
                results["writer"] = writer_chain.invoke({
                    "topic": st.session_state.active_topic,
                    "research": research,
                })
                st.session_state.agent_states["writer"] = "complete"
                st.session_state.results = dict(results)
                render_agent_cards(agent_display, st.session_state.agent_states, results)
                status.update(label="03 · Report drafted", state="complete")
            progress.progress(75, text="Report drafted")

            stage = "Critic"
            with st.status("04 · Reviewing the report", expanded=False) as status:
                st.session_state.agent_states["critic"] = "running"
                render_agent_cards(agent_display, st.session_state.agent_states, results)
                results["critic"] = critic_chain.invoke({"report": results["writer"]})
                st.session_state.agent_states["critic"] = "complete"
                st.session_state.results = dict(results)
                render_agent_cards(agent_display, st.session_state.agent_states, results)
                status.update(label="04 · Review complete", state="complete")
            progress.progress(100, text="Research complete")

            history_item = {
                "topic": st.session_state.active_topic,
                "results": dict(results),
                "created_at": datetime.now().strftime("%b %d, %Y · %H:%M"),
            }
            st.session_state.history = [
                history_item,
                *[item for item in st.session_state.history if item["topic"] != history_item["topic"]],
            ][:5]
            st.success("Your research report is ready.")
            agent_display.empty()
        except Exception as error:
            failed_key = {"Search": "search", "Reader": "reader", "Writer": "writer", "Critic": "critic"}.get(stage)
            if failed_key:
                st.session_state.agent_states[failed_key] = "failed"
            render_agent_cards(agent_display, st.session_state.agent_states, results)
            st.session_state.results = dict(results)
            st.session_state.run_error = friendly_error(error, stage)
            st.session_state.run_error_details = str(error)


if st.session_state.run_error:
    st.error(st.session_state.run_error)
    with st.expander("Technical details"):
        st.code(st.session_state.run_error_details or "No additional details available.")


results = st.session_state.results
if results:
    st.divider()
    st.caption(f"Research question · {st.session_state.active_topic}")

    search_raw = content_to_text(results.get("search_raw", ""))
    search_summary = content_to_text(results.get("search_summary", results.get("search", "")))
    scraped_raw = content_to_text(results.get("scraped_raw", ""))
    reader_summary = content_to_text(results.get("reader_summary", results.get("reader", "")))
    report_text = content_to_text(results.get("writer", ""))
    critic_text = content_to_text(results.get("critic", ""))
    urls = find_urls(search_raw, search_summary, scraped_raw, reader_summary, report_text)
    score_match = re.search(r"score\s*:\s*(\d+(?:\.\d+)?)\s*/\s*10", critic_text, re.IGNORECASE)

    st.markdown("## Final Research Report")
    if report_text:
        st.markdown(report_text)
        st.download_button(
            "Download report (.md)",
            data=f"# ResearchPilot — {st.session_state.active_topic}\n\n{report_text}\n",
            file_name=f"researchpilot_{re.sub(r'[^a-z0-9]+', '-', st.session_state.active_topic.lower()).strip('-')[:48] or 'report'}.md",
            mime="text/markdown",
            key="download_report",
        )
    else:
        st.info("The report is not available yet. Check the pipeline message above.")

    st.divider()
    st.markdown("## Critic Review")
    if critic_text:
        st.markdown(critic_text)
    else:
        st.info("The critic review is not available yet.")

    with st.expander("Agent overview and raw research", expanded=False):
        metrics = st.columns(4)
        metrics[0].metric("Sources found", len(urls))
        metrics[1].metric("Search output", f"{len(search_raw):,} chars")
        metrics[2].metric("Scraped text", f"{len(scraped_raw):,} chars")
        metrics[3].metric("Critic score", f"{score_match.group(1)}/10" if score_match else "—")

        st.markdown('<div class="soft-label">Your four-stage research team</div>', unsafe_allow_html=True)
        render_agent_cards(st.container(), st.session_state.agent_states, results)
        overview_tab, search_tab, scrape_tab = st.tabs(
            ["Agent overview", "Raw search", "Raw scrape"]
        )
        with overview_tab:
            st.markdown("#### Search Agent summary")
            st.markdown(search_summary or "Search summary is not available yet.")
            st.markdown("#### Reader Agent summary")
            st.markdown(reader_summary or "Reader summary is not available yet.")
            if urls:
                st.markdown("#### Sources identified")
                for index, url in enumerate(urls, start=1):
                    st.markdown(f"{index}. [{url}]({url})")

        with search_tab:
            st.markdown("#### Search Agent summary")
            st.markdown(search_summary or "No search summary was returned.")
            st.markdown("#### Raw `web_search` tool response")
            st.markdown(
                "<div class='raw-caption'>Direct output from the web search tool, before the Search Agent summarizes it.</div>",
                unsafe_allow_html=True,
            )
            if search_raw:
                st.code(search_raw, language=None)
            else:
                st.info("No raw web_search tool message was captured for this run.")

        with scrape_tab:
            st.markdown("#### Reader Agent summary")
            st.markdown(reader_summary or "No reader summary was returned.")
            st.markdown("#### Raw `scrape_url` tool response")
            st.markdown(
                "<div class='raw-caption'>Page text returned by the scraper, before the Reader Agent summarizes it.</div>",
                unsafe_allow_html=True,
            )
            if scraped_raw:
                st.code(scraped_raw, language=None)
            else:
                st.info("No raw scrape_url tool message was captured for this run.")

    if st.session_state.history:
        st.caption(f"Saved in this session · {st.session_state.history[0]['created_at']}")
else:
    st.divider()
    st.markdown(
        '<div class="empty-state"><div class="result-heading">Ready when you are</div>'
        '<div>Enter a focused question above to create a report with source links and an AI review.</div></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    "<div style='text-align:center;color:#63738b;font-size:.78rem;padding-top:2.5rem;'>"
    "ResearchPilot · Search · Read · Write · Review</div>",
    unsafe_allow_html=True,
)
