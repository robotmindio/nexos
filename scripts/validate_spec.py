#!/usr/bin/env python3
"""Validate NexOS specification consistency. Never qualifies an OS/runtime.

No network calls or external schema resolution. This is not a production
policy evaluator, cryptographic verifier, provider, or workflow engine.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    raise SystemExit("Install specification dependencies: python3 -m pip install -r requirements-spec.txt")

ROOT = Path(__file__).resolve().parents[1]
FORMAT = FormatChecker()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"non-finite JSON number: {value}")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def duplicates(values):
    return sorted(str(k) for k, count in Counter(values).items() if count > 1)


def schema_policy_errors(schema):
    """Bounded local checks, not a proof of regex or validator execution safety."""
    problems = []
    if len(json.dumps(schema).encode()) > 131072:
        return ["embedded schema exceeds the 128 KiB registry proposal"]
    stack = [(schema, 0)]
    nodes = 0
    while stack:
        value, depth = stack.pop()
        nodes += 1
        if nodes > 4096:
            problems.append("embedded schema exceeds 4096 nodes")
            break
        if depth > 32:
            problems.append("embedded schema exceeds depth 32")
            break
        if isinstance(value, dict):
            for key in ("$ref", "$dynamicRef"):
                if key in value and not (isinstance(value[key], str) and value[key].startswith("#")):
                    problems.append("embedded schema uses non-local reference")
            if "$id" in value:
                problems.append("embedded schemas cannot change the local resolution base with $id")
            if "pattern" in value and (not isinstance(value["pattern"], str) or len(value["pattern"]) > 256):
                problems.append("embedded pattern exceeds bounded profile")
            stack.extend((v, depth + 1) for v in value.values())
        elif isinstance(value, list):
            stack.extend((v, depth + 1) for v in value)
    if not problems:
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as error:
            problems.append(f"invalid embedded schema: {type(error).__name__}")
    return problems


def semantic_errors(definition, value, catalog=None):
    """Checks relationships inside supplied fixtures, never actual live authority."""
    errors = []
    catalog = catalog or {}
    if definition == "capability":
        for key in ("input_schema", "output_schema"):
            errors.extend(f"{key}: {x}" for x in schema_policy_errors(value[key]))
            if value[key].get("type") != "object":
                errors.append(f"{key}: v0 requires an object-root schema")
        recovery = value.get("recovery_contract")
        if recovery:
            reversible = value["effects"]["reversibility"]
            if reversible == "compensatable" and recovery["scope"] != "compensation":
                errors.append("compensatable operation needs a compensation recovery contract")
            if reversible == "reversible" and recovery["scope"] == "compensation":
                errors.append("reversible operation cannot claim compensation as exact restoration")
    if definition == "grant":
        if timestamp(value["expires_at"]) <= timestamp(value["not_before"]):
            errors.append("grant expiry must follow not_before")
        if duplicates(x["budget_id"] for x in value["budget_allocations"]):
            errors.append("duplicate budget allocation identity")
    if definition == "prepared_action":
        if timestamp(value["expires_at"]) <= timestamp(value["prepared_at"]):
            errors.append("prepared action expires before or at preparation")
        if timestamp(value["deadline"]) < timestamp(value["expires_at"]):
            errors.append("prepared action expiry exceeds task deadline")
        for key, id_key in [("preconditions", "resource_id"), ("budget_allocations", "budget_id")]:
            if duplicates(x[id_key] for x in value[key]):
                errors.append(f"duplicate {key} identity")
    if definition == "context_manifest":
        if value["estimated_tokens"] > value["token_budget"]:
            errors.append("context exceeds proposed token budget")
        for item in value["items"]:
            if item["freshness_status"] == "current" and timestamp(value["prepared_at"]) > timestamp(item["valid_until"]):
                errors.append("current context freshness has expired at preparation")
            if timestamp(item["valid_until"]) < timestamp(item["observed_at"]):
                errors.append("context freshness interval is reversed")
            if value["model_destination_id"] not in item["disclosure_target_ids"]:
                errors.append("context destination is not declared for every included item")
    if definition == "view":
        bindings = {x["id"]: x for x in value["bindings"]}
        if duplicates(x["id"] for x in value["bindings"]):
            errors.append("duplicate view binding IDs")
        if duplicates(x["id"] for x in value["components"]):
            errors.append("duplicate view component IDs")
        for component in value["components"]:
            if component["binding_id"] is not None and component["binding_id"] not in bindings:
                errors.append("view component references a missing binding")
            if component["component"] in ("action", "form") and component["binding_id"] is None:
                errors.append("interactive component has no capability binding")
        for binding in value["bindings"]:
            key = (binding["capability"]["id"], binding["capability"]["version"])
            candidate = catalog.get(key)
            if binding["mode"] == "query" and candidate is not None and candidate["effects"]["mutation"] != "none":
                errors.append("query binding targets a mutating capability")
    if definition == "checkpoint":
        if duplicates(x["name"] for x in value["components"]):
            errors.append("duplicate checkpoint component names")
    if definition == "evidence":
        if value["result"] == "passed" and any(x["exit_code"] != x["expected_exit_code"] for x in value["commands"]):
            errors.append("passed evidence contains an unexpected exit code")
        if value["qualifies_runtime"] and value["repository_commit"] is None:
            errors.append("runtime evidence lacks an immutable repository commit")
    return errors


def validate_case(schema, case, catalog=None):
    name = case["definition"]
    if name not in schema["$defs"]:
        return ["unknown contract definition"]
    wrapper = {"$schema": schema["$schema"], "$defs": schema["$defs"], "$ref": "#/$defs/" + name}
    errors = [f"shape: {error.message}" for error in Draft202012Validator(wrapper, format_checker=FORMAT).iter_errors(case["instance"])]
    if not errors:
        errors.extend(semantic_errors(name, case["instance"], catalog))
    return errors


def graph_errors(plan):
    errors = []
    packages = {x["id"]: x for x in plan["packages"]}
    if duplicates(x["id"] for x in plan["packages"]):
        errors.append("duplicate package IDs")
    for package in plan["packages"]:
        if duplicates(package["depends_on"]):
            errors.append(f"{package['id']}: duplicate dependencies")
        for dependency in package["depends_on"]:
            if dependency not in packages:
                errors.append(f"{package['id']}: unknown dependency {dependency}")
    visiting, done = set(), set()
    def visit(key):
        if key in visiting:
            errors.append(f"dependency cycle at {key}")
            return
        if key in done or key not in packages:
            return
        visiting.add(key)
        for dep in packages[key]["depends_on"]:
            visit(dep)
        visiting.remove(key)
        done.add(key)
    for key in packages:
        visit(key)
    return errors


def traceability_errors(plan, matrix, root=ROOT):
    errors = []
    packages = {x["id"]: x for x in plan["packages"]}
    experiences = {x["id"]: x for x in matrix["experiences"]}
    invariants = {x["id"]: x for x in matrix["invariants"]}
    milestones = {x["id"]: x for x in plan["milestones"]}
    for label, values in [("experience", matrix["experiences"]),("invariant", matrix["invariants"]),("milestone", plan["milestones"]),("profile", plan["release_profiles"])]:
        if duplicates(x["id"] for x in values):
            errors.append(f"duplicate {label} IDs")
    for collection, field in [(packages,"document"),(experiences,"document"),(invariants,"normative_ref")]:
        for key, item in collection.items():
            target = root / item[field]
            if not target.is_file() or not target.resolve().is_relative_to(root.resolve()):
                errors.append(f"{key}: missing or escaping document {item[field]}")
    for left, field, right, back in [(packages,"experiences",experiences,"packages"),(packages,"invariants",invariants,"packages"),(experiences,"invariants",invariants,"experiences")]:
        for key, item in left.items():
            for target in item[field]:
                if target not in right or key not in right[target][back]:
                    errors.append(f"coverage not reciprocal: {key} -> {target}")
        for key, item in right.items():
            for target in item[back]:
                if target not in left or key not in left[target][field]:
                    errors.append(f"coverage not reciprocal: {key} -> {target}")
    for package in packages.values():
        if package["milestone"] not in milestones:
            errors.append(f"{package['id']}: unknown milestone")
    for milestone in milestones.values():
        for key in milestone["requires"]:
            if key not in packages:
                errors.append(f"{milestone['id']}: unknown requirement {key}")
    for profile in plan["release_profiles"]:
        required = set(profile["requires"])
        if profile["qualifier_package"] not in packages:
            errors.append(f"{profile['id']}: unknown qualifier")
        for key in required:
            if key not in packages:
                errors.append(f"{profile['id']}: unknown prerequisite {key}")
            elif not set(packages[key]["depends_on"]).issubset(required):
                errors.append(f"{profile['id']}: prerequisites not dependency-closed at {key}")
        for field, index in [("experiences",experiences),("invariants",invariants)]:
            for key in profile[field]:
                if key not in index:
                    errors.append(f"{profile['id']}: unknown {field} {key}")
    return errors


def evidence_reference_errors(refs, root, *, subject=None, section="packages", profile=None, qualification_kind="runtime"):
    """Check recorded claims and scope. Does not authenticate evidence or rerun it."""
    errors, records = [], []
    schema = load_json(root / 'contracts/nexos.schema.json')
    for item in refs:
        if not isinstance(item, str):
            errors.append("qualified evidence must reference a repository-relative JSON record")
            continue
        path = root / item
        if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
            errors.append(f"missing or escaping qualification evidence: {item}")
            continue
        try:
            record = load_json(path)
        except (ValueError,OSError) as error:
            errors.append(f"unreadable evidence: {item}: {error}")
            continue
        record_errors = validate_case(schema, {"definition":"evidence", "instance":record})
        if record_errors:
            errors.append(f"invalid qualification evidence {item}: {record_errors[0]}")
            continue
        if record["example_only"] or record["result"] != "passed":
            errors.append(f"evidence cannot qualify runtime or engineering work: {item}")
            continue
        runtime_required = section == "profiles" or qualification_kind == "runtime"
        allowed_kinds = {"integration","runtime_vm","runtime_hardware","product_evaluation"} if runtime_required else ({"specification","integration"} if qualification_kind == "specification" else {"specification","unit","integration"})
        if record["validation_kind"] not in allowed_kinds or (runtime_required and record["qualifies_runtime"] is not True):
            errors.append(f"evidence cannot qualify runtime or requested engineering claim: {item}")
            continue
        records.append(record)
    if subject:
        covered_packages = set().union(*(set(x["coverage"]["packages"]) for x in records))
        if section == "packages" and subject not in covered_packages:
            errors.append(f"evidence does not cover package {subject}")
        if section == "profiles" and profile:
            if not any(x["coverage"]["release_profile_id"] == subject for x in records):
                errors.append(f"no explicit qualification record for profile {subject}")
            scoped = [x for x in records if x["coverage"]["release_profile_id"] in (None,subject)]
            for field in ("experiences","invariants"):
                covered = set().union(*(set(x["coverage"][field]) for x in scoped))
                if not set(profile[field]).issubset(covered):
                    errors.append(f"profile {subject} evidence does not cover all {field}")
    return errors


def resolve_scope(scope, plan):
    """Resolve a finite engineering scope; a valid scope does not grant permission."""
    packages={x["id"]:x for x in plan["packages"]}
    milestones={x["id"]:x for x in plan["milestones"]}
    profiles={x["id"]:x for x in plan["release_profiles"]}
    errors=[]; covered=set()
    for field,index in [("package_ids",packages),("milestone_ids",milestones),("release_profile_ids",profiles)]:
        for key in scope[field]:
            if key not in index:
                errors.append(f"unknown scope ID: {key}")
            elif field == "package_ids":
                covered.add(key)
            else:
                covered.update(index[key]["requires"])
    if not covered:
        errors.append("scope resolves to no implementation work")
    return covered,errors


def state_errors(plan, state, root=ROOT):
    errors = []
    packages = {x["id"]:x for x in plan["packages"]}
    profiles = {x["id"]:x for x in plan["release_profiles"]}
    if set(state["packages"]) != set(packages):
        errors.append("state package IDs differ from the plan")
    if set(state["profiles"]) != set(profiles):
        errors.append("state profile IDs differ from the plan")
    allowed = {"pending","in_progress","implemented","qualified","blocked"}
    for section in ("packages","profiles"):
        for key, entry in state[section].items():
            if entry["status"] not in allowed:
                errors.append(f"{key}: unknown status")
            if entry["status"] == "qualified":
                if not entry["evidence"]:
                    errors.append(f"{key}: qualified without evidence")
                errors.extend(evidence_reference_errors(entry["evidence"], root, subject=key, section=section, profile=profiles.get(key), qualification_kind=packages.get(key,{}).get("qualification_kind","runtime")))
                if section == "packages" and key in packages:
                    for dependency in packages[key]["depends_on"]:
                        if state["packages"].get(dependency,{}).get("status") != "qualified":
                            errors.append(f"{key}: prerequisite {dependency} not qualified")
                if section == "profiles" and key in profiles:
                    for dependency in profiles[key]["requires"]:
                        if state["packages"].get(dependency,{}).get("status") != "qualified":
                            errors.append(f"{key}: prerequisite {dependency} not qualified")
                    qualifier = profiles[key]["qualifier_package"]
                    if state["packages"].get(qualifier,{}).get("status") not in ("implemented","qualified"):
                        errors.append(f"{key}: qualification procedure {qualifier} not implemented")
            if section == "packages" and entry.get("checkpoint"):
                checkpoint_path = root / entry["checkpoint"]
                if not checkpoint_path.is_file() or not checkpoint_path.resolve().is_relative_to(root.resolve()):
                    errors.append(f"{key}: missing or escaping checkpoint record")
                else:
                    governance = load_json(root / 'contracts/program.schema.json')
                    checkpoint = load_json(checkpoint_path)
                    wrapper = {"$schema":governance["$schema"],"$defs":governance["$defs"],"$ref":"#/$defs/checkpoint"}
                    checkpoint_errors = list(Draft202012Validator(wrapper,format_checker=FORMAT).iter_errors(checkpoint))
                    if checkpoint_errors:
                        errors.append(f"{key}: invalid active checkpoint: {checkpoint_errors[0].message}")
                    else:
                        covered, scope_problems = resolve_scope(checkpoint["scope"],plan)
                        errors.extend(f"{key}: {x}" for x in scope_problems)
                        if key not in covered:
                            errors.append(f"{key}: checkpoint scope does not match assigned package")
                        for reference_key in ("mandate_ref","environment_tuple_ref"):
                            referenced = root / checkpoint[reference_key]
                            if not referenced.is_file() or not referenced.resolve().is_relative_to(root.resolve()):
                                errors.append(f"{key}: missing or escaping checkpoint {reference_key}")
                        mandate_path = root / checkpoint["mandate_ref"]
                        if mandate_path.is_file() and mandate_path.resolve().is_relative_to(root.resolve()):
                            mandate = load_json(mandate_path)
                            mandate_schema = {"$schema":governance["$schema"],"$defs":governance["$defs"],"$ref":"#/$defs/mandate"}
                            mandate_errors = list(Draft202012Validator(mandate_schema,format_checker=FORMAT).iter_errors(mandate))
                            if mandate_errors:
                                errors.append(f"{key}: invalid referenced mandate: {mandate_errors[0].message}")
                            else:
                                assigned, mandate_problems = resolve_scope(mandate["scope"],plan)
                                errors.extend(f"{key}: {x}" for x in mandate_problems)
                                if not covered.issubset(assigned):
                                    errors.append(f"{key}: checkpoint scope exceeds recorded mandate")
            if entry["status"] == "blocked" and not entry["blockers"]:
                errors.append(f"{key}: blocked without a concrete blocker")
    if state.get("qualification") == "not_started" and any(x["status"] == "qualified" for group in [state["packages"],state["profiles"]] for x in group.values()):
        errors.append("qualification state contradicts qualified records")
    return errors


def link_errors(root=ROOT):
    errors, checked = [], 0
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if len(re.findall(r"^```", text, re.M)) % 2:
            errors.append(f"unbalanced code fence: {path.relative_to(root)}")
        # Literal examples in fenced blocks do not declare navigation links.
        text = re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", text, flags=re.M|re.S)
        for target in re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
            if urlsplit(target).scheme or target.startswith(("#","//")):
                continue
            filename = unquote(target.split("#",1)[0])
            if not filename:
                continue
            resolved = (path.parent / filename).resolve()
            checked += 1
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f"broken/escaping link: {path.relative_to(root)} -> {target}")
    return errors, checked


def run(root=ROOT):
    problems, checks = [], []
    schema = load_json(root/'contracts/nexos.schema.json')
    Draft202012Validator.check_schema(schema)
    fixtures = load_json(root/'contracts/examples.json')["cases"]
    if duplicates(x["id"] for x in fixtures):
        problems.append("duplicate fixture IDs")
    catalog = {(x["instance"]["id"],x["instance"]["version"]):x["instance"] for x in fixtures if x['definition']=='capability' and x['expected']=='valid'}
    for case in fixtures:
        errors = validate_case(schema,case,catalog)
        expected_valid = case["expected"] == "valid"
        if (not errors) != expected_valid:
            problems.append(f"fixture {case['id']}: expected {case['expected']}, got {errors or 'valid'}")
    checks.append({'name':'contract_examples','count':len(fixtures),'positive':sum(c['expected']=='valid' for c in fixtures),'negative':sum(c['expected']=='invalid' for c in fixtures)})
    plan=load_json(root/'program/plan.json');matrix=load_json(root/'conformance/matrix.json');state=load_json(root/'program/state.json')
    governance=load_json(root/'contracts/program.schema.json')
    Draft202012Validator.check_schema(governance)
    governance_cases=[('plan',plan),('state',state),('matrix',matrix),('mandate_template',load_json(root/'program/mandate-template.json')),('checkpoint_template',load_json(root/'program/checkpoint-template.json'))]
    governance_errors=[]
    for definition, instance in governance_cases:
        wrapper={"$schema":governance["$schema"],"$defs":governance["$defs"],"$ref":"#/$defs/"+definition}
        governance_errors.extend(f"{definition} shape: {x.message}" for x in Draft202012Validator(wrapper,format_checker=FORMAT).iter_errors(instance))
    problems.extend(governance_errors)
    checks.append({'name':'program_metadata_schemas','count':len(governance_cases)})
    if not governance_errors:
        problems.extend(graph_errors(plan));problems.extend(traceability_errors(plan,matrix,root));problems.extend(state_errors(plan,state,root))
    checks.append({'name':'program_graph_and_traceability','packages':len(plan['packages']),'experiences':len(matrix['experiences']),'invariants':len(matrix['invariants']),'release_profiles':len(plan['release_profiles'])})
    errors,count=link_errors(root);problems.extend(errors);checks.append({'name':'local_markdown_links','count':count})
    for path in root.rglob('*.json'):
        if 'evidence' not in path.relative_to(root).parts:
            load_json(path)
    inputs=[]
    for path in sorted(root.rglob('*')):
        relative=path.relative_to(root)
        if path.is_file() and not any(p in ('evidence','__pycache__','.git','.venv') for p in relative.parts) and (path.suffix in ('.md','.json','.py','.txt') or path.name=='Makefile'):
            inputs.append({'path':str(relative),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    return {'schema_version':'0.1.0','validation_kind':'specification','qualifies_runtime':False,'recorded_at':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'result':'failed' if problems else 'passed','checks':checks,'problems':problems,'toolchain':{'python':sys.version.split()[0],'jsonschema':version('jsonschema'),'referencing':version('referencing')},'input_manifest':inputs,'limitations':['No operating system, provider, model, sandbox, VM, hardware or external integration was executed.','Schema/fixture checks do not prove live authorization, canonicalization, cryptographic authenticity or recovery.','Runtime qualifications must be independently reproduced on the declared tuple.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    try:
        report=run(args.root.resolve())
    except (OSError,ValueError,KeyError,TypeError) as error:
        print(f'SPECIFICATION CHECK FAILED: {error}',file=sys.stderr)
        return 1
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('input_manifest','recorded_at')},indent=2))
    return 0 if report['result']=='passed' else 1

if __name__=='__main__':
    sys.exit(main())
