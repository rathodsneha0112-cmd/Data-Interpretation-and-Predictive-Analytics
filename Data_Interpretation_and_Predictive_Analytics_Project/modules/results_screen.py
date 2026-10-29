import tkinter as tk
from tkinter import ttk
import theme as T
from modules.base_screen import BaseScreen

class ResultsScreen(BaseScreen):
    nav="dash"
    def __init__(self,app,quiz):
        n=len(quiz.qs); s=quiz.score(); acc=s/n
        super().__init__(app,"Results","Great work!" if acc>=.8 else "Good effort - review the topics below." if acc>=.5 else "Keep practising - study the notes, then retry.")
        row=tk.Frame(self.body,bg=T.BG); row.pack(fill="x")
        a=T.card(row); a.config(padx=26,pady=26); a.pack(side="left",fill="y",padx=(0,12))
        c=tk.Canvas(a,width=220,height=220,bg=T.CARD,highlightthickness=0); c.pack()
        c.create_arc(20,20,200,200,start=0,extent=359.9,style="arc",width=18,outline=T.CARD2)
        if acc>0: c.create_arc(20,20,200,200,start=90,extent=-359.9*acc,style="arc",width=18,outline=T.OK if acc>=.6 else T.ERR)
        c.create_text(110,100,text=f"{acc*100:.0f}%",fill=T.FG,font=T.FBIG); c.create_text(110,136,text="ACCURACY",fill=T.MUT,font=(T.FAM,9,"bold"))
        b=T.card(row); b.config(padx=26,pady=22); b.pack(side="left",fill="both",expand=True)
        T.label(b,f"Score: {s} / {n}",(T.FAM,20,"bold")).pack(anchor="w")
        T.label(b,f"Time spent: {quiz.elapsed//60:02d}:{quiz.elapsed%60:02d}  ·  Avg {quiz.elapsed/n:.0f}s per question",fg=T.MUT).pack(anchor="w",pady=(2,12))
        for m,(ok,tot) in quiz.by_module().items():
            r=tk.Frame(b,bg=T.CARD); r.pack(fill="x",pady=(0,6)); T.label(r,f"{m}   {ok}/{tot}").pack(side="left")
            if ok/tot<.6: T.link(r,"📖 Study this",lambda m=m:app.learn(m),T.WARN).pack(side="right")
            ttk.Progressbar(b,maximum=tot,value=ok).pack(fill="x",pady=(0,8))
        bt=tk.Frame(b,bg=T.CARD); bt.pack(anchor="w",pady=(16,4))
        ttk.Button(bt,text="Review answers",command=lambda:app.review(quiz)).pack(side="left")
        ttk.Button(bt,text="Retry",style="Ghost.TButton",command=lambda:app.start(None if quiz.module=="Mixed" else quiz.module,len(quiz.qs))).pack(side="left",padx=8)
        ttk.Button(bt,text="Dashboard",style="Ghost.TButton",command=app.home).pack(side="left")
