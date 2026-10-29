"""90 questions (6 modules x 15: 5 Easy, 5 Medium, 5 Hard). Every answer is computed in code from
seeded templates, so values and step-by-step solutions are mathematically consistent."""
import random, calendar, datetime as dt
from fractions import Fraction

MODULES=["Clock","Calendar","Pattern","Bar Graph","Pie Chart","Line Graph"]
LEVELS=["Easy"]*5+["Medium"]*5+["Hard"]*5
DAYS=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
def g(x): return "%g"%round(x,2)
def u(s): return lambda v:g(v)+s
R=lambda v:"₹"+f"{v:,.0f}"

def num(a,f):
    st=max(1,round(abs(a)*.1)); o=[a]
    for k in (1,-1,2,3,-2,4,5,-3):
        v=round(a+k*st,2)
        if v>=0 and v not in o: o.append(v)
        if len(o)==4: break
    return [f(v) for v in o]

def mk(r,mod,i,q,a,ex,f=str,pool=None,vis=None,opts=None):
    if opts is None: opts=[a]+r.sample([p for p in pool if p!=a],3) if pool else num(a,f)
    c=opts[0]; opts=list(opts); r.shuffle(opts)
    return dict(module=mod,level=LEVELS[i],question=q,options=opts,answer=opts.index(c),explanation=ex,visual=vis)

# ---------------- CLOCK ----------------
def ang(h,m):
    a=abs(30*h-5.5*m); return min(a,360-a)
def clock(i):
    r=random.Random(1000+i); f=u("°")
    if i<5:
        h=(i*3+r.randrange(3))%12+1; m=r.randrange(5,60,5); a=abs(30*h-5.5*m); ans=min(a,360-a)
        return mk(r,"Clock",i,f"What is the angle between the hour and minute hands at {h}:{m:02d}?",ans,
          f"Angle = |30h − 5.5m| = |30×{h} − 5.5×{m}| = {g(a)}°. Smaller angle = min({g(a)}, {g(360-a)}) = {g(ans)}°.",f)
    if i<10:
        if i%2:
            h=r.choice(range(1,11)); a=round(60*h/11,2)
            q=f"The hands of a clock coincide between {h} and {h+1} o'clock. How many minutes past {h} is that?"
            ex=f"Hands coincide when 5.5m = 30h → m = 60h/11 = 60×{h}/11 = {g(a)} min."
        else:
            h=r.choice([1,2,3,4,7,8,9,10,11]); a=round((30*h+180)/5.5 if h<5 else (30*h-180)/5.5,2)
            q=f"At what time (minutes past {h}) are the hands of a clock exactly opposite (180° apart) between {h} and {h+1} o'clock?"
            ex=f"Opposite hands: |30h − 5.5m| = 180 → m = {g(a)} min past {h}."
        return mk(r,"Clock",i,q,a,ex,u(" min"))
    lm=r.choice([5,10,12,15,20]); t=r.randrange(2,10); M=t*(60-lm); hh=(M//60)%12; mm=M%60; a=ang(hh,mm)
    return mk(r,"Clock",i,f"A clock loses {lm} minutes every hour and is set correctly at 12:00 noon. After {t} true hours, what is the angle between its hands?",a,
      f"In {t} h the clock advances {t}×(60−{lm}) = {M} min, so it shows {hh or 12}:{mm:02d}. Angle = |30×{hh} − 5.5×{mm}| = {g(abs(30*hh-5.5*mm))}° → smaller angle {g(a)}°.",f)

# ---------------- CALENDAR ----------------
def odd(d):
    N=d.year-1; c=N//100; cen=[0,5,3,1][c%4]; rr=N%100; yo=(rr+rr//4)%7; n=d.timetuple().tm_yday; t=(cen+yo+n)%7
    return DAYS[t],(f"Odd days: {c} century(ies) → {cen}; {rr} years → ({rr}+{rr//4}) mod 7 = {yo}; "
      f"days elapsed to {d:%d %b} = {n} ≡ {n%7}. Total = ({cen}+{yo}+{n%7}) mod 7 = {t} ⇒ {DAYS[t]} (0 = Sunday).")
def cal(i):
    r=random.Random(2000+i); M="Calendar"
    rd=lambda a,b:dt.date(r.randrange(a,b),1,1)+dt.timedelta(r.randrange(365))
    wd=lambda d:DAYS[d.isoweekday()%7]
    if i<3 or 10<=i<12:
        d=rd(1990,2031) if i<3 else rd(1601,2400); a,s=odd(d)
        return mk(r,M,i,f"What day of the week was {d:%d %B %Y}?",a,s,pool=DAYS)
    if i==3:
        Y=r.randrange(1950,2100); f=lambda y:y//4-y//100+y//400; a=f(Y)-f(1900)
        return mk(r,M,i,f"How many leap years lie between 1901 and {Y} (inclusive)?",a,
          f"Leap years ≤ Y = ⌊Y/4⌋ − ⌊Y/100⌋ + ⌊Y/400⌋. For {Y}: {f(Y)}; for 1900: {f(1900)}. Difference = {a}.")
    if i==4:
        n=r.randrange(8,40); a=str(n%7)
        return mk(r,M,i,f"How many odd days are there in {n} consecutive ordinary (non-leap) years?",a,
          f"Each ordinary year = 52 weeks + 1 odd day, so {n} years give {n} odd days ≡ {n%7} (mod 7).",pool=[str(x) for x in range(7)])
    if i<8:
        d=rd(2000,2031); k=r.randrange(100,900); a=wd(d+dt.timedelta(k))
        return mk(r,M,i,f"{d:%d %B %Y} is a {wd(d)}. What day of the week will it be after {k} days?",a,
          f"{k} = 7×{k//7} + {k%7}, so only {k%7} odd days matter: {wd(d)} + {k%7} = {a}.",pool=DAYS)
    if i==8:
        y=r.randrange(2000,2031); m=r.randrange(1,13); w=r.randrange(7); nd=calendar.monthrange(y,m)[1]
        c=sum(dt.date(y,m,k).isoweekday()%7==w for k in range(1,nd+1)); f1=dt.date(y,m,1)
        return mk(r,M,i,f"How many {DAYS[w]}s are there in {f1:%B %Y}?",str(c),
          f"The month has {nd} days = 4 weeks + {nd-28} extra day(s). 1st is a {wd(f1)}; counting {DAYS[w]}s gives {c}.",pool=["3","4","5","6"])
    if i==9:
        y=r.randrange(1996,2020); k=r.randrange(2,9); d0=dt.date(y,1,1); d1=dt.date(y+k,1,1); n=(d1-d0).days
        return mk(r,M,i,f"1 January {y} was a {wd(d0)}. What day will 1 January {y+k} be?",wd(d1),
          f"Days between = {n} ≡ {n%7} (mod 7). {wd(d0)} + {n%7} = {wd(d1)}.",pool=DAYS)
    if i==12:
        y=r.randrange(1990,2031); c=sum(dt.date(y,m,13).isoweekday()==5 for m in range(1,13))
        return mk(r,M,i,f"How many Friday-the-13ths occur in {y}?",str(c),
          f"Find the weekday of the 13th of each month using odd days; exactly {c} of them are Fridays in {y}.",pool=["1","2","3","4"])
    if i==13:
        d1=rd(2000,2020); d2=d1+dt.timedelta(r.randrange(200,1200)); a=(d2-d1).days
        return mk(r,M,i,f"How many days are there from {d1:%d %b %Y} to {d2:%d %b %Y} (start excluded, end included)?",a,
          f"Add remaining days of the start month, all full months between, and days of the final month (Feb has 29 days in leap years): total {a}.")
    y=r.randrange(1901,2090); y2=y+1
    while not(dt.date(y2,1,1).weekday()==dt.date(y,1,1).weekday() and calendar.isleap(y2)==calendar.isleap(y)): y2+=1
    return mk(r,M,i,f"The calendar of {y} is next repeated in which year?",None,
      f"A calendar repeats when 1 Jan falls on the same weekday and the leap status matches. Adding 1 odd day per ordinary year and 2 per leap year until the total ≡ 0 (mod 7) first happens in {y2}.",
      opts=[str(y2),str(y2-6),str(y2+5),str(y2+11)])

# ---------------- PATTERN (Canvas) ----------------
def pat(i):
    r=random.Random(3000+i); M="Pattern"
    if i<5:
        a=r.randrange(2,6); d=r.randrange(2,8); b=r.randrange(2,4)
        if i==0: s=[a+d*k for k in range(6)]; ex=f"Constant difference +{d}."
        elif i==1: s=[a*b**k for k in range(6)]; ex=f"Each term is multiplied by {b}."
        elif i==2: s=[k*k+a for k in range(1,7)]; ex=f"Terms follow n² + {a}."
        elif i==3:
            s=[a]
            for k in range(5): s.append(s[-1]+(d if k%2==0 else -1))
            ex=f"Alternately +{d} and −1."
        else:
            s=[a,d]
            for k in range(4): s.append(s[-1]+s[-2])
            ex="Each term is the sum of the previous two."
        return mk(r,M,i,"Find the missing number in the sequence drawn on the canvas.",s[5],f"{ex} Missing term = {s[5]}.",
          vis=dict(kind="seq",cells=[str(x) for x in s[:5]]+["?"]))
    if i<10:
        ops=[("a + b",lambda a,b:a+b),("a × b",lambda a,b:a*b),("a × b − a",lambda a,b:a*b-a),("a² + b",lambda a,b:a*a+b),("a×b + a + b",lambda a,b:a*b+a+b)]
        nm,fn=ops[i-5]; rows=[(x,y,fn(x,y)) for x,y in [(r.randrange(2,9),r.randrange(2,9)) for _ in range(3)]]
        rows_s=[[str(v) for v in row] for row in rows[:2]]+[[str(rows[2][0]),str(rows[2][1]),"?"]]
        return mk(r,M,i,"In the 3×3 number matrix, find the missing value.",rows[2][2],
          f"In every row, third = {nm} (a, b = first two numbers). Row 3: a={rows[2][0]}, b={rows[2][1]} → {rows[2][2]}.",vis=dict(kind="matrix",rows=rows_s))
    st=r.choice([30,45,60,90,120]); s0=r.randrange(0,360,30); an=[(s0+st*k)%360 for k in range(3)]; a=(s0+3*st)%360
    return mk(r,M,i,"Each tile rotates the arrow clockwise by a fixed angle. What is the orientation (degrees clockwise from 'up') of the missing arrow?",None,
      f"Tile angles {an[0]}°, {an[1]}°, {an[2]}° → rotation step = {st}°. Next = ({an[2]}+{st}) mod 360 = {a}°.",
      vis=dict(kind="rot",angles=an+[None]),opts=[f"{a}°",f"{(a+st)%360}°",f"{(a-st)%360}°",f"{(a+180)%360}°"])

# ---------------- BAR / LINE ----------------
def graph(i,kind,seed):
    r=random.Random(seed+i); M="Bar Graph" if kind=="bar" else "Line Graph"
    y0=r.randrange(2015,2020); L=[str(y0+k) for k in range(5)]
    A=r.sample(range(20,100,10),5); B=r.sample(range(20,100,10),5); sa,sb=sum(A),sum(B); y=r.randrange(4)
    pc=lambda a,b:(b-a)/a*100; ga=[round(pc(A[k],A[k+1]),1) for k in range(4)]; dB=[abs(B[k+1]-B[k]) for k in range(4)]
    Tg=sa//5+r.randrange(5,15); fr=Fraction(A[y],B[y]); tk_=" thousand"; nt=" (earliest year if tied)"
    vis=dict(kind=kind,title=("Production" if kind=="line" else "Sales")+" of two companies",labels=L,series={"Company X":A,"Company Y":B},ylabel="Thousand units")
    T=[
     (f"What was Company X's value in {L[y]}?",A[y],f"Read from the chart: {A[y]} thousand.",u(tk_),None),
     ("What is Company X's total over the five years?",sa,f"{'+'.join(map(str,A))} = {sa}.",u(tk_),None),
     ("In which year was Company X's value the highest?",L[A.index(max(A))],f"Highest value is {max(A)} in {L[A.index(max(A))]}.",None,L),
     (f"By how much does Company X differ from Company Y in {L[y]}?",abs(A[y]-B[y]),f"|{A[y]} − {B[y]}| = {abs(A[y]-B[y])}.",u(tk_),None),
     ("What is Company X's average value over the five years?",round(sa/5,2),f"{sa}/5 = {g(sa/5)}.",u(tk_),None),
     (f"What is the magnitude of the percentage change in Company X from {L[y]} to {L[y+1]}?",round(abs(pc(A[y],A[y+1])),1),
        f"Change = ({A[y+1]}−{A[y]})/{A[y]}×100 = {g(pc(A[y],A[y+1]))}% (magnitude shown).",u("%"),None),
     (f"What is the magnitude of the percentage change in Company Y from {L[y]} to {L[y+1]}?",round(abs(pc(B[y],B[y+1])),1),
        f"Change = ({B[y+1]}−{B[y]})/{B[y]}×100 = {g(pc(B[y],B[y+1]))}% (magnitude shown).",u("%"),None),
     (f"What is the ratio of Company X to Company Y in {L[y]}?",f"{fr.numerator}:{fr.denominator}",f"{A[y]}:{B[y]} simplifies to {fr.numerator}:{fr.denominator}.",None,
        ["1:1","2:1","3:2","1:2","2:3","3:1","4:3","3:4","5:2","1:3"]),
     (f"Company X's {L[y]} value is what percent of its five-year total?",round(A[y]/sa*100,1),f"{A[y]}/{sa}×100 = {g(A[y]/sa*100)}%.",u("%"),None),
     ("By how much does Company X's average differ from Company Y's average?",round(abs(sa-sb)/5,2),f"|{sa} − {sb}|/5 = {g(abs(sa-sb)/5)}.",u(tk_),None),
     (f"Which year shows the highest percentage growth for Company X over the previous year?{nt}",L[ga.index(max(ga))+1],f"Yearly % changes: {ga}. Largest is {max(ga)}%.",None,L),
     (f"What is the magnitude of the percentage change in the combined (X+Y) value from {L[0]} to {L[4]}?",round(abs((A[4]+B[4])/(A[0]+B[0])*100-100),1),
        f"Combined {A[0]+B[0]} → {A[4]+B[4]}; change = {g(((A[4]+B[4])/(A[0]+B[0])-1)*100)}% (magnitude shown).",u("%"),None),
     ("Company X's five-year total is what percent of Company Y's five-year total?",round(sa/sb*100,1),f"{sa}/{sb}×100 = {g(sa/sb*100)}%.",u("%"),None),
     (f"Company X's six-year average must be {Tg} thousand. What must its sixth-year value be?",6*Tg-sa,f"6×{Tg} − {sa} = {6*Tg-sa}.",u(tk_),None),
     (f"In which year did Company Y change the most (in absolute value) from the previous year?{nt}",L[dB.index(max(dB))+1],f"Absolute year-on-year changes: {dB}. Largest = {max(dB)}.",None,L),
    ]
    if kind=="line": T[3]=("In which year was Company Y's value the lowest?",L[B.index(min(B))],f"Lowest point of Company Y is {min(B)} in {L[B.index(min(B))]}.",None,L)
    q,a,ex,f,pool=T[i]
    return mk(r,M,i,q,a,ex,f or str,pool,vis)

# ---------------- PIE ----------------
def pie(i):
    r=random.Random(5000+i); cats=r.sample(["Rent","Food","Transport","Education","Savings","Health","Utilities","Leisure"],5)
    p=r.choice([[10,15,20,25,30],[5,15,20,25,35],[5,10,20,30,35],[5,10,15,30,40]]); r.shuffle(p)
    tot=r.choice([20000,40000,50000,80000,120000,200000]); y,z=r.sample(range(5),2); hi,lo=(y,z) if p[y]>p[z] else (z,y)
    val=lambda k:p[k]*tot//100; Y,Z,H,Lo=cats[y],cats[z],cats[hi],cats[lo]
    pr=Fraction(p[y],p[z]); mx,mn=p.index(max(p)),p.index(min(p)); sh=round(p[y]*1.2/(100+.2*p[y])*100,1)
    vis=dict(kind="pie",title=f"Monthly budget – total ₹{tot:,}",labels=cats,values=p)
    T=[
     (f"What is the central angle of the {Y} sector?",p[y]*3.6,f"{p[y]}% × 3.6 = {g(p[y]*3.6)}°.",u("°"),None),
     (f"How much money is allocated to {Y}?",val(y),f"{p[y]}% of {tot:,} = {val(y):,}.",R,None),
     ("Which category has the largest allocation?",cats[mx],f"{cats[mx]} has the biggest share ({p[mx]}%).",None,cats),
     (f"A sector has a central angle of {g(p[y]*3.6)}°. What percentage of the budget is it?",p[y],f"{g(p[y]*3.6)}/360 × 100 = {p[y]}%.",u("%"),None),
     ("What is the difference in money between the largest and smallest categories?",(max(p)-min(p))*tot//100,f"({max(p)}% − {min(p)}%) of {tot:,} = {(max(p)-min(p))*tot//100:,}.",R,None),
     (f"What is the combined central angle of {Y} and {Z}?",(p[y]+p[z])*3.6,f"({p[y]}+{p[z]})% × 3.6 = {g((p[y]+p[z])*3.6)}°.",u("°"),None),
     (f"What is the ratio of {Y} to {Z}?",f"{pr.numerator}:{pr.denominator}",f"{p[y]}:{p[z]} = {pr.numerator}:{pr.denominator}.",None,["1:1","2:1","3:2","1:2","2:3","3:1","4:3","3:4","5:2","1:3","7:2","6:1"]),
     (f"What is the combined amount for {Y} and {Z}?",val(y)+val(z),f"{val(y):,} + {val(z):,} = {val(y)+val(z):,}.",R,None),
     (f"{H} is what percent more than {Lo}?",round((p[hi]-p[lo])/p[lo]*100,1),f"({p[hi]}−{p[lo]})/{p[lo]}×100 = {g((p[hi]-p[lo])/p[lo]*100)}%.",u("%"),None),
     (f"If the total budget rises by 25% with the same shares, how much goes to {Y}?",val(y)*1.25,f"{val(y):,} × 1.25 = {g(val(y)*1.25)}.",R,None),
     (f"If spending on {Y} rises by 20% and the others stay the same, what is {Y}'s new percentage share?",sh,f"New value {g(p[y]*1.2)} out of {g(100+.2*p[y])} → {g(sh)}%.",u("%"),None),
     (f"By how many degrees is the combined angle of {Y} and {Z} different from the angle of all remaining sectors?",abs(2*(p[y]+p[z])-100)*3.6,
        f"|(p+q) − (100−p−q)|% × 3.6 = |{2*(p[y]+p[z])-100}|% × 3.6 = {g(abs(2*(p[y]+p[z])-100)*3.6)}°.",u("°"),None),
     (f"What is the total amount allocated to all categories except {Y}?",tot-val(y),f"{tot:,} − {val(y):,} = {tot-val(y):,}.",R,None),
     (f"If the amount for {Z} is cut by 40%, what is the new total budget?",round(tot-.4*val(z)),f"{tot:,} − 0.4×{val(z):,} = {round(tot-.4*val(z)):,}.",R,None),
     (f"The difference between {H} and {Lo} is {R(val(hi)-val(lo))}. What is the total budget?",tot,f"Difference = ({p[hi]}−{p[lo]})% of total = {R(val(hi)-val(lo))} → total = {tot:,}.",R,None),
    ]
    q,a,ex,f,pool=T[i]
    return mk(r,"Pie Chart",i,q,a,ex,f or str,pool,vis)

QUESTIONS=([clock(i) for i in range(15)]+[cal(i) for i in range(15)]+[pat(i) for i in range(15)]+
           [graph(i,"bar",4000) for i in range(15)]+[pie(i) for i in range(15)]+[graph(i,"line",6000) for i in range(15)])
for n,q in enumerate(QUESTIONS): q["id"]=n+1
