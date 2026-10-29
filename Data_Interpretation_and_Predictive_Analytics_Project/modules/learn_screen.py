"""Learning Hub: topic grid (LearnHub) and per-topic study page (LearnScreen). LearnPanel is reused by the in-quiz study popup."""
import tkinter as tk, webbrowser, pathlib, html, urllib.parse
from tkinter import ttk
import theme as T
from study import STUDY
from questions import MODULES
from modules.base_screen import BaseScreen, ScrollFrame

GUIDES=pathlib.Path(__file__).resolve().parent.parent/"guides"

def open_video(q): webbrowser.open(q if q.startswith("http") else "https://www.youtube.com/results?search_query="+urllib.parse.quote_plus(q))

def open_guide(module):
    """Open guides/<module>.pdf if the user dropped one in; otherwise build a printable HTML cheat sheet from the notes."""
    pdf=GUIDES/STUDY[module].get("pdf",f"{module}.pdf")
    if pdf.exists(): return webbrowser.open(pdf.as_uri())
    s=STUDY[module]; li=lambda xs:"".join(f"<li>{html.escape(x)}</li>" for x in xs)
    rows="".join(f"<tr><td><b>{html.escape(a)}</b></td><td>{html.escape(b)}</td></tr>" for a,b in s["formulas"])
    page=(f"<html><head><meta charset='utf-8'><title>{module} cheat sheet</title><style>body{{font-family:Segoe UI,Arial;max-width:760px;margin:30px auto;line-height:1.5}}"
          f"td{{border:1px solid #ccc;padding:6px 10px}}table{{border-collapse:collapse}}h1{{color:{s['color']}}}</style></head><body><h1>{module} – Cheat Sheet</h1>"
          f"<p><i>{html.escape(s['tagline'])}</i></p><h2>Key notes</h2><ul>{li(s['notes'])}</ul><h2>Formulas</h2><table>{rows}</table>"
          f"<h2>Exam tips</h2><ul>{li(s['tips'])}</ul><p><small>Use your browser's Print → Save as PDF.</small></p></body></html>")
    GUIDES.mkdir(exist_ok=True); f=GUIDES/f"{module}_cheatsheet.html"; f.write_text(page,encoding="utf-8"); webbrowser.open(f.as_uri())

class LearnPanel(tk.Frame):
    """Tabbed Notes / Formulas / Videos for one module."""
    def __init__(self,parent,module,wrap=760):
        super().__init__(parent,bg=T.BG); s=STUDY[module]; nb=ttk.Notebook(self); nb.pack(fill="both",expand=True)
        def tab(name):
            sf=ScrollFrame(nb); nb.add(sf,text=name); return sf.inner
        n=tab("📝  Notes")
        for t in s["notes"]:
            r=T.card(n); r.pack(fill="x",pady=4,padx=4); r.config(pady=11)
            tk.Label(r,text="●",fg=s["color"],bg=T.CARD,font=T.FS).pack(side="left",anchor="n",padx=(0,12),pady=3)
            tk.Label(r,text=t,font=T.F,fg=T.FG,bg=T.CARD,wraplength=wrap-40,justify="left").pack(side="left",anchor="w")
        c=T.card(n); c.pack(fill="x",pady=14,padx=4); T.label(c,"💡 Exam tips",T.FB,s["color"]).pack(anchor="w")
        for t in s["tips"]: T.label(c,"• "+t,wraplength=wrap-30,justify="left").pack(anchor="w",pady=2)
        f=tab("➗  Formulas")
        for a,b in s["formulas"]:
            c=T.card(f); c.pack(fill="x",pady=5,padx=4); tk.Frame(c,bg=s["color"],width=4).pack(side="left",fill="y",padx=(0,12))
            col=tk.Frame(c,bg=T.CARD); col.pack(side="left",fill="x")
            T.label(col,a,T.FS,T.MUT).pack(anchor="w"); T.label(col,b,(T.MONO,12,"bold"),wraplength=wrap-60,justify="left").pack(anchor="w")
        v=tab("▶  Videos & PDF")
        T.label(v,"Opens YouTube in your browser.",T.FS,T.MUT,bg=T.BG).pack(anchor="w",padx=4,pady=(2,8))
        for title,desc,q in s["videos"]:
            c=T.card(v); c.pack(fill="x",pady=5,padx=4); tk.Label(c,text="▶",font=(T.FAM,20),fg=T.ERR,bg=T.CARD).pack(side="left",padx=(0,14))
            col=tk.Frame(c,bg=T.CARD); col.pack(side="left",fill="x",expand=True)
            T.label(col,title,T.FB).pack(anchor="w"); T.label(col,desc,T.FS,T.MUT,wraplength=wrap-200,justify="left").pack(anchor="w")
            T.link(c,"Watch",lambda q=q:open_video(q),T.ERR).pack(side="right")
        c=T.card(v); c.pack(fill="x",pady=(14,5),padx=4); tk.Label(c,text="📄",font=(T.FAM,20),bg=T.CARD,fg=T.FG).pack(side="left",padx=(0,14))
        col=tk.Frame(c,bg=T.CARD); col.pack(side="left",fill="x",expand=True)
        T.label(col,f"{module} cheat sheet / PDF guide",T.FB).pack(anchor="w")
        T.label(col,"Opens the PDF guide in your viewer."if(GUIDES/STUDY[module].get("pdf",f"{module}.pdf")).exists() else "Opens a printable cheat sheet (add a PDF to guides/ to replace it).",T.FS,T.MUT,wraplength=wrap-200,justify="left").pack(anchor="w")
        T.link(c,"Open",lambda:open_guide(module)).pack(side="right")

class LearnScreen(BaseScreen):
    nav="learn"
    def __init__(self,app,module):
        s=STUDY[module]; super().__init__(app,f"{module} — Study Material",s["tagline"])
        T.link(self.hdr,"← Learning Hub",app.learn,T.CARD2,T.BG).pack(side="right",padx=6)
        ttk.Button(self.hdr,text="Take the quiz ▶",command=lambda:app.start(module,10)).pack(side="right",padx=6)
        LearnPanel(self.body,module).pack(fill="both",expand=True)

class LearnHub(BaseScreen):
    nav="learn"
    def __init__(self,app):
        super().__init__(app,"Learning Hub","Read the notes, watch a lecture, then test yourself.")
        g=tk.Frame(self.body,bg=T.BG); g.pack(fill="x")
        for k,m in enumerate(MODULES):
            s=STUDY[m]; c=T.card(g); c.grid(row=k//3,column=k%3,sticky="nsew",padx=(0 if k%3==0 else 8,0 if k%3==2 else 8),pady=8); g.columnconfigure(k%3,weight=1,uniform="h")
            top=tk.Frame(c,bg=T.CARD); top.pack(fill="x"); tk.Frame(top,bg=s["color"],width=10,height=10).pack(side="left",padx=(0,8)); T.label(top,m,T.FT).pack(side="left")
            T.label(c,s["tagline"],T.FS,T.MUT,wraplength=250,justify="left").pack(anchor="w",pady=(8,12))
            pl=tk.Frame(c,bg=T.CARD); pl.pack(anchor="w",pady=(0,14))
            for txt in (f"{len(s['notes'])} notes",f"{len(s['formulas'])} formulas",f"{len(s['videos'])} videos"): T.pill(pl,txt,s["color"]).pack(side="left",padx=(0,6))
            b=tk.Frame(c,bg=T.CARD); b.pack(anchor="w")
            T.link(b,"📖 Study",lambda m=m:app.learn(m)).pack(side="left",padx=(0,6)); T.link(b,"Quiz ▶",lambda m=m:app.start(m,10),T.CARD2).pack(side="left"); T.hover_card(c,s["color"])
