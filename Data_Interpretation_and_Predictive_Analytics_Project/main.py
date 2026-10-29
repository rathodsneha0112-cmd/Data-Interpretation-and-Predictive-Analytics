import tkinter as tk
from tkinter import messagebox
import theme as T
from quiz_engine import Quiz
from modules.dashboard import Dashboard
from modules.quiz_screen import QuizScreen
from modules.results_screen import ResultsScreen
from modules.review_screen import ReviewScreen
from modules.learn_screen import LearnHub, LearnScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("DATA INTERPRETATION AND PREDICTIVE ANALYTICS"); self.geometry("1280x820"); self.minsize(1100,720); T.apply(self)
        sb=tk.Frame(self,bg=T.SIDE,width=240,highlightthickness=1,highlightbackground=T.BORDER); sb.pack(side="left",fill="y"); sb.pack_propagate(False)
        logo=tk.Frame(sb,bg=T.SIDE); logo.pack(fill="x",padx=22,pady=(28,26))
        tk.Label(logo,text="📊",font=(T.FAM,20),bg=T.PRI_D,fg="#FFFFFF",width=2).pack(side="left")
        tx=tk.Frame(logo,bg=T.SIDE); tx.pack(side="left",padx=12)
        tk.Label(tx,text="Data Interpretation",font=(T.FAM,10,"bold"),fg=T.FG,bg=T.SIDE).pack(anchor="w")
        tk.Label(tx,text="& Predictive Analytics",font=(T.FAM,9,"bold"),fg=T.PRI,bg=T.SIDE).pack(anchor="w")
        tk.Label(tx,text="Understand · Practise · Improve",font=(T.FAM,8),fg=T.MUT,bg=T.SIDE).pack(anchor="w")
        tk.Label(sb,text="MENU",font=(T.FAM,8,"bold"),fg=T.DIM,bg=T.SIDE).pack(anchor="w",padx=26,pady=(0,6))
        self.nav={}
        for key,t,cmd in (("dash","🏠   Dashboard",self.home),("learn","📚   Learning Hub",self.learn),
                          ("quiz","⚡   Mixed Practice (20)",lambda:self.start(None,20)),("about","ℹ️   About",self.about)):
            row=tk.Frame(sb,bg=T.SIDE); row.pack(fill="x",padx=12,pady=2)
            bar=tk.Frame(row,bg=T.SIDE,width=3); bar.pack(side="left",fill="y")
            b=tk.Button(row,text=t,command=cmd,bg=T.SIDE,fg=T.MUT,activebackground=T.CARD2,activeforeground=T.FG,relief="flat",anchor="w",
                        padx=14,pady=11,font=T.F,bd=0,cursor="hand2",highlightthickness=0); b.pack(side="left",fill="x",expand=True)
            b.bind("<Enter>",lambda e,b=b:b.config(bg=T.CARD2) if b["bg"]==T.SIDE else None); b.bind("<Leave>",lambda e,b=b:b.config(bg=T.SIDE) if b["bg"]==T.CARD2 and b["fg"]==T.MUT else None)
            self.nav[key]=(b,bar)
        tk.Label(sb,text="Logic & Data Interpretation – II",font=(T.FAM,8),fg=T.DIM,bg=T.SIDE).pack(side="bottom",pady=16)
        self.content=tk.Frame(self,bg=T.BG); self.content.pack(side="right",fill="both",expand=True); self.cur=None; self.home()
    def show(self,s):
        if self.cur: self.cur.destroy()
        self.cur=s; s.pack(fill="both",expand=True)
        for k,(b,bar) in self.nav.items(): on=k==s.nav; b.config(bg=T.CARD2 if on else T.SIDE,fg=T.FG if on else T.MUT,font=T.FB if on else T.F); bar.config(bg=T.PRI if on else T.SIDE)
    def home(self): self.show(Dashboard(self))
    def learn(self,module=None): self.show(LearnScreen(self,module) if module else LearnHub(self))
    def start(self,module,n): self.show(QuizScreen(self,Quiz(module,n)))
    def show_results(self,q): self.show(ResultsScreen(self,q))
    def review(self,q): self.show(ReviewScreen(self,q))
    def about(self): messagebox.showinfo("About","DATA INTERPRETATION AND PREDICTIVE ANALYTICS\nCourse: Logic and Data Interpretation II\nClass: TE / B · Artificial Intelligence and Data Science\nProfessor: Siddharth Machhindra Bhore\n\nPractise six topics, review worked solutions, and track quiz performance.")

if __name__=="__main__": App().mainloop()
