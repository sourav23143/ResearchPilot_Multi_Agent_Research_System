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
    .block-container { max-width: 1220px; padding: 2.2rem 2.3rem 4rem; }
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


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


for key, default in {
    "topic_input": "",
    "active_topic": "",
    "results": {},
    "history": [],
    "run_error": None,
    "run_error_details": None,
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
    st.caption("Your model and search credentials are read from the project’s `.env` file.")

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

if submitted:
    if not topic.strip():
        st.warning("Enter a research question to get started.")
    else:
        st.session_state.active_topic = topic.strip()
        st.session_state.results = {}
        st.session_state.run_error = None
        st.session_state.run_error_details = None
        results = {}
        stage = "Search"
        progress = st.progress(0, text="Preparing your research workspace…")
        try:
            with st.status("01 · Searching the web", expanded=False) as status:
                search_agent = build_search_agent()
                search_result = search_agent.invoke({
                    "messages": [(
                        "user",
                        f"Find recent, reliable, detailed information about: {st.session_state.active_topic}",
                    )]
                })
                results["search"] = content_to_text(search_result["messages"][-1].content)
                if not results["search"].strip():
                    raise RuntimeError("The search agent returned no readable text.")
                st.session_state.results = dict(results)
                status.update(label="01 · Web research gathered", state="complete")
            progress.progress(25, text="Web research gathered")

            stage = "Reader"
            with st.status("02 · Reading a relevant source", expanded=False) as status:
                reader_agent = build_reader_agent()
                reader_result = reader_agent.invoke({
                    "messages": [(
                        "user",
                        f"For the topic '{st.session_state.active_topic}', choose the most relevant URL "
                        f"from these results and scrape it for useful detail.\n\n"
                        f"Search results:\n{results['search'][:5000]}",
                    )]
                })
                results["reader"] = content_to_text(reader_result["messages"][-1].content)
                st.session_state.results = dict(results)
                status.update(label="02 · Source read", state="complete")
            progress.progress(50, text="Source read")

            stage = "Writer"
            with st.status("03 · Drafting your report", expanded=False) as status:
                research = (
                    f"SEARCH RESULTS:\n{results['search'][:6000]}\n\n"
                    f"DETAILED SOURCE CONTENT:\n{results['reader'][:6000]}"
                )
                results["writer"] = writer_chain.invoke({
                    "topic": st.session_state.active_topic,
                    "research": research,
                })
                st.session_state.results = dict(results)
                status.update(label="03 · Report drafted", state="complete")
            progress.progress(75, text="Report drafted")

            stage = "Critic"
            with st.status("04 · Reviewing the report", expanded=False) as status:
                results["critic"] = critic_chain.invoke({"report": results["writer"]})
                st.session_state.results = dict(results)
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
        except Exception as error:
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
    st.subheader("Research workspace")
    st.markdown(f"**Question:** {st.session_state.active_topic}")

    search_text = content_to_text(results.get("search", ""))
    reader_text = content_to_text(results.get("reader", ""))
    report_text = content_to_text(results.get("writer", ""))
    critic_text = content_to_text(results.get("critic", ""))
    urls = find_urls(search_text, reader_text, report_text)
    score_match = re.search(r"score\s*:\s*(\d+(?:\.\d+)?)\s*/\s*10", critic_text, re.IGNORECASE)

    metrics = st.columns(3)
    metrics[0].metric("Sources found", len(urls))
    metrics[1].metric("Report length", f"{word_count(report_text):,} words")
    metrics[2].metric("Critic score", f"{score_match.group(1)}/10" if score_match else "—")

    report_tab, sources_tab, reading_tab, review_tab = st.tabs(
        ["Report", "Sources", "Source notes", "Critic review"]
    )
    with report_tab:
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

    with sources_tab:
        if urls:
            st.markdown("Sources identified in the research output:")
            for index, url in enumerate(urls, start=1):
                st.markdown(f"{index}. [{url}]({url})")
        elif search_text:
            st.info("No source links were detected. Review the search output below for any citations.")
        if search_text:
            with st.expander("Full search output", expanded=not urls):
                st.markdown(search_text)

    with reading_tab:
        if reader_text:
            st.markdown(reader_text)
        else:
            st.info("The source-reading step did not produce content.")

    with review_tab:
        if critic_text:
            st.markdown(critic_text)
        else:
            st.info("The critic review is not available yet.")

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
