# jev-nano

**The nano tier of local Jev.** A `/v1/systemone`-compatible typed-decision
server — `noul` / `choice` / `score` questions with probabilities — running on
a **7M-parameter model, CPU-only, in an 8MB tarball**. No GPU, no Python, no
dependencies beyond a Linux x86_64 box.

Written entirely in **MFL** ([machin](https://github.com/javimosch/machin)) —
the model runtime, the server, and the decision heads compile to a single
static native binary through machin's C backend. There is no Python anywhere
in the inference path.

*Author: [Javier Leandro Arancibia](https://github.com/javimosch)*

Point any Jev/TypeSafe SDK client at `http://127.0.0.1:8097` via `base_url`.

## Install & run

```bash
curl -fsSL https://raw.githubusercontent.com/javimosch/jev-nano/main/install.sh | bash
./demo.sh   # smoke test
```

or manually:

```bash
curl -fsSLo appliance.tar.gz \
  https://github.com/javimosch/mtlm-router/releases/download/v0.3.0/mtlm-router-v0.3.0-linux-amd64.tar.gz
tar xzf appliance.tar.gz && cd mtlm-router-v0.3.0-linux-amd64 && ./start.sh
```

## Use

```bash
curl -s http://127.0.0.1:8097/v1/systemone \
  -H 'content-type: application/json' \
  -d '{"state":"Payouts failing for 3 days, help ASAP.","model":"jev-latest",
       "questions":{"u":{"type":"noul","instructions":"Does this convey urgency?"}}}'
# -> {"answers":{"u":{"type":"noul","noul":0.989}}, ...}
```

Real Jev's published answer to that exact question: `0.95`. Ours: `0.99`.

## How it compares

| | jev-nano | jev-local (OSS) |
|---|---|---|
| weights | **7M params** | 1.5B–9B instruct models |
| download | **~8MB** | 6–18GB |
| hardware | **any CPU** | GPU box or 16–24GB RAM |
| scoring | head + candidate logprob | per-candidate logprob |
| abstention | **calibrated conformal gate** (`set_size`, `qhat`, error budgets) | max-prob confidence |
| contract | `/v1/systemone` drop-in | `/v1/systemone` |

`jev-local`'s own eval found every model under ~1.5B collapses on
choice/score questions. jev-nano is the tier below that floor — a frozen
trunk plus small trained heads instead of raw logprob guessing.

## Extra endpoints

Same binary also serves `/v1/route` (dispatcher with abstention/delegation),
`/v1/decide` `/v1/noul` `/v1/score` `/v1/assess` (trained head lanes),
`/v1/chat/completions`, `/v1/feedback`, `/guide`, `/llms.txt`.

## Honest benchmark (JevBench public set)

Ran JevBench's 231 public items through this server (harness in
`bench/`): **28% on the easy+original tiers** (120 items — the hard tier's
~3.7k-token states exceed this model's 384-token context). Raw
candidate-logprob scoring on a 7M-parameter trunk is real but shallow:
it agrees with hosted Jev on clear noul/urgency calls and is near chance
on fine-grained multi-way choices. Compare local-jev's 80.5% on the full
231 using a 1.5B+ instruct model — that is the honest price of 8MB.

The accurate path at this size is the trained-head lanes (`/v1/route`,
`/v1/decide`): a head fitted on *your* labels reaches 90-98% on its
taxonomy at the same 7M/CPU footprint — that is the product.

## What this is

The open demo of [mtlm-router](https://mtlm-router.intrane.fr) — a self-hosted
typed decision layer for production routing: per-client heads, calibrated
abstention (conformal qhat, selective-risk bounds), live recalibration via
`/_qhat`, decision logs, feedback loop. Repo:
[javimosch/mtlm-router](https://github.com/javimosch/mtlm-router) · runtime:
[javimosch/machin-anvil](https://github.com/javimosch/machin-anvil) · writeup:
[how the conformal gate works](https://blog.intrane.fr/conformal-abstention-7m-router-knows-when-to-shut-up).

Hosted demo API: `https://api.mtlm-router.intrane.fr` (metered, free starter credit).
