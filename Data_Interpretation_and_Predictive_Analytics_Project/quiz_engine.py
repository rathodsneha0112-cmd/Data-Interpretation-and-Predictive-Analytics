import time, random
from questions import QUESTIONS
LIMITS={10:600,15:900,20:1200}   # seconds
HISTORY=[]

class Quiz:
    def __init__(self,module=None,n=10):
        pool=[q for q in QUESTIONS if module in (None,q["module"])]
        self.qs=random.sample(pool,min(n,len(pool))); self.limit=LIMITS.get(n,n*60)
        self.module=module or "Mixed"; self.answers={}; self.i=0; self.start=time.time(); self.elapsed=0; self.done=False
    def remaining(self): return max(0,int(self.limit-(time.time()-self.start)))
    def answer(self,i,c): self.answers[i]=c
    def correct(self,i): return self.answers.get(i)==self.qs[i]["answer"]
    def score(self): return sum(self.correct(i) for i in range(len(self.qs)))
    def by_module(self):
        d={}
        for i,q in enumerate(self.qs):
            a=d.setdefault(q["module"],[0,0]); a[1]+=1; a[0]+=self.correct(i)
        return d
    def finish(self):
        if self.done: return
        self.done=True; self.elapsed=min(self.limit,int(time.time()-self.start))
        HISTORY.append(dict(module=self.module,score=self.score(),total=len(self.qs),time=self.elapsed))
