import tkinter as tk, math
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import theme as T
from modules.base_screen import BaseScreen
from modules.learn_screen import LearnPanel
from study import STUDY

class QuizScreen(BaseScreen):
    def __init__(self,app,quiz):
        self.nav="quiz" if quiz.module=="Mixed" else "dash"   # sidebar highlight
        super().__init__(app,f"{quiz.module} Quiz","Select an answer, then Submit to see the solution."); self.pop=None
        self.q=quiz; self.var=tk.IntVar(value=-1); self.locked=False; self.fc=None; self.fig=None; self.job=None
        self.timer=tk.Label(self.hdr,font=(T.MONO,15,"bold"),fg=T.PRI_L,bg=T.CARD,padx=16,pady=7,highlightthickness=1,highlightbackground=T.BORDER); self.timer.pack(side="right")
        T.link(self.hdr,"📖 Study notes",self.study,T.CARD2,T.BG).pack(side="right",padx=16)
        self.prog=ttk.Progressbar(self.body,maximum=len(quiz.qs)); self.prog.pack(fill="x",pady=(0,14))
        row=tk.Frame(self.body,bg=T.BG); row.pack(fill="both",expand=True); row.rowconfigure(0,weight=1)
        row.columnconfigure(0,weight=1,uniform="a"); row.columnconfigure(1,weight=1,uniform="a")
        L=T.card(row); L.config(padx=24,pady=22); L.grid(row=0,column=0,sticky="nsew",padx=(0,10))
        self.vis=T.card(row); self.vis.grid(row=0,column=1,sticky="nsew",padx=(10,0))
        self.meta=T.pill(L,"",T.PRI_L,T.CARD2); self.meta.pack(anchor="w")
        self.qt=T.label(L,"",(T.FAM,14,"bold"),wraplength=400,justify="left"); self.qt.pack(anchor="w",pady=(14,14))
        self.rb=[]
        for k in range(4):
            b=tk.Radiobutton(L,variable=self.var,value=k,indicatoron=0,font=T.F,fg=T.FG,bg=T.CARD2,selectcolor="#2C3180",activebackground=T.HOVER,
                activeforeground=T.FG,disabledforeground=T.FG,anchor="w",justify="left",wraplength=400,padx=16,pady=10,bd=0,relief="flat",offrelief="flat",
                overrelief="flat",highlightthickness=1,highlightbackground=T.BORDER,highlightcolor=T.PRI,cursor="hand2",command=self.mark)
            b.pack(fill="x",pady=4); self.rb.append(b)
            b.bind("<Enter>",lambda e,k=k:self.rb[k]["state"]=="normal" and self.var.get()!=k and self.rb[k].config(bg=T.HOVER))
            b.bind("<Leave>",lambda e,k=k:self.rb[k]["state"]=="normal" and self.var.get()!=k and self.rb[k].config(bg=T.CARD2))
        bar=tk.Frame(L,bg=T.CARD); bar.pack(fill="x",pady=(14,10))
        self.sub=ttk.Button(bar,text="Submit",command=self.submit); self.sub.pack(side="left")
        self.nxt=ttk.Button(bar,text="Next ▶",style="Ghost.TButton",command=self.next); self.nxt.pack(side="left",padx=8)
        self.fb=T.label(L,"",T.FB); self.fb.pack(anchor="w")
        self.ex=T.label(L,"",fg=T.MUT,wraplength=400,justify="left"); self.ex.pack(anchor="w",pady=4)
        self.load(); self.tick()

    def load(self):
        q=self.q.qs[self.q.i]; self.locked=False; self.var.set(-1); self.prog["value"]=self.q.i
        self.meta.config(text=f"  Q{self.q.i+1} / {len(self.q.qs)}  ·  {q['module']}  ·  {q['level']}  ")
        self.qt.config(text=q["question"]); self.fb.config(text=""); self.ex.config(text="")
        for b,o in zip(self.rb,q["options"]): b.config(text=o,bg=T.CARD2,selectcolor="#2C3180",highlightbackground=T.BORDER,state="normal")
        self.sub.state(["!disabled"]); self.nxt.config(text="Finish ✔" if self.q.i==len(self.q.qs)-1 else "Next ▶")
        self.clear_vis(); v=q["visual"]
        if v: (self.canvas if v["kind"] in ("seq","matrix","rot") else self.chart)(v)

    def mark(self):
        """Highlight the chosen option with an accent border."""
        for k,b in enumerate(self.rb): b.config(highlightbackground=T.PRI if self.var.get()==k else T.BORDER,bg=T.CARD2)

    def submit(self):
        c=self.var.get()
        if self.locked or c<0: return
        self.locked=True; q=self.q.qs[self.q.i]; self.q.answer(self.q.i,c)
        for k,b in enumerate(self.rb):
            b.config(state="disabled")
            if k==q["answer"]: b.config(bg=T.OK_BG,selectcolor=T.OK_BG,highlightbackground=T.OK)
            elif k==c: b.config(bg=T.ERR_BG,selectcolor=T.ERR_BG,highlightbackground=T.ERR)
            else: b.config(fg=T.MUT,disabledforeground=T.MUT,highlightbackground=T.BORDER)
        ok=c==q["answer"]; self.fb.config(text="✔ Correct!" if ok else "✘ Incorrect",fg=T.OK if ok else T.ERR)
        self.ex.config(text="Solution: "+q["explanation"]); self.sub.state(["disabled"])

    def next(self):
        if not self.locked and self.var.get()>=0: self.submit(); return
        if self.q.i==len(self.q.qs)-1: self.finish()
        else: self.q.i+=1; self.load()

    def finish(self):
        self.stop()
        if not self.locked and self.var.get()>=0: self.q.answer(self.q.i,self.var.get())
        self.q.finish(); self.app.show_results(self.q)

    def tick(self):
        rem=self.q.remaining(); self.timer.config(text=f"⏱ {rem//60:02d}:{rem%60:02d}",fg=T.ERR if rem<60 else T.PRI_L)
        if rem==0: self.finish()
        else: self.job=self.after(500,self.tick)

    def stop(self):
        if self.job: self.after_cancel(self.job); self.job=None
        self.clear_vis()

    def study(self):
        """Popup with the notes for the current question's topic (timer keeps running)."""
        m=self.q.qs[self.q.i]["module"]
        if self.pop and self.pop.winfo_exists(): self.pop.destroy()
        w=self.pop=tk.Toplevel(self.app); w.title(f"{m} — Study notes"); w.geometry("820x600"); w.configure(bg=T.BG)
        tk.Label(w,text=f"{m} — {STUDY[m]['tagline']}",font=T.FT,fg=STUDY[m]["color"],bg=T.BG).pack(anchor="w",padx=18,pady=(14,6))
        LearnPanel(w,m,wrap=700).pack(fill="both",expand=True,padx=18,pady=(0,14))

    def destroy(self):
        self.stop()
        if self.pop and self.pop.winfo_exists(): self.pop.destroy()
        super().destroy()

    def clear_vis(self):
        if self.fig is not None: self.fig.clear()
        self.fig=None; self.fc=None
        for w in self.vis.winfo_children(): w.destroy()

    def canvas(self,s):
        c=tk.Canvas(self.vis,width=500,height=330,bg=T.CARD,highlightthickness=0); c.pack(expand=True)
        def box(x,y,w,t,hl=False):
            c.create_rectangle(x,y,x+w,y+w,outline=T.PRI if hl else T.BORDER,width=2,fill=T.CARD2)
            c.create_text(x+w/2,y+w/2,text=t,fill=T.PRI_L if hl else T.FG,font=(T.FAM,18,"bold"))
        if s["kind"]=="seq":
            n=len(s["cells"]); w=72; x0=(500-n*w-(n-1)*6)//2
            for k,t in enumerate(s["cells"]): box(x0+k*(w+6),130,w,t,t=="?")
        elif s["kind"]=="matrix":
            for r,row in enumerate(s["rows"]):
                for k,t in enumerate(row): box(110+k*92,25+r*92,84,t,t=="?")
        else:
            n=len(s["angles"]); w=108; x0=(500-n*w)//2
            for k,a in enumerate(s["angles"]):
                x=x0+k*w; box(x+4,110,w-8,"?" if a is None else "",a is None)
                if a is None: continue
                cx,cy=x+w/2,110+(w-8)/2; th=math.radians(a); pts=[]
                for px,py in ((0,-32),(16,12),(0,3),(-16,12)):
                    pts+=[cx+px*math.cos(th)-py*math.sin(th),cy+px*math.sin(th)+py*math.cos(th)]
                c.create_polygon(pts,fill=T.PRI,outline=T.FG,width=2)

    def chart(self,s):
        fig=Figure(figsize=(5.2,4),dpi=100,facecolor=T.CARD); ax=fig.add_subplot(111); ax.set_facecolor(T.CARD)
        if s["kind"]=="pie":
            ax.pie(s["values"],labels=[f"{l}\n{v}%" for l,v in zip(s["labels"],s["values"])],startangle=90,
                colors=[T.PRI,T.OK,T.WARN,"#F472B6",T.ACCENT],textprops={"color":T.FG,"fontsize":9},wedgeprops={"edgecolor":T.CARD})
        else:
            x=np.arange(len(s["labels"])); cols=[T.PRI,T.WARN]
            for n,(k,v) in enumerate(s["series"].items()):
                if s["kind"]=="bar": ax.bar_label(ax.bar(x+(n-.5)*.38,v,.38,label=k,color=cols[n]),color=T.FG,fontsize=8)
                else:
                    ax.plot(x,v,marker="o",label=k,color=cols[n],lw=2)
                    for xi,yi in zip(x,v): ax.annotate(str(yi),(xi,yi),textcoords="offset points",xytext=(0,6),ha="center",color=T.FG,fontsize=8)
            ax.set_xticks(x); ax.set_xticklabels(s["labels"]); ax.set_ylabel(s["ylabel"],color=T.MUT); ax.tick_params(colors=T.MUT)
            ax.grid(axis="y",alpha=.15,color=T.MUT); ax.legend(facecolor=T.CARD,labelcolor=T.FG,edgecolor=T.CARD)
            for sp in ax.spines.values(): sp.set_color(T.BORDER)
        ax.set_title(s["title"],color=T.FG,fontsize=11); fig.tight_layout()
        self.fig=fig; self.fc=FigureCanvasTkAgg(fig,self.vis); self.fc.get_tk_widget().pack(fill="both",expand=True); self.fc.draw()
