"""Fail-closed shared CI integration. Missing team inputs are never passes."""
import argparse, base64, hashlib, json, os, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

REQUIRED = ("Area 2 verification", "Phase D verification", "Finish 01 contract integrity",
            "Finish 01 contract foundation", "Finish 02 validation regressions", "Finish 03 business rules")
def write(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
def validate_mutation(report, policy, source):
    if report["source_sha"] != source: raise ValueError("Mutation report is for another source")
    if report["tool"] not in ("mutmut", "cosmic-ray"): raise ValueError("Unrecognised mutation producer")
    floor=policy["minimum_score"]
    if not isinstance(floor,(int,float)) or not 0 <= floor <= 100 or not policy.get("justification"):
        raise ValueError("Owner must supply a justified mutation threshold")
    operators=report["custom_operators"]
    if len({r["name"] for r in operators if r.get("source") and r.get("business_rule")}) < 2:
        raise ValueError("Two implemented business-rule custom operators required")
    analyses=report["survivor_analysis"]
    if len({r["id"] for r in analyses}) < 15: raise ValueError("Fifteen baseline survivors need analysis")
    for row in analyses:
        if not row.get("evidence") or row["classification"] not in ("equivalent","missing-test","weak-assertion"):
            raise ValueError("Incomplete survivor analysis")
        if row["classification"]!="equivalent" and row.get("retest_status")!="killed":
            raise ValueError("A killable survivor remains")
    total,killed,equivalent=report["total"],report["killed"],report["equivalent"]
    if not all(isinstance(x,int) and x>=0 for x in (total,killed,equivalent)) or killed+equivalent>total or total<=equivalent:
        raise ValueError("Inconsistent mutation counts")
    score=100*killed/(total-equivalent)
    if score<floor: raise ValueError("Mutation score below the justified policy")
    raw=Path(report["raw_result_path"])
    if hashlib.sha256(raw.read_bytes()).hexdigest()!=report["raw_sha256"]:
        raise ValueError("Raw mutation evidence missing or changed")
    return dict(score=score,threshold=floor,total=total,killed=killed,equivalent=equivalent)
def validate_sonar(analyses, gate, source):
    rows=analyses.get("analyses",[])
    if not rows or rows[0].get("revision")!=source: raise ValueError("Sonar analysis revision is not the tested source")
    status=gate["projectStatus"]
    if status["status"]!="OK": raise ValueError("Actual Sonar quality gate is not OK")
    metrics={r["metricKey"]:r for r in status.get("conditions",[])}
    families=(
        ("new_duplicated_lines_density",),
        ("new_reliability_rating","new_software_quality_reliability_rating"),
        ("new_security_rating","new_software_quality_security_rating"),
        ("new_blocker_violations",),
        ("new_critical_violations","new_high_issues"),
    )
    for alternatives in families:
        conditions=[metrics[k] for k in alternatives if k in metrics]
        if not conditions or any(c["status"]!="OK" for c in conditions):
            raise ValueError("Missing/nonpassing proposed owner gate condition: "+"/".join(alternatives))
    if float(metrics["new_duplicated_lines_density"]["errorThreshold"])>3:
        raise ValueError("Sonar duplication threshold exceeds the supplied <=3% proposal")
    return dict(analysis_id=rows[0]["key"],status=status["status"],conditions=status["conditions"])
def get_json(url,token):
    req=urllib.request.Request(url,headers={"Authorization":"Basic "+base64.b64encode((token+":").encode()).decode()})
    with urllib.request.urlopen(req,timeout=30) as response: return json.load(response)
def main():
    p=argparse.ArgumentParser();p.add_argument("kind",choices=("sonar","mutation","aggregate"))
    p.add_argument("--source",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    result=dict(kind=a.kind,source_sha=a.source,accepted=False)
    try:
        if a.kind=="sonar":
            host=os.environ.get("SONAR_HOST_URL","").rstrip("/");token=os.environ.get("SONAR_TOKEN","")
            if not host or not token: raise ValueError("Owner must provide reachable SONAR_HOST_URL and SONAR_TOKEN; historical localhost baseline is not a current gate")
            project=urllib.parse.quote("sqe-horilla",safe="")
            analyses=get_json(host+"/api/project_analyses/search?project="+project+"&ps=1",token)
            gate=get_json(host+"/api/qualitygates/project_status?projectKey="+project,token)
            result.update(analyses=analyses,gate=gate,validation=validate_sonar(analyses,gate,a.source))
        elif a.kind=="mutation":
            runner=Path("scripts/team/run_mutation.py");policy=Path("docs/team/mutation_policy.json")
            missing=[str(p) for p in (runner,policy) if not p.is_file()]
            if missing: raise ValueError("Missing supplied Area 1 mutation implementation/policy: "+", ".join(missing))
            report=Path(a.output).with_name("mutation-tool.json")
            command=[sys.executable,str(runner),"--source",a.source,"--output",str(report)]
            result["command"]=command;code=subprocess.call(command)
            if code: raise ValueError("Mutation producer returned nonzero: "+str(code))
            result["validation"]=validate_mutation(read(report),read(policy),a.source)
        else:
            states={k:os.environ.get(k,"missing") for k in ("UNIT_RESULT","SONAR_RESULT","MUTATION_RESULT")}
            result["dependencies"]=states
            if any(v!="success" for v in states.values()): raise ValueError("Required shared producer failed, skipped or missing")
            repository=os.environ["GITHUB_REPOSITORY"];token=os.environ["GH_TOKEN"]
            req=urllib.request.Request("https://api.github.com/repos/"+repository+"/actions/runs?head_sha="+a.source+"&per_page=100",
                headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json"})
            with urllib.request.urlopen(req,timeout=30) as response: runs=json.load(response)["workflow_runs"]
            selected={name:max([r for r in runs if r["name"]==name],key=lambda r:r["id"],default=None) for name in REQUIRED}
            result["required_runs"]={name:None if row is None else {k:row[k] for k in ("id","status","conclusion","head_sha","html_url")} for name,row in selected.items()}
            if any(r is None or r["status"]!="completed" or r["conclusion"]!="success" for r in selected.values()):
                raise ValueError("Mandatory Area 2/browser/contract producer missing, unfinished or failed for this source")
        result["accepted"]=True
    except Exception as error:
        result["reason"]=str(error);write(a.output,result);print(json.dumps(result,sort_keys=True));return 1
    write(a.output,result);print(json.dumps(result,sort_keys=True));return 0
if __name__=="__main__": sys.exit(main())
