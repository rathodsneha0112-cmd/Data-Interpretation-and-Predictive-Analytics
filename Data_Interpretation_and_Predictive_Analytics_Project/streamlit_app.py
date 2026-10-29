"""DATA INTERPRETATION AND PREDICTIVE ANALYTICS — Streamlit learning and insights app.
Run locally: streamlit run streamlit_app.py. Quiz history is session-only; no database is used."""
import html, pathlib, time, urllib.parse
import streamlit as st
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Polygon
import math

from questions import MODULES, QUESTIONS
from quiz_engine import Quiz
from study import STUDY

GUIDES = pathlib.Path(__file__).resolve().parent / "guides"
BG, CARD, CARD2, BORDER = "#F4F7FA", "#FFFFFF", "#E7F2F0", "#D5E2E6"
PRI, PRI_L, ACCENT = "#0F766E", "#115E59", "#F59E0B"
OK, ERR, WARN, FG, MUT = "#15803D", "#B91C1C", "#B45309", "#1F2937", "#64748B"
OK_BG, ERR_BG = "#DCFCE7", "#FEE2E2"

st.set_page_config(page_title="DATA INTERPRETATION AND PREDICTIVE ANALYTICS", page_icon="📊", layout="wide")
st.markdown(f"""<style>
:root {{ color-scheme: light; }}
html, body, [class*="css"] {{ font-family: Inter, "Segoe UI", Arial, sans-serif; }}
.block-container{{padding-top:1.8rem;padding-bottom:3rem;max-width:1280px}}
.stApp{{background:linear-gradient(180deg,#F7FAFC 0%,{BG} 48%,#F1F7F7 100%);color:{FG}}}
[data-testid="stHeader"]{{background:rgba(247,250,252,.82)}}
section[data-testid="stSidebar"]{{background:linear-gradient(180deg,#E8F4F1 0%,#F2F7F9 100%);border-right:1px solid {BORDER}}}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2{{font-size:1.12rem;letter-spacing:-.02em;color:#123B43}}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{{color:#5C7379}}
.opt{{padding:12px 16px;margin:8px 0;border-radius:12px;background:{CARD};border:1px solid {BORDER};color:{FG};transition:border-color .18s ease,background .18s ease}}
.opt.ok{{background:{OK_BG};border-color:{OK}}} .opt.bad{{background:{ERR_BG};border-color:{ERR}}} .opt.dim{{color:{MUT}}}
.pill{{display:inline-block;padding:4px 11px;border-radius:999px;background:#E4F2EF;color:{PRI};font-size:.77rem;font-weight:700;margin-right:6px;border:1px solid #D2E8E2}}
.timer{{text-align:center;padding:9px 14px;border-radius:12px;background:{CARD};border:1px solid {BORDER};color:{PRI};font-family:Consolas,monospace;font-size:1.25rem;font-weight:800;box-shadow:0 4px 12px rgba(18,59,67,.04)}}
.timer.low{{color:{ERR}}}
.q{{font-size:1.2rem;font-weight:700;line-height:1.55;margin:14px 0 10px}}
.sol{{color:{MUT};margin-top:10px;line-height:1.65}}
.dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px;box-shadow:0 0 0 3px rgba(15,118,110,.08)}}
.hero{{position:relative;overflow:hidden;padding:2.6rem 2.5rem;border-radius:24px;background:linear-gradient(118deg,#102B3A 0%,#0C5D60 52%,#138879 100%);color:white;margin:0 0 1.4rem 0;box-shadow:0 18px 42px rgba(13,79,80,.18);border:1px solid rgba(255,255,255,.12)}}
.hero:after{{content:"";position:absolute;width:280px;height:280px;border-radius:50%;right:-70px;top:-105px;border:1px solid rgba(219,255,247,.2);box-shadow:0 0 0 28px rgba(219,255,247,.035),0 0 0 58px rgba(219,255,247,.025);pointer-events:none}}
.hero .eyebrow{{display:inline-block;font-size:.74rem;letter-spacing:.15em;font-weight:800;text-transform:uppercase;color:#C9F5EA;background:rgba(221,255,246,.1);border:1px solid rgba(221,255,246,.16);padding:7px 12px;border-radius:999px;margin-bottom:1.1rem}}
.hero h1{{font-size:clamp(2rem,4.3vw,3.25rem);line-height:1.08;letter-spacing:-.045em;color:white;margin:0 0 1rem 0;max-width:900px}}
.hero p{{font-size:1.04rem;line-height:1.75;max-width:850px;color:#E3F5F2;margin:0}}
.section-kicker{{color:{PRI};font-weight:850;letter-spacing:.11em;text-transform:uppercase;font-size:.72rem;margin:.35rem 0 .55rem}}
.research-card{{padding:1.25rem 1.3rem;border:1px solid {BORDER};border-radius:17px;background:linear-gradient(160deg,#FFFFFF 0%,#FBFDFD 100%);height:100%;box-shadow:0 7px 20px rgba(26,62,74,.045);border-top:3px solid #85C8B9}}
.research-card b{{color:#153C46;font-size:1rem;letter-spacing:-.01em}}
.research-card p{{color:#536771;line-height:1.65;margin:.65rem 0 .1rem;font-size:.94rem}}
.presentation-shell{{background:linear-gradient(135deg,#FFFFFF 0%,#F0F8F6 100%);border:1px solid #D2E6E2;border-radius:20px;padding:1.35rem 1.45rem 1.45rem;box-shadow:0 10px 27px rgba(18,59,67,.06);margin:.55rem 0 1.6rem}}
.presentation-topline{{display:flex;align-items:center;gap:10px;color:#0F766E;font-size:.72rem;font-weight:850;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.45rem}}
.presentation-title{{font-size:1.35rem;font-weight:800;letter-spacing:-.025em;color:#143B45;margin:0 0 1rem}}
.presentation-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:1.15rem}}
.presentation-item{{background:rgba(255,255,255,.86);border:1px solid #DCEAE7;padding:12px 14px;border-radius:13px;min-height:80px}}
.presentation-label{{font-size:.69rem;color:#668087;text-transform:uppercase;letter-spacing:.08em;font-weight:800;margin-bottom:5px}}
.presentation-value{{font-size:.9rem;line-height:1.4;color:#183C46;font-weight:700}}
.team-label{{font-size:.8rem;color:#4D6D73;font-weight:800;letter-spacing:.04em;margin:.2rem 0 .55rem}}
.member-table{{width:100%;border-collapse:separate;border-spacing:0;background:white;border:1px solid #DCEAE7;border-radius:13px;overflow:hidden}}
.member-table th{{background:#123F49;color:white;text-align:left;padding:11px 14px;font-size:.76rem;letter-spacing:.05em;text-transform:uppercase}}
.member-table td{{padding:10px 14px;border-bottom:1px solid #E7EFEE;color:{FG};font-size:.9rem}}
.member-table tr:nth-child(even) td{{background:#F7FBFA}}
.member-table tr:last-child td{{border-bottom:none}}
.member-table td:first-child{{color:#0F766E;font-weight:800;width:110px}}
div.stButton>button{{border-radius:12px;font-weight:700;border:1px solid {BORDER};min-height:2.65rem;transition:all .16s ease}}
div.stButton>button:hover{{border-color:#77BCAF;color:#0B5F59;box-shadow:0 5px 13px rgba(15,118,110,.1);transform:translateY(-1px)}}
[data-testid="stMetric"]{{background:rgba(255,255,255,.9);padding:1rem 1.05rem;border:1px solid {BORDER};border-radius:15px;box-shadow:0 5px 16px rgba(26,62,74,.035)}}
[data-testid="stMetricLabel"]{{color:#607780;font-weight:650}}
h1, h2, h3{{letter-spacing:-.025em}}
hr{{border-color:#D9E6E8}}
@media (max-width: 800px){{.hero{{padding:1.8rem 1.35rem}}.presentation-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.presentation-shell{{padding:1.05rem}}}}
</style>""", unsafe_allow_html=True)

ss = st.session_state
for k, v in (("page", "home"), ("module", None), ("history", []), ("quiz", None), ("qid", 0)):
    ss.setdefault(k, v)


def esc(s):
    """HTML-escape and neutralise '$' so Streamlit does not treat it as LaTeX."""
    return html.escape(str(s)).replace("$", "&#36;")


# ---------- navigation / state ----------
def go(page, module=None):
    ss.page, ss.module = page, module


def start(module, n):
    ss.quiz = Quiz(module, n); ss.qid += 1; ss.page = "quiz"


def accuracy(module=None):
    """Return question-weighted accuracy; mixed quizzes contribute to each module too."""
    history = list(ss.history)
    if module is None:
        total = sum(int(item.get("total", 0)) for item in history)
        score = sum(int(item.get("score", 0)) for item in history)
    else:
        score = total = 0
        for item in history:
            detail = item.get("module_scores", {}).get(module)
            if detail:
                score += int(detail.get("correct", 0))
                total += int(detail.get("total", 0))
            elif item.get("module") == module:
                score += int(item.get("score", 0))
                total += int(item.get("total", 0))
    return score / total * 100 if total else None


def finish():
    """Store attempt-level and module-level stats only in this browser session."""
    q = ss.quiz
    if q is None:
        ss.page = "home"
        return
    sel = ss.get(f"sel_{ss.qid}_{q.i}")
    if q.i not in q.answers and sel is not None:
        q.answer(q.i, sel)
    if not q.done:
        q.done = True
        q.elapsed = min(q.limit, int(time.time() - q.start))
        per_module = {
            name: {"correct": ok, "total": tot, "accuracy": (ok / tot * 100 if tot else 0.0)}
            for name, (ok, tot) in q.by_module().items()
        }
        total_q = len(q.qs)
        score = q.score()
        ss.history.append({
            "module": q.module, "score": score, "total": total_q,
            "accuracy": (score / total_q * 100 if total_q else 0.0),
            "time": q.elapsed, "module_scores": per_module, "timestamp": time.time(),
        })
    ss.page = "results"


def header(title, sub=""):
    st.markdown(f"## {title}")
    if sub: st.caption(sub)


def sidebar():
    cur = ss.page
    q = ss.quiz
    active = {
        "home": "home", "dash": "dash", "insights": "insights",
        "results": "dash", "review": "dash", "hub": "learn", "learn": "learn",
        "quiz": "quiz" if (q is not None and q.module == "Mixed") else "dash",
    }.get(cur, "home")
    with st.sidebar:
        st.markdown("## 📊 DATA INTERPRETATION")
        st.markdown("### & PREDICTIVE ANALYTICS")
        st.caption("Read data · Build reasoning · Grow with practice")
        items = (
            ("home", "🏡  Home", go, ("home",)),
            ("dash", "📈  Learning Dashboard", go, ("dash",)),
            ("learn", "📚  Study & Practice Library", go, ("hub",)),
            ("insights", "🔎  Performance Insights", go, ("insights",)),
            ("quiz", "⚡  Quick Mixed Quiz · 20 Q", start, (None, 20)),
        )
        for key, label, cb, args in items:
            st.button(label, key=f"nav_{key}", on_click=cb, args=args, use_container_width=True, type="primary" if active == key else "secondary")
        st.divider()
        st.caption("Course: Logic and Data Interpretation II\n\nClass: TE / B · AI & DS\n\nScores are kept for this browser session only.")


# ---------- study material ----------
def video_url(q): return q if q.startswith("http") else "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q)


def cheat_sheet(m):
    s = STUDY[m]; li = lambda xs: "".join(f"<li>{html.escape(x)}</li>" for x in xs)
    rows = "".join(f"<tr><td><b>{html.escape(a)}</b></td><td>{html.escape(b)}</td></tr>" for a, b in s["formulas"])
    return (f"<html><head><meta charset='utf-8'><title>{m} cheat sheet</title><style>body{{font-family:Segoe UI,Arial;max-width:760px;margin:30px auto;line-height:1.5}}"
            f"td{{border:1px solid #ccc;padding:6px 10px}}table{{border-collapse:collapse}}h1{{color:{s['color']}}}</style></head><body><h1>{m} – Cheat Sheet</h1>"
            f"<p><i>{html.escape(s['tagline'])}</i></p><h2>Key notes</h2><ul>{li(s['notes'])}</ul><h2>Formulas</h2><table>{rows}</table>"
            f"<h2>Exam tips</h2><ul>{li(s['tips'])}</ul><p><small>Use your browser's Print → Save as PDF.</small></p></body></html>")


def study_panel(m, ctx):
    s = STUDY[m]; t1, t2, t3 = st.tabs(["📝  Notes", "➗  Formulas", "▶  Videos & PDF"])
    with t1:
        for n in s["notes"]:
            with st.container(border=True): st.markdown(f"<span class='dot' style='background:{s['color']}'></span>{esc(n)}", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"**💡 Exam tips**")
            for t in s["tips"]: st.markdown(f"- {esc(t)}", unsafe_allow_html=True)
    with t2:
        for a, b in s["formulas"]:
            with st.container(border=True): st.caption(a); st.code(b, language=None)
    with t3:
        st.caption("Videos open YouTube in a new tab.")
        for title, desc, q in s["videos"]:
            with st.container(border=True):
                st.markdown(f"**{title}**"); st.caption(desc); st.link_button("▶ Watch", video_url(q))
        with st.container(border=True):
            pdf = GUIDES / s.get("pdf", f"{m}.pdf")
            st.markdown(f"**{m} cheat sheet / PDF guide**")
            if pdf.exists():
                st.download_button("📄 Download PDF guide", pdf.read_bytes(), file_name=pdf.name, mime="application/pdf", key=f"pdf_{ctx}_{m}")
            else:
                st.caption("Printable cheat sheet generated from the notes (open it, then Print → Save as PDF).")
                st.download_button("📄 Download cheat sheet", cheat_sheet(m), file_name=f"{m}_cheatsheet.html", mime="text/html", key=f"cs_{ctx}_{m}")


# ---------- pages ----------
def topic_card(m, buttons):
    s = STUDY[m]
    with st.container(border=True):
        a = accuracy(m)
        st.markdown(f"<span class='dot' style='background:{s['color']}'></span><b style='font-size:1.1rem'>{m}</b>"
                    f"<span class='pill' style='float:right;color:{s['color']}'>{'New' if a is None else f'{a:.0f}%'}</span>", unsafe_allow_html=True)
        st.caption(s["tagline"])
        if buttons == "dash": st.progress((a or 0) / 100)
        else: st.markdown(f"<span class='pill'>{len(s['notes'])} notes</span><span class='pill'>{len(s['formulas'])} formulas</span><span class='pill'>{len(s['videos'])} videos</span>", unsafe_allow_html=True)
        c = st.columns(3 if buttons == "dash" else 2)
        c[0].button("📖 Study", key=f"{buttons}_study_{m}", on_click=go, args=("learn", m), use_container_width=True)
        if buttons == "dash":
            c[1].button("10 Q", key=f"q10_{m}", on_click=start, args=(m, 10), use_container_width=True)
            c[2].button("15 Q", key=f"q15_{m}", on_click=start, args=(m, 15), use_container_width=True)
        else:
            c[1].button("Quiz ▶", key=f"hub_quiz_{m}", on_click=start, args=(m, 10), use_container_width=True)


def home_page():
    """Polished landing page with academic presentation details and project context."""
    st.markdown(
        "<div class='hero'>"
        "<div class='eyebrow'>STUDENT LEARNING PLATFORM · ACADEMIC PROJECT</div>"
        "<h1>DATA INTERPRETATION AND<br>PREDICTIVE ANALYTICS</h1>"
        "<p>Strengthen logical reasoning with guided study resources, timed practice, clear solutions, and personal progress insights—all in one focused learning space.</p>"
        "</div>", unsafe_allow_html=True,
    )
    a, b, c = st.columns([1.15, 1, 1])
    with a:
        st.button("📈  Explore Dashboard", key="home_dashboard", on_click=go, args=("dash",), type="primary", use_container_width=True)
    with b:
        st.button("📚  Browse Learning Hub", key="home_learn", on_click=go, args=("hub",), use_container_width=True)
    with c:
        st.button("🔎  View Performance Insights", key="home_insights", on_click=go, args=("insights",), use_container_width=True)

    st.markdown("<div class='section-kicker'>Platform snapshot</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Question library", f"{len(QUESTIONS)}")
    k2.metric("Learning areas", f"{len(MODULES)}")
    k3.metric("Difficulty bands", "3")
    k4.metric("Practice formats", "10 / 15 / 20 Q")

    # Presentation details intentionally appear before the research summary on the Home page.
    st.markdown("### Presentation details — TE / B")
    members = [
        ("05", "Sudiksha Dumbre"),
        ("18", "Sakshi Mulik"),
        ("31", "Vaishnavi Pol"),
        ("32", "Vedant Rajmane"),
        ("35", "Sneha Rathod"),
    ]
    member_rows = "".join(f"<tr><td>{roll}</td><td>{name}</td></tr>" for roll, name in members)
    st.markdown(
        "<div class='presentation-shell'>"
        "<div class='presentation-topline'>✦ Project presentation · Artificial Intelligence and Data Science</div>"
        "<div class='presentation-grid'>"
        "<div class='presentation-item'><div class='presentation-label'>Course name</div><div class='presentation-value'>Logic and Data Interpretation II</div></div>"
        "<div class='presentation-item'><div class='presentation-label'>Branch</div><div class='presentation-value'>Artificial Intelligence and Data Science</div></div>"
        "<div class='presentation-item'><div class='presentation-label'>Class / Division</div><div class='presentation-value'>TE / B</div></div>"
        "<div class='presentation-item'><div class='presentation-label'>Professor</div><div class='presentation-value'>Siddharth Machhindra Bhore</div></div>"
        "</div>"
        "<div class='team-label'>PROJECT TEAM</div>"
        f"<table class='member-table'><thead><tr><th>Roll No.</th><th>Group Member</th></tr></thead><tbody>{member_rows}</tbody></table>"
        "</div>", unsafe_allow_html=True,
    )

    st.markdown("### Research-style project summary")
    st.markdown(
        "Students can find it difficult to practise regularly without knowing which reasoning skills need more attention. This platform brings together a structured question library, timed quizzes, worked explanations, topic-level scores, and a simple estimate based on recent attempts. It turns quiz results into practical feedback, helping learners choose what to review next."
    )
    cards = st.columns(3)
    research_cards = [
        ("01 · Learning challenge", "Students need a consistent way to practise charts, number patterns, calendars, and clock-based questions while identifying recurring errors."),
        ("02 · Project approach", "Questions are organised across six learning areas and three difficulty bands. Answers are checked against answer keys, then results are summarised by topic."),
        ("03 · Practical value", "Learners receive an immediate score, worked explanations, topic-specific revision prompts, and a simple estimate from recent quiz results."),
    ]
    for col, (title, body) in zip(cards, research_cards):
        with col:
            st.markdown(f"<div class='research-card'><b>{title}</b><p>{body}</p></div>", unsafe_allow_html=True)

    with st.expander("Project goals and workflow", expanded=False):
        st.markdown("**Main goals**")
        st.markdown("- Offer structured practice in clock problems, calendars, number patterns, bar charts, pie charts, and line graphs.")
        st.markdown("- Provide quick answer feedback along with an explanation for each question.")
        st.markdown("- Summarise topic accuracy and use recent attempts to calculate a clear, easy-to-follow performance estimate.")
        st.markdown("**How a learner uses the platform**")
        st.markdown("1. Choose a topic or mixed quiz.  2. Complete the timed questions.  3. Check the score and worked answers.  4. Use topic results to plan the next revision session.")
        st.markdown("**Analytics in context:** predictive analytics uses historical information to estimate possible future outcomes. In this project, the displayed estimate is a recency-weighted average of recent quiz percentages. It is an interpretable baseline, not a trained or validated machine-learning model; actual future performance may differ.")

    st.markdown("### Explore the learning areas")
    st.markdown(" · ".join(f"**{esc(m)}**" for m in MODULES))

    with st.expander("References and project scope", expanded=False):
        st.markdown("**Further reading**")
        st.markdown("- [IBM — What is Predictive Analytics?](https://www.ibm.com/think/topics/predictive-analytics): a practical introduction to analysing historical data and estimating outcomes.")
        st.markdown("- [Educational Data Mining to Predict Students’ Academic Performance: A Survey Study (2023)](https://eric.ed.gov/?id=EJ1363934): an overview of research on student-performance prediction.")
        st.markdown("- [Streamlit documentation](https://docs.streamlit.io/): reference documentation for the web application framework.")
        st.caption("Project boundaries: quiz history is kept only in the active Streamlit session and is not written to a database. The score estimate is a learning aid, not a validated predictor of examination marks.")


def insights():
    """Explain recent quiz performance with a transparent, lightweight forecast."""
    header("Performance Insights", "Review your quiz history, identify topics to revisit, and see a simple estimate based on recent results.")
    history = list(ss.history)
    if not history:
        st.info("No attempts have been recorded in this browser session yet. Complete a topic quiz or the Mixed Challenge to unlock your personal insights.")
        st.markdown("#### How this page works")
        st.markdown("- **Descriptive analysis:** reports quiz scores and accuracy by topic.\n- **Predictive baseline:** after attempts are available, computes a weighted average of up to the last three quiz percentages, giving more weight to the most recent score.\n- **Action:** directs you to the lowest-scoring assessed topic for revision.")
        st.caption("This is an interpretable baseline, not a trained machine-learning model. Data is session-only.")
        return

    percentages = [item.get("score", 0) / item.get("total", 1) * 100 for item in history if item.get("total", 0)]
    recent = percentages[-3:]
    weights = list(range(1, len(recent) + 1))
    forecast = sum(score * weight for score, weight in zip(recent, weights)) / sum(weights)
    average = sum(percentages) / len(percentages) if percentages else 0
    delta = percentages[-1] - percentages[-2] if len(percentages) >= 2 else None

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Completed attempts", len(percentages))
    m2.metric("Average accuracy", f"{average:.1f}%")
    m3.metric("Latest accuracy", f"{percentages[-1]:.1f}%", None if delta is None else f"{delta:+.1f} pp vs previous")
    m4.metric("Estimated next accuracy", f"{forecast:.1f}%")
    st.caption(f"Estimate method: recency-weighted mean of the last {len(recent)} attempt(s), with weights {', '.join(map(str, weights))} from oldest to newest. It is a descriptive baseline, not a trained predictive model.")

    left, right = st.columns([1.35, 1])
    with left:
        with st.container(border=True):
            st.markdown("#### Attempt accuracy trend")
            fig = Figure(figsize=(7, 3.5), dpi=110, facecolor=CARD)
            ax = fig.add_subplot(111); ax.set_facecolor(CARD)
            xs = list(range(1, len(percentages) + 1))
            ax.plot(xs, percentages, marker="o", color=PRI, linewidth=2.5, label="Actual accuracy")
            ax.axhline(forecast, color=ACCENT, linestyle="--", linewidth=2, label="Recent weighted estimate")
            ax.set_ylim(0, 100); ax.set_xlabel("Quiz attempt", color=MUT); ax.set_ylabel("Accuracy (%)", color=MUT)
            ax.set_xticks(xs if len(xs) <= 12 else xs[::max(1, len(xs)//10)])
            ax.tick_params(colors=MUT); ax.grid(axis="y", alpha=.22, color=MUT)
            for spine in ax.spines.values(): spine.set_color(BORDER)
            ax.legend(facecolor=CARD, labelcolor=FG, edgecolor=BORDER)
            fig.tight_layout(); st.pyplot(fig)
    with right:
        with st.container(border=True):
            st.markdown("#### What the estimate means")
            st.markdown(f"The recent weighted estimate is **{forecast:.1f}%**. It summarises recent quiz percentages and is useful as a self-check, but it does not know about future question difficulty, study time, or external exam conditions.")
            if len(percentages) >= 2:
                if delta > 1:
                    st.success("Your latest result is higher than the previous attempt. Keep the practice routine consistent.")
                elif delta < -1:
                    st.warning("Your latest result dropped compared with the previous attempt. Review the answer explanations before retrying.")
                else:
                    st.info("Your latest result is broadly similar to the previous attempt. Target a module to make progress.")

    totals = {m: [0, 0] for m in MODULES}
    for item in history:
        detail = item.get("module_scores", {})
        for name, values in detail.items():
            if name in totals:
                totals[name][0] += int(values.get("correct", 0))
                totals[name][1] += int(values.get("total", 0))
        if not detail and item.get("module") in totals:
            name = item["module"]; totals[name][0] += int(item.get("score", 0)); totals[name][1] += int(item.get("total", 0))

    st.markdown("### Topic-level performance")
    assessed = []
    for name in MODULES:
        correct, total = totals[name]
        if total:
            pct = correct / total * 100
            band = "Strong" if pct >= 80 else "Developing" if pct >= 60 else "Needs practice"
            assessed.append((name, pct, total, band))
        else:
            pct, band = 0.0, "Not assessed"
        c1, c2, c3 = st.columns([2, 4, 1.5])
        c1.markdown(f"**{name}**")
        if total:
            c2.progress(pct / 100, text=f"{pct:.1f}% · {total} question(s)")
        else:
            c2.caption("Complete a quiz covering this module to measure progress.")
        c3.caption(band)
    if assessed:
        weakest = min(assessed, key=lambda row: row[1])
        st.markdown(f"**Suggested next step:** revise **{weakest[0]}** (current observed accuracy: {weakest[1]:.1f}%).")
        st.button("📖 Study recommended topic", key="insights_study_weakest", on_click=go, args=("learn", weakest[0]), type="primary")
    st.caption("Privacy note: quiz history is stored only in Streamlit session state for this browser session; closing/restarting the session can clear it.")


def dashboard():
    header("Learning Dashboard", "Choose a topic, refresh the key ideas, and then check your understanding with a quiz.")
    acc = accuracy(); c = st.columns(3)
    c[0].metric("📝 Quizzes taken", len(ss.history)); c[1].metric("🎯 Overall accuracy", "–" if acc is None else f"{acc:.0f}%"); c[2].metric("📚 Question bank", len(QUESTIONS))
    st.markdown("#### Topics")
    for r in range(0, len(MODULES), 3):
        for col, m in zip(st.columns(3), MODULES[r:r + 3]):
            with col: topic_card(m, "dash")
    st.button("⚡  Mixed Challenge — 20 Questions (20 min)", key="mixed_dash", on_click=start, args=(None, 20), type="primary")


def hub():
    header("Study & Practice Library", "Use concise notes, formulas, video resources, and topic quizzes to build confidence.")
    for r in range(0, len(MODULES), 3):
        for col, m in zip(st.columns(3), MODULES[r:r + 3]):
            with col: topic_card(m, "hub")


def learn():
    m = ss.module
    header(f"{m} — Study Material", STUDY[m]["tagline"])
    a, b, _ = st.columns([1, 1, 4])
    a.button("Take the quiz ▶", key="learn_quiz", on_click=start, args=(m, 10), type="primary")
    b.button("← Learning Hub", key="learn_back", on_click=go, args=("hub",))
    study_panel(m, "learn")


def options_html(q, chosen):
    out = []
    for k, o in enumerate(q["options"]):
        cls = "ok" if k == q["answer"] else "bad" if k == chosen else "dim"
        mark = "✔  " if k == q["answer"] else "✘  " if k == chosen else ""
        out.append(f"<div class='opt {cls}'>{mark}{esc(o)}</div>")
    return "".join(out)


def box(ax, x, y, w, t, hl=False):
    ax.add_patch(Rectangle((x, y), w, w, fc=CARD2, ec=PRI if hl else BORDER, lw=2))
    ax.text(x + w / 2, y + w / 2, t, color=PRI_L if hl else FG, ha="center", va="center", fontsize=16, fontweight="bold")


def draw_visual(v):
    fig = Figure(figsize=(5.4, 4.2), dpi=110, facecolor=CARD); ax = fig.add_subplot(111); ax.set_facecolor(CARD); k = v["kind"]
    if k == "pie":
        ax.pie(v["values"], labels=[f"{l}\n{x}%" for l, x in zip(v["labels"], v["values"])], startangle=90,
               colors=[PRI, ACCENT, WARN, "#C084FC", "#60A5FA"], textprops={"color": FG, "fontsize": 9}, wedgeprops={"edgecolor": CARD})
        ax.set_title(v["title"], color=FG, fontsize=11)
    elif k in ("bar", "line"):
        x = list(range(len(v["labels"]))); cols = [PRI, ACCENT]
        for n, (name, vals) in enumerate(v["series"].items()):
            if k == "bar": ax.bar_label(ax.bar([i + (n - .5) * .38 for i in x], vals, .38, label=name, color=cols[n]), color=FG, fontsize=8)
            else:
                ax.plot(x, vals, marker="o", label=name, color=cols[n], lw=2)
                for xi, yi in zip(x, vals): ax.annotate(str(yi), (xi, yi), textcoords="offset points", xytext=(0, 6), ha="center", color=FG, fontsize=8)
        ax.set_xticks(x); ax.set_xticklabels(v["labels"]); ax.set_ylabel(v["ylabel"], color=MUT); ax.tick_params(colors=MUT)
        ax.grid(axis="y", alpha=.15, color=MUT); ax.legend(facecolor=CARD, labelcolor=FG, edgecolor=CARD)
        for sp in ax.spines.values(): sp.set_color(BORDER)
        ax.set_title(v["title"], color=FG, fontsize=11)
    else:
        ax.set_axis_off(); ax.set_aspect("equal")
        if k == "seq":
            n = len(v["cells"])
            for i, t in enumerate(v["cells"]): box(ax, i * 1.1, 0, 1, t, t == "?")
            ax.set_xlim(-.1, n * 1.1); ax.set_ylim(-.3, 1.3)
        elif k == "matrix":
            R = len(v["rows"])
            for r, row in enumerate(v["rows"]):
                for i, t in enumerate(row): box(ax, i * 1.1, (R - 1 - r) * 1.1, 1, t, t == "?")
            ax.set_xlim(-.1, 3.4); ax.set_ylim(-.1, R * 1.1)
        else:   # rot: arrows rotated by the given angles, None = the unknown cell
            n = len(v["angles"])
            for i, a in enumerate(v["angles"]):
                box(ax, i * 1.2, 0, 1.1, "?" if a is None else "", a is None)
                if a is None: continue
                cx, cy, th = i * 1.2 + .55, .55, math.radians(a)
                pts = [(cx + (px * math.cos(th) - py * math.sin(th)) / 100, cy - (px * math.sin(th) + py * math.cos(th)) / 100) for px, py in ((0, -32), (16, 12), (0, 3), (-16, 12))]
                ax.add_patch(Polygon(pts, closed=True, fc=PRI, ec=FG, lw=1.5))
            ax.set_xlim(-.1, n * 1.2); ax.set_ylim(-.4, 1.5)
    fig.tight_layout(); st.pyplot(fig)


def timer_box():
    rem = ss.quiz.remaining() if ss.quiz else 0
    st.markdown(f"<div class='timer {'low' if rem < 60 else ''}'>⏱ {rem // 60:02d}:{rem % 60:02d}</div>", unsafe_allow_html=True)
    if rem == 0 and ss.page == "quiz": st.rerun()
if hasattr(st, "fragment"): timer_box = st.fragment(run_every=1)(timer_box)   # live countdown on newer Streamlit


def quiz_page():
    q = ss.quiz
    if q is None: go("home"); st.rerun()
    if q.remaining() == 0: finish(); st.rerun()
    cur = q.qs[q.i]; done = q.i in q.answers; last = q.i == len(q.qs) - 1; key = f"sel_{ss.qid}_{q.i}"
    h, t = st.columns([5, 1])
    with h: header(f"{q.module} Quiz", "Select an answer, then Submit to see the solution.")
    with t: timer_box()
    st.progress(q.i / len(q.qs))
    L, R = st.columns(2)
    with L, st.container(border=True):
        st.markdown(f"<span class='pill'>Q{q.i + 1} / {len(q.qs)}</span><span class='pill'>{esc(cur['module'])}</span><span class='pill'>{esc(cur['level'])}</span>"
                    f"<div class='q'>{esc(cur['question'])}</div>", unsafe_allow_html=True)
        if done:
            c = q.answers[q.i]; ok = c == cur["answer"]
            st.markdown(options_html(cur, c), unsafe_allow_html=True)
            st.markdown(f"<b style='color:{OK if ok else ERR}'>{'✔ Correct!' if ok else '✘ Incorrect'}</b><div class='sol'>Solution: {esc(cur['explanation'])}</div>", unsafe_allow_html=True)
            sel = None
        else:
            opts = cur["options"]
            sel = st.radio("Choose an answer", range(len(opts)), format_func=lambda k: opts[k].replace("$", "\\$"), index=None, key=key, label_visibility="collapsed")
        b1, b2, _ = st.columns([1, 1, 2])
        if b1.button("Submit", key=f"sub_{key}", type="primary", disabled=done or sel is None, use_container_width=True):
            q.answer(q.i, sel); st.rerun()
        if b2.button("Finish ✔" if last else "Next ▶", key=f"next_{key}", use_container_width=True):
            if not done and sel is not None: q.answer(q.i, sel)
            if last: finish()
            else: q.i += 1
            st.rerun()
        with st.expander("📖 Study notes for this topic"): study_panel(cur["module"], "quiz")
    with R, st.container(border=True):
        if cur["visual"]: draw_visual(cur["visual"])
        else: st.caption("No diagram for this question.")


def results():
    q = ss.quiz; n = len(q.qs); s = q.score(); acc = s / n
    header("Results", "Great work!" if acc >= .8 else "Good effort - review the topics below." if acc >= .5 else "Keep practising - study the notes, then retry.")
    A, B = st.columns([1, 2])
    with A, st.container(border=True):
        fig = Figure(figsize=(3.2, 3.2), dpi=110, facecolor=CARD); ax = fig.add_subplot(111); ax.set_facecolor(CARD)
        ax.pie([acc, 1 - acc], startangle=90, counterclock=False, colors=[OK if acc >= .6 else ERR, CARD2], wedgeprops=dict(width=.22, edgecolor=CARD))
        ax.text(0, .05, f"{acc * 100:.0f}%", color=FG, ha="center", va="center", fontsize=26, fontweight="bold")
        ax.text(0, -.3, "ACCURACY", color=MUT, ha="center", va="center", fontsize=8); fig.tight_layout(); st.pyplot(fig)
    with B, st.container(border=True):
        st.markdown(f"### Score: {s} / {n}")
        st.caption(f"Time spent: {q.elapsed // 60:02d}:{q.elapsed % 60:02d}  ·  Avg {q.elapsed / n:.0f}s per question")
        for m, (ok, tot) in q.by_module().items():
            c1, c2 = st.columns([4, 1]); c1.markdown(f"**{m}**   {ok}/{tot}"); c1.progress(ok / tot)
            if ok / tot < .6: c2.button("📖 Study this", key=f"weak_{m}", on_click=go, args=("learn", m))
        b = st.columns(4)
        b[0].button("Review answers", key="to_review", on_click=go, args=("review",), type="primary", use_container_width=True)
        b[1].button("Retry", key="retry", on_click=start, args=(None if q.module == "Mixed" else q.module, n), use_container_width=True)
        b[2].button("Dashboard", key="res_dash", on_click=go, args=("dash",), use_container_width=True)


def review():
    q = ss.quiz
    a, b = st.columns([4, 1])
    with a: header("Answer Review", "Revisit each question, compare your response with the correct answer, and read the solution.")
    b.button("← Results", key="rev_back", on_click=go, args=("results",))
    only = st.checkbox("Show only mistakes", key="only_wrong"); shown = 0
    for i, cur in enumerate(q.qs):
        got = q.answers.get(i); ok = q.correct(i)
        if only and ok: continue
        shown += 1
        with st.container(border=True):
            tag, col = ("CORRECT", OK) if ok else ("SKIPPED", WARN) if got is None else ("WRONG", ERR)
            st.markdown(f"<span class='pill' style='background:{col};color:#0A0F1E'>{tag}</span><span class='pill'>Q{i + 1} · {esc(cur['module'])} · {esc(cur['level'])}</span>"
                        f"<div class='q'>{esc(cur['question'])}</div>{options_html(cur, got)}<div class='sol'>Solution: {esc(cur['explanation'])}</div>", unsafe_allow_html=True)
    if not shown: st.success("🎉 No mistakes – perfect run!")


sidebar()
pages = {"home": home_page, "dash": dashboard, "hub": hub, "learn": learn, "insights": insights, "quiz": quiz_page, "results": results, "review": review}
pages.get(ss.page, home_page)()
