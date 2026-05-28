import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="RESEARCH LABS",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@400;500;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Sans', sans-serif;
    background: #F0EBE0 !important;
    color: #0a0a0a !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.topbar {
    background: #0a0a0a;
    color: #F0EBE0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2.5rem;
    height: 52px;
    border-bottom: 4px solid #0a0a0a;
}
.topbar-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.12em;
    color: #FFE500;
}
.topbar-mono {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: #666;
    text-transform: uppercase;
}
.topbar-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #FF2D2D;
    display: inline-block;
    margin-right: 0.4rem;
    animation: blink 1.2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── TICKER ── */
.ticker {
    background: #FFE500;
    border-bottom: 4px solid #0a0a0a;
    overflow: hidden;
    height: 34px;
    display: flex;
    align-items: center;
}
.ticker-inner {
    display: flex;
    animation: scroll 22s linear infinite;
    white-space: nowrap;
}
.ticker-inner span {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: #0a0a0a;
    text-transform: uppercase;
    padding: 0 2rem;
}
.ticker-inner span::after { content: " ◼ "; margin-left: 2rem; }
@keyframes scroll { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }

/* ── HERO ── */
.hero-band {
    background: #0a0a0a;
    padding: 3.5rem 2.5rem 3rem;
    border-bottom: 4px solid #0a0a0a;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: end;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 10vw, 8rem);
    line-height: 0.85;
    letter-spacing: 0.04em;
    color: #F0EBE0;
}
.hero-title em { color: #FFE500; font-style: normal; }
.hero-meta { display:flex; flex-direction:column; gap:1rem; align-items:flex-start; justify-content:flex-end; }
.hero-badge {
    display: inline-block;
    background: #FFE500;
    color: #0a0a0a;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 5px 12px;
    border: 3px solid #F0EBE0;
}
.hero-desc {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.95rem;
    color: #999;
    line-height: 1.7;
    max-width: 340px;
}

/* ── SECTION LABEL ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #0a0a0a;
    padding: 6px 0;
    border-bottom: 3px solid #0a0a0a;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::before {
    content: '';
    display: inline-block;
    width: 10px; height: 10px;
    background: #FFE500;
    border: 2px solid #0a0a0a;
    flex-shrink: 0;
}

/* ── INPUT ── */
.stTextInput > div > div > input {
    background: #fff !important;
    border: 4px solid #0a0a0a !important;
    border-radius: 0 !important;
    color: #0a0a0a !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1rem !important;
    box-shadow: 5px 5px 0 #0a0a0a !important;
    transition: box-shadow 0.08s !important;
}
.stTextInput > div > div > input:focus {
    box-shadow: 7px 7px 0 #FFE500 !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: #aaa !important; }
.stTextInput > label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #0a0a0a !important;
    font-weight: 700 !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: #FFE500 !important;
    color: #0a0a0a !important;
    border: 4px solid #0a0a0a !important;
    border-radius: 0 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.5rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.4rem 2rem !important;
    box-shadow: 5px 5px 0 #0a0a0a !important;
    transition: all 0.07s !important;
    width: 100% !important;
}
.stButton > button:hover {
    box-shadow: 8px 8px 0 #0a0a0a !important;
    transform: translate(-2px,-2px) !important;
}
.stButton > button:active {
    box-shadow: 2px 2px 0 #0a0a0a !important;
    transform: translate(3px,3px) !important;
}

/* ── PIPELINE STEPS ── */
.pipe-step {
    border: 4px solid #0a0a0a;
    padding: 1rem 1.25rem;
    margin-bottom: -4px;
    display: flex;
    align-items: center;
    gap: 1rem;
    background: #F0EBE0;
}
.pipe-step.active { background: #FFE500; }
.pipe-step.done   { background: #0a0a0a; color: #F0EBE0; }
.pipe-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    line-height: 1;
    color: #ccc;
    min-width: 2rem;
    text-align: center;
}
.pipe-step.active .pipe-num { color: #0a0a0a; }
.pipe-step.done   .pipe-num { color: #FFE500; }
.pipe-info { flex: 1; }
.pipe-name {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.pipe-desc { font-size: 0.75rem; color: #777; margin-top: 2px; }
.pipe-step.active .pipe-desc { color: #555; }
.pipe-step.done   .pipe-desc { color: #aaa; }
.pipe-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    padding: 3px 8px;
    border: 2px solid currentColor;
    text-transform: uppercase;
    white-space: nowrap;
}
.badge-wait { color: #bbb; border-color: #bbb; }
.badge-run  { color: #0a0a0a; border-color: #0a0a0a; animation: pulse 0.8s infinite alternate; }
.badge-done { color: #00ff6a; border-color: #00ff6a; }
@keyframes pulse { from{opacity:1} to{opacity:0.4} }

/* ── PROGRESS BAR ── */
.prog-wrap {
    border: 4px solid #0a0a0a;
    background: #fff;
    height: 22px;
    margin: 1.5rem 0 0.5rem;
    box-shadow: 4px 4px 0 #0a0a0a;
    overflow: hidden;
}
.prog-fill {
    height: 100%;
    background: #FFE500;
    transition: width 0.4s ease;
    position: relative;
}
.prog-fill::after {
    content: '';
    position: absolute;
    right: 0; top: 0; bottom: 0;
    width: 4px;
    background: #0a0a0a;
}
.prog-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: #0a0a0a;
    text-align: right;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

/* ── RESULT CARDS ── */
.res-card {
    border: 4px solid #0a0a0a;
    box-shadow: 6px 6px 0 #0a0a0a;
    margin-bottom: 1.5rem;
    overflow: hidden;       /* keeps children inside */
}
.res-header {
    background: #0a0a0a;
    color: #FFE500;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 0.1em;
    padding: 0.6rem 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.res-header.blue  { background: #1a1aff; }
.res-header.green { background: #006622; }
.res-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.15em;
    padding: 3px 8px;
    border: 2px solid rgba(255,229,0,0.8);
    color: rgba(255,229,0,0.8);
    text-transform: uppercase;
}

/* ── BODY INSIDE RES-CARD — scrollable container ── */
.res-body-wrap {
    background: #fff;
    padding: 1.25rem 1.5rem;
    max-height: 420px;
    overflow-y: auto;
    border-top: 4px solid #0a0a0a;
}
.res-body-wrap::-webkit-scrollbar { width: 8px; }
.res-body-wrap::-webkit-scrollbar-track { background: #F0EBE0; }
.res-body-wrap::-webkit-scrollbar-thumb { background: #0a0a0a; }

/* Streamlit markdown rendered inside the card */
.res-body-wrap p, .res-body-wrap li, .res-body-wrap h1,
.res-body-wrap h2, .res-body-wrap h3, .res-body-wrap h4 {
    color: #0a0a0a !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    line-height: 1.75 !important;
}
.res-body-wrap h1, .res-body-wrap h2, .res-body-wrap h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 0.05em !important;
    margin: 1rem 0 0.4rem !important;
}
.res-body-wrap pre {
    background: #F0EBE0;
    border: 2px solid #0a0a0a;
    padding: 0.75rem;
    font-size: 0.8rem;
    overflow-x: auto;
}

/* raw text card (search/scrape) */
.raw-body {
    background: #fff;
    padding: 1.25rem 1.5rem;
    max-height: 300px;
    overflow-y: auto;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.7;
    color: #0a0a0a;
    white-space: pre-wrap;
    word-break: break-word;
    border-top: 4px solid #0a0a0a;
}
.raw-body::-webkit-scrollbar { width: 8px; }
.raw-body::-webkit-scrollbar-thumb { background: #0a0a0a; }

/* ── DOWNLOAD ── */
.stDownloadButton > button {
    background: #0a0a0a !important;
    color: #FFE500 !important;
    border: 4px solid #0a0a0a !important;
    border-radius: 0 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.2rem !important;
    letter-spacing: 0.1em !important;
    box-shadow: 4px 4px 0 #555 !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    box-shadow: 6px 6px 0 #555 !important;
    transform: translate(-2px,-2px) !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    color: #0a0a0a !important;
    background: #F0EBE0 !important;
    border: 3px solid #0a0a0a !important;
    border-radius: 0 !important;
}

/* ── FOOTER ── */
.brutal-footer {
    border-top: 4px solid #0a0a0a;
    background: #0a0a0a;
    color: #555;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-align: center;
    padding: 1rem;
    text-transform: uppercase;
    margin-top: 3rem;
}

/* padding for main cols */
.main-left  { padding: 2rem 2.5rem; border-right: 4px solid #0a0a0a; }
.main-right { padding: 2rem 2rem; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in [("results", {}), ("step", 0), ("done", False), ("running", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── TOPBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">Research Labs_</div>
    <div class="topbar-mono"><span class="topbar-dot"></span>Multi-Agent AI System &nbsp;·&nbsp; v2.0</div>
</div>
""", unsafe_allow_html=True)

# ── TICKER ────────────────────────────────────────────────────────────────────
items = ["Search Agent","Reader Agent","Writer Chain","Critic Chain",
         "Real-time Web Scraping","LLM Analysis","Automated Research"] * 2
ticker_html = "".join(f"<span>{i}</span>" for i in items)
st.markdown(f'<div class="ticker"><div class="ticker-inner">{ticker_html}</div></div>', unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-band">
    <div class="hero-title">RESEARCH<br><em>LABS_</em></div>
    <div class="hero-meta">
        <span class="hero-badge">⬛ 4 AI Agents · LangGraph</span>
        <p class="hero-desc">Four specialized agents search the web, scrape sources, write a full report, and critique it — automatically.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── PIPELINE RENDERER (used in right column & mid-run) ───────────────────────
STEP_META = [
    ("01", "🔍", "Search Agent",  "Gathers recent web info",    "search"),
    ("02", "📄", "Reader Agent",  "Scrapes top URL content",    "reader"),
    ("03", "✍️", "Writer Chain",  "Drafts full report",         "writer"),
    ("04", "🧠", "Critic Chain",  "Reviews & scores report",    "critic"),
]

def render_pipeline(done_keys: list, active_key: str = ""):
    pipe_html = ""
    for num, icon, name, desc, key in STEP_META:
        if key in done_keys:
            cls, badge_cls, badge_txt = "done", "badge-done", "✓ DONE"
        elif key == active_key:
            cls, badge_cls, badge_txt = "active", "badge-run", "● RUNNING"
        else:
            cls, badge_cls, badge_txt = "", "badge-wait", "WAITING"
        pipe_html += f"""
        <div class="pipe-step {cls}">
            <div class="pipe-num">{num}</div>
            <div class="pipe-info">
                <div class="pipe-name">{icon} {name}</div>
                <div class="pipe-desc">{desc}</div>
            </div>
            <span class="pipe-badge {badge_cls}">{badge_txt}</span>
        </div>"""
    pct = len(done_keys) / 4 * 100
    pipe_html += f"""
    <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>
    <div class="prog-label">{len(done_keys)}/4 steps complete — {int(pct)}%</div>
    """
    return pipe_html

# ── LAYOUT ────────────────────────────────────────────────────────────────────
left, right = st.columns([3, 1.3])

with left:
    st.markdown('<div class="main-left">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">// Input</div>', unsafe_allow_html=True)
    topic = st.text_input("Research Topic",
                          placeholder="e.g. Quantum computing breakthroughs in 2025",
                          key="topic_input")
    run_btn = st.button("RUN PIPELINE →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="main-right">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">// Pipeline</div>', unsafe_allow_html=True)
    pipeline_slot = st.empty()          # ← will be updated live
    pipeline_slot.markdown(
        render_pipeline(list(st.session_state.results.keys())),
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── RESULTS AREA (below the two columns) ─────────────────────────────────────
results_slot = st.empty()

def show_results(r):
    with results_slot.container():
        st.markdown('<div style="padding:0 2.5rem">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">// Results</div>', unsafe_allow_html=True)

        # Raw collapsibles
        if "search" in r:
            with st.expander("🔍  SEARCH RESULTS (raw)", expanded=False):
                st.markdown(f'<div class="raw-body">{r["search"]}</div>', unsafe_allow_html=True)

        if "reader" in r:
            with st.expander("📄  SCRAPED CONTENT (raw)", expanded=False):
                st.markdown(f'<div class="raw-body">{r["reader"]}</div>', unsafe_allow_html=True)

        # Final Report — content INSIDE the card via st.container
        if "writer" in r:
            st.markdown("""
            <div class="res-card">
                <div class="res-header blue">✍ Final Research Report
                    <span class="res-tag">Step 03 · Writer</span>
                </div>
                <div class="res-body-wrap" id="writer-body">
            """, unsafe_allow_html=True)
            # Render markdown natively (Streamlit handles it properly)
            st.markdown(r["writer"])
            st.markdown("</div></div>", unsafe_allow_html=True)

            st.download_button(
                label="⬛ DOWNLOAD REPORT (.md)",
                data=r["writer"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
            )

        # Critic — content INSIDE the card
        if "critic" in r:
            st.markdown("""
            <div class="res-card">
                <div class="res-header green">🧠 Critic Feedback
                    <span class="res-tag">Step 04 · Critic</span>
                </div>
                <div class="res-body-wrap" id="critic-body">
            """, unsafe_allow_html=True)
            st.markdown(r["critic"])
            st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.done and st.session_state.results:
    show_results(st.session_state.results)

# ── TRIGGER ───────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.step    = 0
        st.session_state.done    = False
        st.session_state.running = True

        t = topic.strip()
        results = {}
        order   = ["search", "reader", "writer", "critic"]

        def refresh_pipeline(done_keys, active):
            pipeline_slot.markdown(
                render_pipeline(done_keys, active),
                unsafe_allow_html=True
            )

        # ── Step 1: Search ──────────────────────────────────────────────────
        refresh_pipeline([], "search")
        with st.spinner("🔍  Search Agent scanning the web…"):
            sa = build_search_agent()
            sr = sa.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {t}")]})
            results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

        # ── Step 2: Reader ──────────────────────────────────────────────────
        refresh_pipeline(["search"], "reader")
        with st.spinner("📄  Reader Agent scraping top resource…"):
            ra = build_reader_agent()
            rr = ra.invoke({"messages": [("user",
                f"Based on the following search results about '{t}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}")]})
            results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

        # ── Step 3: Writer ──────────────────────────────────────────────────
        refresh_pipeline(["search","reader"], "writer")
        with st.spinner("✍️  Writer drafting the report…"):
            combined = f"SEARCH RESULTS:\n{results['search']}\n\nDETAILED SCRAPED CONTENT:\n{results['reader']}"
            results["writer"] = writer_chain.invoke({"topic": t, "research": combined})
        st.session_state.results = dict(results)

        # ── Step 4: Critic ──────────────────────────────────────────────────
        refresh_pipeline(["search","reader","writer"], "critic")
        with st.spinner("🧠  Critic reviewing the report…"):
            results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

        # ── Done ────────────────────────────────────────────────────────────
        refresh_pipeline(["search","reader","writer","critic"], "")
        st.session_state.running = False
        st.session_state.done    = True
        show_results(results)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brutal-footer">
    Research Labs · Powered by LangGraph + LLM Agents · Built with Streamlit
</div>
""", unsafe_allow_html=True)