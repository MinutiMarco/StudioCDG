import json,re,sys,os
def clean(raw_path, out_path):
    src = open(raw_path).read()
    try:
        t = json.loads(src)['fileContent']
    except Exception:
        t = src
    # accenti mal codificati dall'estrattore
    rep = {"e\\`":"è","a\\`":"à","u\\`":"ù","o\\`":"ò","i\\`":"ì","E\\`":"È","A\\`":"À","‘‘":"“","’’":"”"}
    for k,v in rep.items(): t = t.replace(k,v)
    t = re.sub(r"\\'","'",t)
    # rimuove i blocchi tabella dei marker di pagina
    t = re.sub(r"\|\s*\|\n\|\s*:-:\s*\|\n\|\s*\[\*\*Page (\d+)\*\*\]\(\)\s*\|", r"[[p\1]]", t)
    t = re.sub(r"^-{3,}$", "", t, flags=re.M)
    # footer editore
    t = re.sub(r"^\s*©?\s*Wolters Kluwer Italia.*$", "", t, flags=re.M)
    t = re.sub(r"\n{3,}", "\n\n", t)
    open(out_path,'w').write(t)
    return len(t)
if __name__=="__main__":
    print(clean(sys.argv[1], sys.argv[2]))
