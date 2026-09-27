#!/usr/bin/env python3
"""Issue-form contract tooling for the agentic-feature-workflow plugin.

Two subcommands:

  extract  Convert a GitHub issue-form YAML file into a normalized contract
           JSON document. Requires PyYAML. If PyYAML is unavailable the command
           fails with a clear message and the agent falls back to reading the
           form itself and writing the contract JSON by hand.

  render   Validate a values document against a contract and render a
           deterministic Markdown issue body. Pure standard library.

Contract JSON shape:

  {
    "contract_id": "feature-brief",
    "version": "1.0.0",
    "source": "bundled-default" | "target-repository",
    "origin": "<path or description>",
    "title_pattern": "Feature: <name>",
    "labels": ["enhancement"],
    "fields": [
      {"id": "...", "label": "...", "type": "textarea|input|dropdown|checkboxes",
       "required": true, "description": "...", "options": [...],
       "checkbox_options": [{"label": "...", "required": false}]}
    ]
  }

Values JSON shape:

  {
    "title": "Feature: dark mode",
    "labels": ["enhancement"],
    "fields": {"rationale": "...", "scope": "..."}
  }

Exit codes: 0 valid, 1 validation failed, 2 usage/IO error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

INPUT_TYPES = ("textarea", "input", "dropdown", "checkboxes")

# Substrings that indicate an unreplaced example or placeholder value.
PLACEHOLDER_PATTERNS = (
    r"your-username",
    r"your-org",
    r"your_org",
    r"<name>",
    r"<action>",
    r"<object>",
    r"<area>",
    r"<component>",
    r"<subject>",
    r"\byour-repo\b",
    r"example\.com",
)

TBD_PATTERN = re.compile(r"\[tbd\]", re.IGNORECASE)


def _fail(message, code=2):
    sys.stderr.write("error: %s\n" % message)
    raise SystemExit(code)


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (IOError, OSError) as exc:
        _fail("cannot read %s: %s" % (path, exc))
    except ValueError as exc:
        _fail("%s is not valid JSON: %s" % (path, exc))


# --------------------------------------------------------------------------
# extract
# --------------------------------------------------------------------------


def _normalize_labels(raw):
    if raw is None:
        return []
    if isinstance(raw, str):
        return [part.strip() for part in raw.split(",") if part.strip()]
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    return []


def extract(args):
    try:
        import yaml  # type: ignore
    except ImportError:
        _fail(
            "PyYAML is not installed, so the issue-form YAML cannot be parsed "
            "automatically. Read the form yourself and write an equivalent "
            "contract JSON document instead; see SKILL.md, 'Manual contract "
            "extraction'."
        )

    try:
        with open(args.form, "r", encoding="utf-8") as handle:
            form = yaml.safe_load(handle)
    except (IOError, OSError) as exc:
        _fail("cannot read %s: %s" % (args.form, exc))
    except Exception as exc:  # yaml.YAMLError and friends
        _fail("cannot parse %s as YAML: %s" % (args.form, exc))

    if not isinstance(form, dict):
        _fail("%s does not contain a YAML mapping" % args.form)

    fields = []
    for entry in form.get("body") or []:
        if not isinstance(entry, dict):
            continue
        entry_type = entry.get("type")
        if entry_type not in INPUT_TYPES:
            continue
        attributes = entry.get("attributes") or {}
        validations = entry.get("validations") or {}
        field = {
            "id": entry.get("id") or attributes.get("label") or "",
            "label": attributes.get("label") or entry.get("id") or "",
            "type": entry_type,
            "required": bool(validations.get("required", False)),
        }
        if attributes.get("description"):
            field["description"] = attributes["description"]
        if entry_type == "dropdown":
            field["options"] = [str(o) for o in (attributes.get("options") or [])]
        if entry_type == "checkboxes":
            field["checkbox_options"] = [
                {
                    "label": str((o or {}).get("label", "")),
                    "required": bool((o or {}).get("required", False)),
                }
                for o in (attributes.get("options") or [])
                if isinstance(o, dict)
            ]
        fields.append(field)

    contract = {
        "contract_id": args.contract_id or os.path.splitext(os.path.basename(args.form))[0],
        "version": args.contract_version,
        "source": args.source,
        "origin": args.origin or args.form,
        "form_name": form.get("name", ""),
        "title_pattern": form.get("title", ""),
        "labels": _normalize_labels(form.get("labels")),
        "fields": fields,
    }

    output = json.dumps(contract, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(output)
    else:
        sys.stdout.write(output)
    return 0


# --------------------------------------------------------------------------
# render
# --------------------------------------------------------------------------


def _stringify(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "\n".join("- %s" % _stringify(item) for item in value)
    return str(value)


def render(args):
    contract = _load_json(args.contract)
    values = _load_json(args.values)

    if not isinstance(contract.get("fields"), list):
        _fail("contract %s has no 'fields' list" % args.contract)

    field_values = values.get("fields")
    if not isinstance(field_values, dict):
        _fail("values %s has no 'fields' object" % args.values)

    errors = []
    warnings = []
    tbd_fields = []

    title = _stringify(values.get("title")).strip()
    if not title:
        errors.append("title: missing")

    known_ids = set()
    body_parts = []

    for field in contract["fields"]:
        field_id = field.get("id") or ""
        known_ids.add(field_id)
        label = field.get("label") or field_id
        raw = field_values.get(field_id)
        text = _stringify(raw).strip()

        if not text:
            if field.get("required"):
                errors.append("%s: required field is empty" % field_id)
            else:
                warnings.append("%s: optional field is empty, omitted from body" % field_id)
            continue

        if field.get("type") == "dropdown":
            options = field.get("options") or []
            if options and text not in options:
                errors.append(
                    "%s: %r is not one of the allowed options %s" % (field_id, text, options)
                )

        if TBD_PATTERN.search(text):
            tbd_fields.append(field_id)

        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                warnings.append(
                    "%s: contains placeholder-like text matching %r" % (field_id, pattern)
                )

        body_parts.append("### %s\n\n%s" % (label, text))

    for supplied_id in field_values:
        if supplied_id not in known_ids:
            errors.append(
                "%s: not a field in this contract; its content would be "
                "dropped - map it onto a real field or remove it" % supplied_id
            )

    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, title, re.IGNORECASE):
            errors.append("title: contains unreplaced placeholder matching %r" % pattern)

    labels = values.get("labels")
    if labels is None:
        labels = contract.get("labels") or []
    if not isinstance(labels, list):
        errors.append("labels: must be a list")
        labels = []

    body = "\n\n".join(body_parts) + "\n" if body_parts else ""

    if tbd_fields and args.require_no_tbd:
        errors.append("unresolved [tbd] markers in: %s" % ", ".join(tbd_fields))

    result = {
        "contract_id": contract.get("contract_id"),
        "contract_source": contract.get("source"),
        "contract_origin": contract.get("origin"),
        "valid": not errors,
        "title": title,
        "labels": labels,
        "body": body,
        "tbd_fields": tbd_fields,
        "errors": errors,
        "warnings": warnings,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(output)
    else:
        sys.stdout.write(output)
    return 0 if not errors else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command")

    p_extract = sub.add_parser("extract", help="issue-form YAML -> contract JSON")
    p_extract.add_argument("--form", required=True, help="path to the issue-form YAML")
    p_extract.add_argument("--contract-id", help="contract id to record")
    p_extract.add_argument(
        "--source",
        default="target-repository",
        choices=["target-repository", "bundled-default"],
        help="provenance recorded in the contract (default: target-repository)",
    )
    p_extract.add_argument("--origin", help="origin path recorded in the contract")
    p_extract.add_argument(
        "--contract-version", default="extracted", help="version string to record"
    )
    p_extract.add_argument("--out", help="write JSON here instead of stdout")
    p_extract.set_defaults(func=extract)

    p_render = sub.add_parser("render", help="validate values and render a Markdown body")
    p_render.add_argument("--contract", required=True, help="path to the contract JSON")
    p_render.add_argument("--values", required=True, help="path to the values JSON")
    p_render.add_argument("--out", help="write JSON here instead of stdout")
    p_render.add_argument(
        "--require-no-tbd",
        action="store_true",
        help="treat any remaining [tbd] marker as a validation error",
    )
    p_render.set_defaults(func=render)

    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
