import tkinter as tk
from tkinter import ttk, font as tkfont

# ---- palette (light neutral surfaces, teal primary, amber accent) ----
BG="#F4F7FA"; SIDE="#E7F2F0"; CARD="#FFFFFF"; CARD2="#EAF3F2"; HOVER="#D8ECE8"; BORDER="#D5E2E6"
PRI="#0F766E"; PRI_D="#0B5F59"; PRI_L="#115E59"; ACCENT="#F59E0B"
OK="#15803D"; ERR="#B91C1C"; WARN="#B45309"
FG="#1F2937"; MUT="#64748B"; DIM="#94A3B8"
OK_BG="#DCFCE7"; ERR_BG="#FEE2E2"   # tinted fills for answered options

# ---- fonts: first installed family wins (Segoe UI on Windows, SF on macOS, Inter/Ubuntu on Linux) ----
FAM="Segoe UI"; MONO="Consolas"
F=(FAM,11); FS=(FAM,10); FB=(FAM,12,"bold"); FH=(FAM,24,"bold"); FT=(FAM,14,"bold"); FBIG=(FAM,30,"bold")

def _fonts():
    global FAM,MONO,F,FS,FB,FH,FT,FBIG
    have=set(tkfont.families())
    FAM=next((f for f in ("Segoe UI Variable Text","Segoe UI","SF Pro Text","Helvetica Neue","Inter","Ubuntu","Cantarell","DejaVu Sans") if f in have),"TkDefaultFont")
    MONO=next((f for f in ("Cascadia Code","Consolas","SF Mono","Menlo","DejaVu Sans Mono") if f in have),"TkFixedFont")
    F=(FAM,11); FS=(FAM,10); FB=(FAM,12,"bold"); FH=(FAM,24,"bold"); FT=(FAM,14,"bold"); FBIG=(FAM,30,"bold")

def apply(root):
    _fonts(); root.configure(bg=BG); s=ttk.Style(root); s.theme_use("clam")
    s.configure("TButton",background=PRI_D,foreground="#FFFFFF",font=FB,borderwidth=0,focuscolor=PRI_D,padding=(18,10))
    s.map("TButton",background=[("disabled",CARD2),("active",PRI),("pressed",PRI)],foreground=[("disabled",DIM)])
    s.configure("Ghost.TButton",background=CARD2,foreground=FG,font=FB,borderwidth=0,focuscolor=CARD2,padding=(18,10))
    s.map("Ghost.TButton",background=[("active",HOVER),("pressed",HOVER)])
    s.configure("Horizontal.TProgressbar",background=PRI,troughcolor=CARD2,bordercolor=CARD2,borderwidth=0,lightcolor=PRI,darkcolor=PRI,thickness=8)
    s.configure("TNotebook",background=BG,borderwidth=0,bordercolor=BG,lightcolor=BG,darkcolor=BG,tabmargins=(0,0,0,10)); s.configure("TNotebook.Tab",background=BG,foreground=MUT,font=FB,padding=(18,9),borderwidth=0,bordercolor=BG,lightcolor=BG,darkcolor=BG,focuscolor=BG)
    s.map("TNotebook.Tab",background=[("selected",CARD2),("active",CARD)],foreground=[("selected",FG),("active",FG)])
    s.layout("TNotebook.Tab",[("Notebook.tab",{"sticky":"nswe","children":[("Notebook.padding",{"sticky":"nswe","children":[("Notebook.label",{"sticky":""})]})]})])
    s.layout("Vertical.TScrollbar",[("Vertical.Scrollbar.trough",{"sticky":"ns","children":[("Vertical.Scrollbar.thumb",{"expand":"1","sticky":"nswe"})]})])
    s.configure("Vertical.TScrollbar",background=CARD2,troughcolor=BG,borderwidth=0,bordercolor=BG,lightcolor=CARD2,darkcolor=CARD2,gripcount=0,relief="flat",width=10)
    s.map("Vertical.TScrollbar",background=[("active",HOVER)])

def card(parent,bg=CARD,**kw):
    """Surface with a 1px soft border."""
    return tk.Frame(parent,bg=bg,padx=18,pady=16,highlightthickness=1,highlightbackground=BORDER,highlightcolor=BORDER,**kw)
def label(parent,text,font=None,fg=FG,bg=CARD,**kw): return tk.Label(parent,text=text,font=font or F,fg=fg,bg=bg,**kw)

def hover_card(c,color):
    """Border lights up in the topic colour while the pointer is over the card (or any child)."""
    def on(_=None): c.config(highlightbackground=color,highlightcolor=color)
    def off(_=None):
        w=c.winfo_containing(*c.winfo_pointerxy())
        if w is None or not str(w).startswith(str(c)): c.config(highlightbackground=BORDER,highlightcolor=BORDER)
    def wire(w):
        w.bind("<Enter>",on,add="+"); w.bind("<Leave>",off,add="+")
        for k in w.winfo_children(): wire(k)
    wire(c)

def link(parent,text,cmd,color=PRI_D,bg=CARD):
    """Flat button with hover. `color` is the resting fill; secondary buttons pass CARD2."""
    hov={PRI_D:PRI,CARD2:HOVER,WARN:"#FCD34D",ERR:"#FCA5A5"}.get(color,PRI)
    fg="#1A1205" if color==WARN else "#FFFFFF" if color!=CARD2 else FG
    b=tk.Button(parent,text=text,command=cmd,bg=color,fg=fg,activebackground=hov,activeforeground=fg,relief="flat",bd=0,
                font=(FAM,10,"bold"),padx=14,pady=6,cursor="hand2",highlightthickness=0)
    b.bind("<Enter>",lambda e:b.config(bg=hov)); b.bind("<Leave>",lambda e:b.config(bg=color)); return b

def badge(parent,text,color):
    return tk.Label(parent,text=f"  {text}  ",font=(FAM,9,"bold"),fg="#0A0F1E",bg=color,pady=2)

def pill(parent,text,color=PRI_L,bg=CARD2):
    return tk.Label(parent,text=f"  {text}  ",font=(FAM,9,"bold"),fg=color,bg=bg,pady=3)
