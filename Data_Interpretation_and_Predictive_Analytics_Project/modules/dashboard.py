import tkinter as tk
from tkinter import ttk
import theme as T
from quiz_engine import HISTORY
from questions import MODULES, QUESTIONS
from study import STUDY
from modules.base_screen import BaseScreen

def accuracy(module=None):
    h=[x for x in HISTORY if module in (None,x["module"])]; t=sum(x["total"] for x in h)
    return (sum(x["score"] for x in h)/t*100 if t else None)

class Dashboard(BaseScreen):
    nav="dash"
    def __init__(self,app):
        super().__init__(app,"Dashboard","Pick a topic: study it first, then take the quiz.")
        acc=accuracy(); row=tk.Frame(self.body,bg=T.BG); row.pack(fill="x")
        for k,(ic,t,v,col) in enumerate((("📝","Quizzes taken",len(HISTORY),T.PRI),("🎯","Overall accuracy","–" if acc is None else f"{acc:.0f}%",T.OK),("📚","Question bank",len(QUESTIONS),T.ACCENT))):
            c=T.card(row); c.grid(row=0,column=k,sticky="ew",padx=(0 if k==0 else 8,0 if k==2 else 8)); row.columnconfigure(k,weight=1,uniform="s")
            tk.Label(c,text=ic,font=(T.FAM,18),bg=T.CARD2,fg=col,width=3,pady=6).pack(side="left",padx=(0,14))
            col_=tk.Frame(c,bg=T.CARD); col_.pack(side="left")
            T.label(col_,t,T.FS,T.MUT).pack(anchor="w"); T.label(col_,str(v),(T.FAM,26,"bold"),T.FG).pack(anchor="w")
        tk.Label(self.body,text="Topics",font=T.FT,fg=T.FG,bg=T.BG).pack(anchor="w",pady=(22,4))
        grid=tk.Frame(self.body,bg=T.BG); grid.pack(fill="x")
        for k,m in enumerate(MODULES):
            s=STUDY[m]; c=T.card(grid); c.grid(row=k//3,column=k%3,sticky="nsew",padx=(0 if k%3==0 else 8,0 if k%3==2 else 8),pady=8); grid.columnconfigure(k%3,weight=1,uniform="g")
            top=tk.Frame(c,bg=T.CARD); top.pack(fill="x")
            tk.Frame(top,bg=s["color"],width=10,height=10).pack(side="left",padx=(0,8))
            T.label(top,m,T.FT).pack(side="left")
            a=accuracy(m); T.pill(top,"New" if a is None else f"{a:.0f}%",s["color"]).pack(side="right")
            T.label(c,s["tagline"],T.FS,T.MUT,wraplength=250,justify="left").pack(anchor="w",pady=(8,12))
            ttk.Progressbar(c,maximum=100,value=a or 0).pack(fill="x",pady=(0,14))
            b=tk.Frame(c,bg=T.CARD); b.pack(anchor="w")
            T.link(b,"📖 Study",lambda m=m:app.learn(m),T.CARD2).pack(side="left",padx=(0,6))
            for qn in (10,15): T.link(b,f"{qn} Q",lambda m=m,qn=qn:app.start(m,qn)).pack(side="left",padx=(0,6))
            T.hover_card(c,s["color"])
        ttk.Button(self.body,text="⚡  Mixed Challenge — 20 Questions (20 min)",command=lambda:app.start(None,20)).pack(anchor="w",pady=(14,0))
