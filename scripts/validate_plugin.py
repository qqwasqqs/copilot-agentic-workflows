#!/usr/bin/env python3
"""Static validator for the agentic-feature-workflow Copilot plugin.

Checks the Agent Plugins 1.0 manifest, agent profiles, skills, cross
references, and the bundled issue-form contracts. Standard library only.

Usage: python3 scripts/validate_plugin.py [repo_root]
Exit codes: 0 = all checks passed, 1 = failures found.
"""

import json
import os
import re
import sys

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*[a-z0-9]$")
LEGACY_FIELDS = ("agents", "skills", "commands", "rules", "hooks", "mcp", "lsp")
AGENT_KEYS = {
    "name", "description", "target", "tools", "model",
    "disable-model-invocation", "user-invocable", "mcp-servers", "metadata",
    "include-custom-instructions",
}
IGNORED_AGENT_KEYS = {"handoffs", "argument-hint", "infer"}
SKILL_KEYS = {"name", "description", "license", "allowed-tools"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#][^)]*)\)")

errors = []
warnings = []
checks = [0]


def check(ok, message):
    checks[0] += 1
    if not ok:
        errors.append(message)
    return ok


def warn(ok, message):
    if not ok:
        warnings.append(message)


def read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def parse_frontmatter(text, path):
    """Minimal YAML frontmatter reader for flat key: value blocks."""
    if not text.startswith("---"):
        errors.append("%s: missing YAML frontmatter" % path)
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        errors.append("%s: unterminated YAML frontmatter" % path)
        return None, text
    block = text[3:end]
    body = text[end + 4:]
    data = {}
    key = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")) and key:
            data[key] = str(data.get(key, "")) + " " + raw.strip()
            continue
        if ":" not in raw:
            errors.append("%s: unparseable frontmatter line: %s" % (path, raw))
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        data[key] = value.strip().strip("'\"")
    return data, body


def valid_name(value):
    return (
        isinstance(value, str)
        and 1 <= len(value) <= 64
        and bool(NAME_RE.match(value))
        and "--" not in value
        and ".." not in value
    )


def check_links(path, text, root):
    base = os.path.dirname(path)
    for target in LINK_RE.findall(text):
        target = target.split("#")[0].strip()
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        resolved = os.path.normpath(os.path.join(base, target))
        check(
            os.path.exists(resolved),
            "%s: broken relative link: %s"
            % (os.path.relpath(path, root), target),
        )


def validate_manifest(root):
    path = os.path.join(root, "plugin.json")
    if not check(os.path.isfile(path), "plugin.json is missing"):
        return
    try:
        manifest = json.loads(read(path))
    except ValueError as exc:
        errors.append("plugin.json: invalid JSON: %s" % exc)
        return
    check(
        manifest.get("$schema") == PLUGIN_SCHEMA,
        "plugin.json: $schema must be %s" % PLUGIN_SCHEMA,
    )
    check(valid_name(manifest.get("name")), "plugin.json: invalid name")
    check(bool(manifest.get("version")), "plugin.json: version is required")
    check(
        bool(manifest.get("description")),
        "plugin.json: description is required",
    )
    for field in LEGACY_FIELDS:
        check(
            field not in manifest,
            "plugin.json: legacy component-path field '%s' is not allowed in a "
            "1.0 manifest" % field,
        )


def validate_agents(root):
    agents_dir = os.path.join(root, "com.github.copilot", "agents")
    if not check(
        os.path.isdir(agents_dir), "com.github.copilot/agents is missing"
    ):
        return set()
    files = sorted(
        f for f in os.listdir(agents_dir) if f.endswith(".agent.md")
    )
    check(bool(files), "com.github.copilot/agents contains no .agent.md files")
    names = set()
    for filename in files:
        path = os.path.join(agents_dir, filename)
        rel = os.path.relpath(path, root)
        text = read(path)
        check("\r\n" not in text, "%s: CRLF line endings" % rel)
        data, body = parse_frontmatter(text, rel)
        if data is None:
            continue
        check(bool(data.get("description")), "%s: description is required" % rel)
        name = data.get("name")
        if name:
            check(valid_name(name), "%s: invalid agent name '%s'" % (rel, name))
            check(
                name == filename[: -len(".agent.md")],
                "%s: name '%s' does not match filename" % (rel, name),
            )
            names.add(name)
        for key in data:
            if key in IGNORED_AGENT_KEYS:
                errors.append(
                    "%s: '%s' is ignored on GitHub and must be removed"
                    % (rel, key)
                )
            elif key not in AGENT_KEYS:
                warnings.append("%s: unrecognized frontmatter key '%s'" % (rel, key))
        check(
            len(body) <= 30000,
            "%s: prompt exceeds the 30000 character limit (%d)" % (rel, len(body)),
        )
        check_links(path, body, root)
    return names


def validate_skills(root):
    skills_dir = os.path.join(root, "skills")
    if not check(os.path.isdir(skills_dir), "skills/ is missing"):
        return set()
    names = set()
    for entry in sorted(os.listdir(skills_dir)):
        skill_dir = os.path.join(skills_dir, entry)
        if not os.path.isdir(skill_dir):
            continue
        path = os.path.join(skill_dir, "SKILL.md")
        rel = os.path.relpath(path, root)
        if not check(os.path.isfile(path), "skills/%s: SKILL.md is missing" % entry):
            continue
        text = read(path)
        check("\r\n" not in text, "%s: CRLF line endings" % rel)
        data, body = parse_frontmatter(text, rel)
        if data is None:
            continue
        check(bool(data.get("description")), "%s: description is required" % rel)
        name = data.get("name")
        check(bool(name), "%s: name is required" % rel)
        if name:
            check(valid_name(name), "%s: invalid skill name '%s'" % (rel, name))
            check(
                name == entry,
                "%s: name '%s' does not match its directory '%s'"
                % (rel, name, entry),
            )
            names.add(name)
        for key in data:
            if key not in SKILL_KEYS:
                warnings.append("%s: unrecognized frontmatter key '%s'" % (rel, key))
        check_links(path, body, root)
        for sub_root, _dirs, files in os.walk(skill_dir):
            for filename in files:
                if filename.endswith(".md") and filename != "SKILL.md":
                    ref = os.path.join(sub_root, filename)
                    check_links(ref, read(ref), root)
    return names


def validate_skill_references(root, skill_names):
    """Every `skill-name` mentioned in an agent or skill must exist."""
    targets = []
    agents_dir = os.path.join(root, "com.github.copilot", "agents")
    if os.path.isdir(agents_dir):
        targets += [
            os.path.join(agents_dir, f)
            for f in os.listdir(agents_dir)
            if f.endswith(".agent.md")
        ]
    skills_dir = os.path.join(root, "skills")
    if os.path.isdir(skills_dir):
        for entry in os.listdir(skills_dir):
            candidate = os.path.join(skills_dir, entry, "SKILL.md")
            if os.path.isfile(candidate):
                targets.append(candidate)
    known = set(skill_names)
    suffixes = ("-authoring", "-planning", "-operations", "-contracts")
    for path in targets:
        rel = os.path.relpath(path, root)
        for token in set(re.findall(r"`([a-z0-9][a-z0-9-]+)`", read(path))):
            if token.endswith(suffixes):
                check(
                    token in known,
                    "%s: references unknown skill '%s'" % (rel, token),
                )


def validate_contracts(root):
    base = os.path.join(root, "skills", "issue-form-contracts")
    forms = os.path.join(base, "forms")
    contracts = os.path.join(base, "contracts")
    if not check(
        os.path.isdir(forms) and os.path.isdir(contracts),
        "issue-form-contracts: forms/ or contracts/ is missing",
    ):
        return
    expected = {"feature-brief", "agent-task", "maintainer-task", "ops-task"}
    found = set()
    for filename in sorted(os.listdir(contracts)):
        if not filename.endswith(".contract.json"):
            continue
        key = filename[: -len(".contract.json")]
        found.add(key)
        rel = "skills/issue-form-contracts/contracts/" + filename
        try:
            contract = json.loads(read(os.path.join(contracts, filename)))
        except ValueError as exc:
            errors.append("%s: invalid JSON: %s" % (rel, exc))
            continue
        check(contract.get("source") == "bundled-default", "%s: source must be bundled-default" % rel)
        origin = contract.get("origin", "")
        check(
            bool(origin) and not os.path.isabs(origin) and ":" not in origin,
            "%s: origin must be a relative path" % rel,
        )
        check(
            os.path.isfile(os.path.join(root, origin.replace("/", os.sep))),
            "%s: origin does not resolve: %s" % (rel, origin),
        )
        fields = contract.get("fields")
        check(isinstance(fields, list) and fields, "%s: fields must be a non-empty list" % rel)
        for field in fields or []:
            check(
                bool(field.get("id")) and bool(field.get("label")),
                "%s: every field needs an id and a label" % rel,
            )
        check(
            os.path.isfile(os.path.join(forms, key + ".yml")),
            "%s: no matching form %s.yml" % (rel, key),
        )
    check(
        expected.issubset(found),
        "missing bundled contracts: %s" % ", ".join(sorted(expected - found)),
    )


def validate_boundaries(root):
    templates = os.path.join(root, ".github", "ISSUE_TEMPLATE")
    check(
        not os.path.isdir(templates),
        ".github/ISSUE_TEMPLATE must not exist: bundled forms are contracts, "
        "not templates for this repository",
    )
    agents_dir = os.path.join(root, "com.github.copilot", "agents")
    if os.path.isdir(agents_dir):
        for filename in os.listdir(agents_dir):
            check(
                "-v1" not in filename and "coding-agent" not in filename,
                "com.github.copilot/agents/%s: obsolete agent must not be "
                "discoverable" % filename,
            )
    migration = os.path.join(root, "migration")
    if os.path.isdir(migration):
        for sub_root, _dirs, files in os.walk(migration):
            for filename in files:
                check(
                    filename != "SKILL.md" and not filename.endswith(".agent.md")
                    or sub_root.endswith("agents"),
                    "migration/%s: unexpected discoverable component" % filename,
                )


def main():
    root = os.path.abspath(
        sys.argv[1] if len(sys.argv) > 1
        else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    )
    validate_manifest(root)
    validate_agents(root)
    skill_names = validate_skills(root)
    validate_skill_references(root, skill_names)
    validate_contracts(root)
    validate_boundaries(root)

    for message in warnings:
        sys.stdout.write("WARN  %s\n" % message)
    for message in errors:
        sys.stdout.write("ERROR %s\n" % message)
    sys.stdout.write(
        "\n%d checks run, %d error(s), %d warning(s)\n"
        % (checks[0], len(errors), len(warnings))
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
