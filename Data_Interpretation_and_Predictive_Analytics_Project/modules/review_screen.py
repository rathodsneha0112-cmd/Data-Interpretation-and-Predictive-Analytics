import tkinter as tk
from tkinter import ttk
import theme as T
from modules.base_screen import BaseScreen, ScrollFrame

class ReviewScreen(BaseScreen):
    nav="dash"
    def __init__(self,app,quiz):
        super().__init__(app,"Review Answers","Every question with the correct answer and the worked solution."); self.q=quiz; self.only_wrong=tk.BooleanVar(value=False)
        T.link(self.hdr,"← Results",lambda:app.show_results(quiz),T.CARD2,T.BG).pack(side="right",padx=6)
        tk.Checkbutton(self.hdr,text="Show only mistakes",variable=self.only_wrong,command=self.draw,bg=T.BG,fg=T.FG,selectcolor=T.CARD2,
                       activebackground=T.BG,activeforeground=T.FG,font=T.F,bd=0,highlightthickness=0,cursor="hand2").pack(side="right",padx=10)
        self.sf=ScrollFrame(self.body); self.sf.pack(fill="both",expand=True); self.draw()
    def draw(self):
        for w in self.sf.inner.winfo_children(): w.destroy()
        shown=0
        for i,q in enumerate(self.q.qs):
            a=self.q.answers.get(i); ok=self.q.correct(i)
            if self.only_wrong.get() and ok: continue
            shown+=1; c=T.card(self.sf.inner); c.config(padx=22,pady=18); c.pack(fill="x",pady=7,padx=(0,12))
            top=tk.Frame(c,bg=T.CARD); top.pack(fill="x")
            T.badge(top,"CORRECT" if ok else ("SKIPPED" if a is None else "WRONG"),T.OK if ok else (T.WARN if a is None else T.ERR)).pack(side="left")
            T.label(top,f"  Q{i+1} · {q['module']} · {q['level']}",T.FS,T.MUT).pack(side="left")
            T.label(c,q["question"],(T.FAM,13,"bold"),wraplength=800,justify="left").pack(anchor="w",pady=(12,8))
            for k,o in enumerate(q["options"]):
                good=k==q["answer"]; bad=k==a and not good; col=T.OK if good else (T.ERR if bad else T.MUT); mark="✔  " if good else ("✘  " if bad else "     ")
                tk.Label(c,text=mark+o,font=T.F,fg=col,bg=T.OK_BG if good else T.ERR_BG if bad else T.CARD,anchor="w",padx=12,pady=5).pack(fill="x",pady=2)
            T.label(c,"Solution: "+q["explanation"],T.FS,T.MUT,wraplength=800,justify="left").pack(anchor="w",pady=(10,0))
        if not shown: T.label(self.sf.inner,"🎉 No mistakes – perfect run!",T.FT,T.OK,bg=T.BG).pack(pady=30)
