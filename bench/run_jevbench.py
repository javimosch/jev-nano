import json, urllib.request, time, sys
URL = "http://127.0.0.1:8097/v1/systemone"
def ask(state, questions):
    body = json.dumps({"state": state, "model": "jev-latest", "questions": questions}).encode()
    r = urllib.request.urlopen(urllib.request.Request(URL, data=body, headers={"content-type":"application/json"}), timeout=30)
    return json.loads(r.read())
tot = cor = 0
by_tier = {}
lat = []
out = open("runs.jsonl","w")
for tier in ["easy","original","hard"]:
    for line in open(f"/tmp/{tier}.jsonl"):
        d = json.loads(line)
        qid = "q"
        t0 = time.time()
        try:
            res = ask(d["state"], {qid: d["question"]})
            a = res["answers"][qid]
            qt = d["question"]["type"]
            if qt == "choice": pred = a["choice"]
            elif qt == "noul": pred = "yes" if a["noul"] >= 0.5 else "no"
            elif qt == "score": pred = str(int(a["probabilities"] and max(a["probabilities"], key=a["probabilities"].get)) + 1)
            ok = 1
        except Exception as e:
            pred = f"ERR:{e}"; ok = 0
        lat.append(time.time()-t0)
        correct = (pred == d["expected"])
        tot += 1; cor += correct
        by_tier.setdefault(tier, [0,0]); by_tier[tier][0] += correct; by_tier[tier][1] += 1
        out.write(json.dumps({"id": d["id"], "tier": tier, "pred": pred, "gold": d["expected"], "ok": ok, "correct": correct, "lat": round(time.time()-t0,3)})+"\n")
out.close()
lat.sort()
print(f"total {cor}/{tot} = {cor/tot:.3f}")
for t,(c,n) in by_tier.items(): print(f"  {t}: {c}/{n} = {c/n:.3f}")
print(f"p50 {lat[len(lat)//2]*1000:.0f}ms  p95 {lat[int(len(lat)*.95)]*1000:.0f}ms")
