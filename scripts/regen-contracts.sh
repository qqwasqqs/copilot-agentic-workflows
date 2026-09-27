#!/usr/bin/env bash
# Regenerate the bundled default contract JSON documents from the bundled forms.
# Run from the repository root: bash scripts/regen-contracts.sh
set -eu

root="$(cd "$(dirname "$0")/.." && pwd)"
skill="$root/skills/issue-form-contracts"

for name in feature-brief agent-task maintainer-task ops-task; do
  python3 "$skill/scripts/issue_contract.py" extract \
    --form "$skill/forms/$name.yml" \
    --contract-id "$name" \
    --source bundled-default \
    --origin "skills/issue-form-contracts/forms/$name.yml" \
    --contract-version "1.0.0" \
    --out "$skill/contracts/$name.contract.json"
  echo "regenerated contracts/$name.contract.json"
done
