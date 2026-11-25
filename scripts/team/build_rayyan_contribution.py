"""Build a clearly partial, reproducible contribution from tracked source + genuine CI."""
import argparse, hashlib, io, json, os, re, subprocess, sys, zipfile
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,d): Path(p).write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
def xml(p):
    rows=list(ET.parse(p).getroot().iter("testcase"))
    if not rows: raise ValueError("Empty JUnit: "+str(p))
    return rows
def ident(row):
    props={p.get("name"):p.get("value",p.text) for p in row.findall("./properties/property")}
    return props.get("case_id") or row.get("name"),props
def bad(row): return next((k for k in ("error","failure","skipped") if row.find(k) is not None),None)
def unique(root,name):
    rows=list(Path(root).rglob(name))
    if len(rows)!=1:raise ValueError("Expected exactly one "+name+", found "+str(len(rows)))
    return rows[0]
def verify_evidence(root,source):
    api=Path(root)/"api"; result=read(unique(api,"PROMPT03_EXECUTION_SUMMARY.json"))
    assert result["tested_source_sha"]==source and result["full_scope_accepted"]
    expected={r["case_id"] for r in read("tests/team/api/case_ledger.json")["entries"]}
    for order in ("first","reversed"):
        paths=list(api.rglob(order+"-shard-*.xml"))
        assert len(paths)==16
        ids=[]
        for path in paths:
            for row in xml(path):
                case,props=ident(row)
                assert not bad(row) and props["source_sha"]==source
                assert props["spec_sha256"]==result["spec_sha256"]
                ids.append(case)
        assert len(ids)==len(expected) and len(set(ids))==len(ids) and set(ids)==expected
    browser=xml(unique(Path(root)/"browser","browser.xml"))
    assert len(browser)==10 and not any(bad(r) for r in browser)
    expected_ui={f"UC-RAY-{number:02d}-{flow}" for number in (1,2) for flow in ("MAIN","A1","A2","E1","E2")}
    observed_ui={re.search(r"UC-RAY-\d{2}-(?:MAIN|A[12]|E[12])",row.get("name","")).group(0) for row in browser}
    assert observed_ui==expected_ui
    baseline=xml(unique(Path(root)/"regeneration","baseline.xml"))
    variant=xml(unique(Path(root)/"regeneration","variant.xml"))
    assert len(baseline)==len(variant)==6 and not any(bad(r) for r in baseline)
    expected_fail={"self_allocation_create:body:description:BVA:minLength-below","self_allocation_create:body:attachment:BVA:x-filename-maxLength-above"}
    assert {ident(r)[0] for r in variant if bad(r)}==expected_fail
    assert all(bad(r) in (None,"failure") for r in variant)
    business=list((Path(root)/"business").rglob("business-*.xml"))
    assert len(business)==4
    cases=[r for p in business for r in xml(p)]
    assert len(cases)==482 and not any(bad(r) for r in cases)
    req=read(unique(api,"PROMPT03_REQUIREMENT_EVIDENCE.json"))
    assert req["all_requirements_verified"] and len(req["requirements"])==14
    return result,req

def make_pdf(path,data,verified,requirements):
    from html import escape
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
    from reportlab.graphics.shapes import Drawing,Line,String,Rect,PolyLine
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    font=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    if font.exists():
        pdfmetrics.registerFont(TTFont("Body",str(font)))
        pdfmetrics.registerFont(TTFont("Bold",str(font.with_name("DejaVuSans-Bold.ttf"))))
        regular,bold="Body","Bold"
    else:regular,bold="Helvetica","Helvetica-Bold"
    navy=colors.HexColor("#17324D");teal=colors.HexColor("#087F8C");amber=colors.HexColor("#A65E00")
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Text",fontName=regular,fontSize=9,leading=13,spaceAfter=7))
    styles.add(ParagraphStyle(name="Cell",fontName=regular,fontSize=8,leading=11))
    styles.add(ParagraphStyle(name="Header",fontName=bold,fontSize=8,leading=11,textColor=colors.white))
    styles.add(ParagraphStyle(name="Head",fontName=bold,fontSize=15,leading=19,textColor=navy,spaceBefore=14,spaceAfter=9))
    styles.add(ParagraphStyle(name="Cover",fontName=bold,fontSize=25,leading=30,textColor=navy,spaceAfter=14))
    story=[]
    def clean(s):
        return str(s).replace("\u2011","-").replace("\u2013","-").replace("\u2014","-").replace("\u2192"," -> ")
    def para(s,style="Text"):
        return Paragraph(escape(clean(s)).replace("\n","<br/>"),styles[style])
    def text(s):story.append(para(s))
    def head(s):story.append(para(s,"Head"))
    def table(headers,rows,widths=None):
        values=[[para(x,"Header" if i==0 else "Cell") for x in row] for i,row in enumerate([headers]+rows)]
        t=Table(values,colWidths=widths or [495/len(headers)]*len(headers),repeatRows=1,hAlign="LEFT")
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),navy),("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("VALIGN",(0,0),(-1,-1),"TOP"),("GRID",(0,0),(-1,-1),.3,colors.HexColor("#D5DFE8")),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F1F5F8")]),
            ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
        story.append(t);story.append(Spacer(1,9))
    story.append(para("Final contribution and execution closeout","Cover"))
    text("Syed Muhammad Rayyan Hassan | 24I-3000 | SE-5B | 25 November 2026")
    text("AREA 2 CONTRIBUTION - NOT THE FINAL GROUP SUBMISSION")
    text("Rayyan's technical execution assignment is closed. Whole-project recommendation: HOLD.")
    text("No further technical execution or additional prompt is expected from Rayyan.")
    text("Verified application/test source: "+data["tested_source"])
    text("Published contribution revision: "+os.environ.get("GITHUB_SHA","local"))
    text("Repository: https://github.com/includeduck/SQE-Horilla-Project | PR #8 remains subject to independent review.")
    head("1. Scope, ownership and approach")
    for line in data["scope"]:text(line)
    table(["Stage","Verified contribution","Remaining qualification"],data["stages"],[40,305,150])
    head("2. Actual coverage and results")
    table(["Population","Actual / denominator","Interpretation"],data["coverage"],[145,125,225])
    text("Each complete API collection contains "+str(verified["api_cases"])+" unique cases. The two orders and focused/upstream populations overlap and are never added into a fictitious unique total.")
    table(["Requirement","Required cases per order","Result"],[[r["requirement"],len(r["required_case_ids"]),r["status"]] for r in requirements["requirements"]],[95,130,270])
    table(["Browser flow","Verified result","Persisted / visible oracle"],[[r["id"],r["result"],r["oracle"]] for r in data["browser_flows"]],[100,70,325])
    head("3. Commands, versions and immutable evidence")
    for command in data["commands"]:text(command)
    for row in data["runs"]:text(str(row["id"])+" | "+row["name"]+" | "+row["url"])
    for line in data["version_notes"]:text(line)
    text("Original XML/logs/screenshots/traces and raw derived ledgers are included under evidence; package_manifest.json records payload hashes. The source whitelist excludes .git, databases, environment secrets, virtual environments and user media.")
    head("4. Defects, corrections and retained failed evidence")
    text(data["defect_summary"])
    table(["Defect","Issue","Correction","State"],[[r["id"],"#"+str(r["issue"]),r["fix"][:12],r["state"]] for r in data["defects"]],[85,45,120,245])
    for row in data["defect_notes"]:text(row)
    head("5. Two major root causes and corrective controls")
    for item in data["rca"]:
        text(item["title"])
        table(["Why","Source-backed finding"],[[str(i+1),v] for i,v in enumerate(item["whys"])],[35,460])
        drawing=Drawing(495,110)
        drawing.add(Line(15,55,470,55,strokeColor=navy,strokeWidth=2))
        factors=item["factors"]
        for i,factor in enumerate(factors):
            x=50+i*100;y=95 if i%2==0 else 10
            drawing.add(Line(x,y+5,x+35,55,strokeColor=teal,strokeWidth=1))
            drawing.add(String(x-25,y+10 if y>55 else y-1,clean(factor),fontName=regular,fontSize=7))
        drawing.add(String(340,62,"Observed defect",fontName=bold,fontSize=8,fillColor=navy))
        story.append(drawing);text(item["control"])
    head("6. Defined Pareto population")
    text("Twenty-two distinct confirmed Area 2 product defects across dated builds. Excludes Area 1 findings, coordination, harness errors and repeated failing parametrizations. Historical four/seven-defect snapshots remain in the repository.")
    table(["Category","Count","Share","Cumulative"],data["pareto"],[285,45,75,90])
    head("7. Risk, exit criteria and GQM")
    table(["Risk","L x I","Verified control / residual risk"],data["risks"],[60,55,380])
    table(["Criterion","Target","Actual / decision"],data["criteria"],[75,185,235])
    for line in data["gqm"]:text(line)
    head("8. Mandatory final ownership and readiness")
    text(data["ownership_statement"])
    table(["ID / priority","Mandatory Wasay action","Dependency and acceptance"],[[r["id"]+" / "+r["priority"],r["work"],r["acceptance"]] for r in data["remaining"]],[90,205,200])
    for line in data["limits"]:text(line)
    text("Assignment closeout is not project release, teammate acceptance, a human review or a personal viva result.")
    def footer(canvas,doc):
        canvas.setStrokeColor(navy);canvas.line(42,34,553,34)
        canvas.setFont(regular,7);canvas.drawString(42,23,"SQE Horilla | Rayyan contribution | Project HOLD")
        canvas.drawRightString(553,23,str(doc.page))
    doc=SimpleDocTemplate(str(path),pagesize=(595,842),rightMargin=50,leftMargin=50,topMargin=42,bottomMargin=48,
        title="Rayyan final contribution and execution closeout",author="Syed Muhammad Rayyan Hassan")
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

def main():
    p=argparse.ArgumentParser();p.add_argument("--evidence",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    data=read("docs/team/finish-line/FINAL_CLOSEOUT_DATA.json")
    verified,req=verify_evidence(a.evidence,data["tested_source"])
    pdf=out/"Rayyan_24I-3000_Final_Contribution.pdf";make_pdf(pdf,data,verified,req)
    allowed_prefix=("tests/team/","scripts/team/","docs/team/",".github/workflows/",".github/scripts/")
    exact={"Communication.md","handoff.md","requirements.txt","sonar-project.properties","LICENSE","README.md",
        "horilla/config.py","horilla/filters.py","horilla/models.py","horilla_api/api_decorators/base/decorators.py",
        "horilla_api/api_methods/base/methods.py","horilla_api/api_serializers/leave/serializers.py","horilla_api/api_views/leave/views.py","leave/forms.py"}
    paths=subprocess.check_output(["git","ls-files","-z"]).decode().split("\0")
    payload={}
    deny={".db",".sqlite",".sqlite3",".sql",".pem",".key",".pfx"}
    for name in paths:
        if not name or not(name in exact or name.startswith(allowed_prefix)):continue
        if name=="docs/team/finish-line/FINAL_PUBLICATION.json":continue
        path=Path(name)
        if path.suffix.lower() in deny or path.name==".env" or any(x in path.parts for x in (".git",".venv","node_modules","media","__pycache__")):continue
        if path.is_file():payload["source/"+name]=path.read_bytes()
    for path in Path(a.evidence).rglob("*"):
        if path.is_file():
            if path.suffix.lower() in deny: raise ValueError("Database/key unexpectedly present in CI evidence")
            payload["evidence/"+path.relative_to(a.evidence).as_posix()]=path.read_bytes()
    payload["Rayyan_24I-3000_Final_Contribution.pdf"]=pdf.read_bytes()
    payload["PACKAGE_README.txt"]=("RAYYAN CONTRIBUTION ONLY - NOT FINAL GROUP SUBMISSION\n"
        "The archive contains Rayyan's work and genuine shared inputs with their original ownership.\n"
        "No synchronized .git is claimed. Clone the public repository at the recorded revision to obtain upstream dependencies/history.\n"
        "Group Area 3, mutation, accepted integration and owner gates remain mandatory Wasay work.\n"
        "See source/handoff.md and source/docs/team/reports/RAYYAN_FINAL_CLOSEOUT.md.\n").encode()
    manifest={"format":1,"label":"Exact contribution payload; not a whole-group release","source_revision":os.environ.get("GITHUB_SHA"),"tested_source":data["tested_source"],
        "exclusions":["package_manifest.json self-hash","ZIP outer bytes","active databases/secrets/virtualenv/media",".git unavailable accepted group history"],
        "files":[{"path":name,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
            "git_blob_sha1":hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest() if name.startswith("source/") else None}
            for name,raw in sorted(payload.items())]}
    index={}
    for item in subprocess.check_output(["git","ls-files","-s","-z"]).decode().split("\0"):
        if item:
            metadata,name=item.split("\t",1);index[name]=metadata.split()[1]
    for row in manifest["files"]:
        if row["path"].startswith("source/") and row["git_blob_sha1"]!=index[row["path"][7:]]:
            raise ValueError("Packaged source differs from published Git bytes: "+row["path"])
    for name,raw in payload.items():
        if re.search(rb"-----BEGIN (?:RSA|EC|OPENSSH) PRIVATE KEY-----",raw) or re.search(rb"gh[pousr]_[A-Za-z0-9]{30,}",raw):
            raise ValueError("Credential-shaped payload refused; inspect "+name)
    payload["package_manifest.json"]=(json.dumps(manifest,indent=2)+"\n").encode()
    archive=out/"Rayyan_24I-3000_SE5B_Contribution.zip"
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as stream:
        for name,raw in sorted(payload.items()):stream.writestr(name,raw)
    with zipfile.ZipFile(archive) as stream:
        assert stream.testzip() is None
        for row in manifest["files"]:assert hashlib.sha256(stream.read(row["path"])).hexdigest()==row["sha256"]
    write(out/"package_manifest.json",manifest)
    print("FINAL_PACKAGE "+json.dumps({"source_revision":manifest["source_revision"],"tested_source":data["tested_source"],"files":len(manifest["files"]),
        "zip_bytes":archive.stat().st_size,"zip_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),"pdf_sha256":hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "api_cases_per_order":verified["api_cases"],"mandatory_families":verified["mandatory_input_families"],"requirements":len(req["requirements"])}),flush=True)
if __name__=="__main__":main()
