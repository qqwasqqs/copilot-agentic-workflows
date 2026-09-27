#!/usr/bin/env bash
# Smoke tests: negative validator cases + contract render/validate round trips.
set -eu
ROOT=/var/www/copilot-agentic-workflows
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
PASS=0
FAIL=0

ok()  { PASS=$((PASS+1)); echo "PASS  $1"; }
bad() { FAIL=$((FAIL+1)); echo "FAIL  $1"; }

# --- negative validator cases -------------------------------------------------
COPY="$TMP/repo"
cp -r "$ROOT" "$COPY"
rm -rf "$COPY/.git"

expect_fail() { # <label> <needle>
  if python3 "$COPY/scripts/validate_plugin.py" "$COPY" > "$TMP/out" 2>&1; then
    bad "$1 (validator exited 0)"
  elif grep -q "$2" "$TMP/out"; then
    ok "$1"
  else
    bad "$1 (wrong error)"; cat "$TMP/out"
  fi
}

python3 - "$COPY" <<'PY'
import json, sys
p = sys.argv[1] + "/plugin.json"
m = json.load(open(p))
m["agents"] = "./com.github.copilot/agents"
json.dump(m, open(p, "w"), indent=2)
PY
expect_fail "detects legacy component-path field" "legacy component-path"
git -C "$ROOT" show HEAD:plugin.json > /dev/null 2>&1 || true
cp "$ROOT/plugin.json" "$COPY/plugin.json"

mkdir -p "$COPY/.github/ISSUE_TEMPLATE"
cp "$ROOT/skills/issue-form-contracts/forms/ops-task.yml" "$COPY/.github/ISSUE_TEMPLATE/"
expect_fail "detects forms installed as issue templates" "ISSUE_TEMPLATE must not exist"
rm -rf "$COPY/.github"

sed -i 's/^name: ops-issue-authoring$/name: wrong-name/' "$COPY/skills/ops-issue-authoring/SKILL.md"
expect_fail "detects skill name/dir mismatch" "does not match its directory"
cp "$ROOT/skills/ops-issue-authoring/SKILL.md" "$COPY/skills/ops-issue-authoring/SKILL.md"

printf '\n[broken](references/does-not-exist.md)\n' >> "$COPY/skills/sub-issue-planning/SKILL.md"
expect_fail "detects broken relative link" "broken relative link"
cp "$ROOT/skills/sub-issue-planning/SKILL.md" "$COPY/skills/sub-issue-planning/SKILL.md"

printf 'handoffs: [x]\n' > "$TMP/inject"
sed -i "2r $TMP/inject" "$COPY/com.github.copilot/agents/ops-issue-planner.agent.md"
expect_fail "detects ignored 'handoffs' frontmatter" "is ignored on GitHub"
cp "$ROOT/com.github.copilot/agents/ops-issue-planner.agent.md" "$COPY/com.github.copilot/agents/ops-issue-planner.agent.md"

cp "$ROOT/skills/issue-form-contracts/forms/ops-task.yml" "$TMP/orphan.yml"
rm "$COPY/skills/issue-form-contracts/contracts/ops-task.contract.json"
expect_fail "detects a missing bundled contract" "missing bundled contracts"
cp "$ROOT/skills/issue-form-contracts/contracts/ops-task.contract.json" "$COPY/skills/issue-form-contracts/contracts/"

if python3 "$COPY/scripts/validate_plugin.py" "$COPY" > "$TMP/out" 2>&1; then
  ok "restored copy validates cleanly"
else
  bad "restored copy validates cleanly"; cat "$TMP/out"
fi

# --- render round trips -------------------------------------------------------
RENDER="$ROOT/skills/issue-form-contracts/scripts/issue_contract.py"
C="$ROOT/skills/issue-form-contracts/contracts"

for name in feature-brief agent-task maintainer-task ops-task; do
  python3 - "$C/$name.contract.json" "$TMP/$name.values.json" <<'PY'
import json, sys
c = json.load(open(sys.argv[1]))
vals = {}
for f in c["fields"]:
    t = f.get("type")
    if t == "checkboxes":
        vals[f["id"]] = [o["label"] for o in f.get("options", [])][:1]
    elif t == "dropdown":
        vals[f["id"]] = f.get("options", ["n/a"])[0]
    else:
        vals[f["id"]] = "Sample content for %s." % f["label"]
title = c.get("title_pattern") or "Sample title"
import re as _re
title = _re.sub(r"[<\[][^>\]]+[>\]]", "sample feature", title).strip() or "Sample title"
doc = {"title": title, "labels": c.get("labels", []), "fields": vals}
json.dump(doc, open(sys.argv[2], "w"), indent=2)
PY
  if python3 "$RENDER" render --contract "$C/$name.contract.json" --values "$TMP/$name.values.json" \
       --out "$TMP/$name.body.md" --require-no-tbd > "$TMP/out" 2>&1; then
    if python3 -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d['valid'] and d['body'].startswith('### ') and d['title'] else 1)" "$TMP/$name.body.md"; then
      ok "render $name (valid values)"
    else
      bad "render $name: invalid report or missing '### label' body"
    fi
  else
    bad "render $name (valid values)"; cat "$TMP/out"
  fi
done

# missing required field must fail
python3 - "$C/feature-brief.contract.json" "$TMP/feature-brief.values.json" "$TMP/bad1.json" <<'PY'
import json, sys
c = json.load(open(sys.argv[1]))
v = json.load(open(sys.argv[2]))
req = [f["id"] for f in c["fields"] if f.get("required")]
v["fields"].pop(req[0], None)
json.dump(v, open(sys.argv[3], "w"), indent=2)
PY
if python3 "$RENDER" render --contract "$C/feature-brief.contract.json" --values "$TMP/bad1.json" > "$TMP/out" 2>&1; then
  bad "missing required field rejected"; cat "$TMP/out"
else
  ok "missing required field rejected"
fi

# unresolved [tbd] must fail under --require-no-tbd
python3 - "$TMP/feature-brief.values.json" "$TMP/bad2.json" <<'PY'
import json, sys
v = json.load(open(sys.argv[1]))
k = sorted(v["fields"])[0]
v["fields"][k] = "[tbd] still undecided"
json.dump(v, open(sys.argv[2], "w"), indent=2)
PY
if python3 "$RENDER" render --contract "$C/feature-brief.contract.json" --values "$TMP/bad2.json" --require-no-tbd > "$TMP/out" 2>&1; then
  bad "unresolved [tbd] rejected"; cat "$TMP/out"
else
  ok "unresolved [tbd] rejected"
fi

# unknown field id must fail
python3 - "$TMP/feature-brief.values.json" "$TMP/bad3.json" <<'PY'
import json, sys
v = json.load(open(sys.argv[1]))
v["fields"]["not_a_real_field"] = "x"
json.dump(v, open(sys.argv[2], "w"), indent=2)
PY
if python3 "$RENDER" render --contract "$C/feature-brief.contract.json" --values "$TMP/bad3.json" > "$TMP/out" 2>&1; then
  bad "unknown field id rejected"; cat "$TMP/out"
else
  ok "unknown field id rejected"
fi

# --- contract drift -----------------------------------------------------------
cp -r "$C" "$TMP/before"
bash "$ROOT/scripts/regen-contracts.sh" > /dev/null 2>&1 || { bad "regen-contracts.sh ran"; }
if diff -r "$TMP/before" "$C" > /dev/null 2>&1; then
  ok "contracts match their forms (no drift)"
else
  bad "contracts drifted from forms"; diff -r "$TMP/before" "$C" || true
fi

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
