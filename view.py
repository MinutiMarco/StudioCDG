import re,sys
p=sys.argv[1]; a=int(sys.argv[2]) if len(sys.argv)>2 else 0; b=int(sys.argv[3]) if len(sys.argv)>3 else 10**9
out=[]
for ln in open(p):
    s=ln.rstrip()
    if not s.strip(): continue
    if re.fullmatch(r"\[\[p\d+\]\]", s.strip()): continue
    if re.fullmatch(r"\d{1,4}", s.strip()): continue          # numeri di pagina
    if re.match(r"^\d+\\?_LIBRI", s.strip()): continue         # artefatti di composizione
    if re.fullmatch(r".{0,90}\d+\.(\d+\.)?", s.strip()): continue  # header/footer correnti
    if re.match(r"^\|", s): continue
    out.append(s)
# ricompone le righe spezzate in paragrafi
txt=[]; buf=""
for s in out:
    if re.match(r"^(\d+\.[\d.]*\s|Tavola |Figura |[-–•]\s|Obiettivi di |Sintesi dei |Parole chiave)", s) or s.isupper():
        if buf: txt.append(buf); buf=""
        txt.append(s)
    elif buf and not buf.endswith(('.',':',';','?','!')) and buf[-1:].islower():
        buf+=" "+s
    else:
        if buf: txt.append(buf)
        buf=s
if buf: txt.append(buf)
print("\n".join(txt[a:b]))
