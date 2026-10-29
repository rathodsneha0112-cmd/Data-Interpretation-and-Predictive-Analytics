import tkinter as tk
from tkinter import ttk
import theme as T

class BaseScreen(tk.Frame):
    nav=None   # sidebar key to highlight (set by subclasses)
    def __init__(self,app,title,subtitle=""):
        super().__init__(app.content,bg=T.BG); self.app=app
        self.hdr=tk.Frame(self,bg=T.BG); self.hdr.pack(fill="x",padx=34,pady=(26,6))
        box=tk.Frame(self.hdr,bg=T.BG); box.pack(side="left")
        tk.Label(box,text=title,font=T.FH,fg=T.FG,bg=T.BG).pack(anchor="w")
        if subtitle: tk.Label(box,text=subtitle,font=T.F,fg=T.MUT,bg=T.BG).pack(anchor="w",pady=(2,0))
        self.body=tk.Frame(self,bg=T.BG); self.body.pack(fill="both",expand=True,padx=34,pady=(10,22))

class ScrollFrame(tk.Frame):
    """Vertically scrollable frame; put children in .inner."""
    def __init__(self,parent):
        super().__init__(parent,bg=T.BG)
        self.cv=tk.Canvas(self,bg=T.BG,highlightthickness=0); sb=ttk.Scrollbar(self.cv.master,orient="vertical",command=self.cv.yview)
        self.inner=tk.Frame(self.cv,bg=T.BG); self.win=self.cv.create_window((0,0),window=self.inner,anchor="nw")
        self.cv.configure(yscrollcommand=sb.set); self.cv.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")
        self.inner.bind("<Configure>",lambda e:self.cv.configure(scrollregion=self.cv.bbox("all")))
        self.cv.bind("<Configure>",lambda e:self.cv.itemconfig(self.win,width=e.width))
        ScrollFrame.live.append(self); self.bind("<Destroy>",lambda e:self in ScrollFrame.live and ScrollFrame.live.remove(self))
        if not ScrollFrame.wired:   # one app-wide wheel binding; scrolls whichever ScrollFrame is on screen
            ScrollFrame.wired=True
            for ev in ("<MouseWheel>","<Button-4>","<Button-5>"): self.bind_all(ev,ScrollFrame.wheel,add="+")
    live=[]; wired=False
    @staticmethod
    def wheel(e):
        d=-1 if (e.num==4 or getattr(e,"delta",0)>0) else 1
        for f in ScrollFrame.live:
            if f.cv.winfo_viewable(): f.cv.yview_scroll(d,"units"); break
