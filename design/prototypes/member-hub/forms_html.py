"""Render the Hub's mentoring forms word for word from fixtures/forms/*.json, for the guide pages."""
import html, json, sys
F = "/home/claude/cnap-platform/fixtures/forms/"
SCALE = ["1 - Strongly Disagree", "2 - Disagree", "3 - Neither Agree nor Disagree", "4 - Agree", "5 - Strongly Agree", "Not Applicable"]
e = html.escape

def form(code, summary_small, open_=False, note=""):
    d = json.load(open(F + code + ".json"))
    out = [f'<details class="form"{" open" if open_ else ""}>',
           f'  <summary><span>{e(d["name"])}<small>{summary_small}</small></span></summary>',
           '  <div class="form-b">']
    for p in d.get("display", {}).get("about", []):
        out.append(f'    <p>{e(p)}</p>')
    pre = d.get("display", {}).get("prefill")
    if pre:
        out.append('    <p class="meta">Filled in for you: ' + e(", ".join(x[0] for x in pre)) + '.</p>')
    for s in d["sections"]:
        qs = s["questions"]
        likert = [q for q in qs if q["type"] == "likert"]
        out.append(f'    <h4 class="fq-h">{e(s.get("title",""))}</h4>')
        if s.get("instructions"):
            out.append(f'    <p class="meta">{e(s["instructions"])}</p>')
        if likert:
            out.append('    <p class="fq-scale">Answered on this scale: ' + " · ".join(e(x) for x in SCALE) + '</p>')
            out.append('    <ol class="fq">')
            for q in likert:
                out.append(f'      <li>{e(q["prompt"])}</li>')
            out.append('    </ol>')
        rest = [q for q in qs if q["type"] != "likert"]
        if rest:
            out.append('    <ul class="fq-open">')
            for q in rest:
                kind = {"date": "Date", "long_text": "Written answer"}.get(q["type"], "Answer")
                h = f'<span>{e(q["help_text"])}</span>' if q.get("help_text") else ""
                out.append(f'      <li><b>{e(q["prompt"])}</b> <em>{kind}{", optional" if q.get("required") is False else ""}</em>{h}</li>')
            out.append('    </ul>')
    if note:
        out.append(f'    {note}')
    out.append('  </div>')
    out.append('</details>')
    return "\n".join(out)

open_link = '<p class="fq-link"><a href="index.html#wk">Open it in My work</a><span class="meta"> In the Hub, this opens the form itself as a read-only preview, from your reporting.</span></p>'
pieces = {
  "mentor_q": form("mentor_questionnaire", "About 10 minutes · 19 statements and 3 written answers", note=open_link),
  "pilot_r": form("pilot_mentor_report", "About 30 minutes · if you mentor a pilot project", note=open_link),
  "primary_r": form("primary_mentor_report", "About 30 minutes · if you mentor a primary project", note=open_link),
  "mentee_q": form("mentee_survey", "For your awareness · your mentee answers this, not you"),
  "mentee_q_self": form("mentee_survey", "About 10 minutes · 19 statements and 3 written answers", note=open_link),
}
json.dump(pieces, open("/tmp/claude-0/hubbuild/forms_pieces.json", "w"))
print({k: len(v) for k, v in pieces.items()})
