#!/usr/bin/env python3
"""Device inventory: budget check and Markdown rendering.

Usage:
  inventory.py --check            exit 1 on any budget violation
  inventory.py --write            rewrite docs/device-inventory.md
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from collections import defaultdict

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "inventory/devices.yaml"
DOC_PATH = ROOT / "docs/device-inventory.md"
OWNED_STATES = {"owned", "paired"}


def load(path: pathlib.Path = DEFAULT_PATH) -> dict:
    return yaml.safe_load(path.read_text())


def budget(inv: dict) -> dict[str, dict[str, int]]:
    assigned_owned: dict[str, int] = defaultdict(int)
    to_buy: dict[str, int] = defaultdict(int)
    for d in inv["devices"]:
        if d["status"] in OWNED_STATES:
            assigned_owned[d["model"]] += 1
        elif d["status"] == "to_buy":
            to_buy[d["model"]] += 1
        else:
            raise ValueError(f"{d['name']}: unknown status {d['status']}")
    out = {}
    for model, owned in inv["stock"].items():
        out[model] = {
            "owned": owned,
            "assigned_owned": assigned_owned[model],
            "to_buy": to_buy[model],
            "spare": owned - assigned_owned[model],
        }
    return out


def spare_outputs(inv: dict) -> list[str]:
    return [
        f"{d['name']}.{k}"
        for d in inv["devices"]
        for k, v in (d.get("outputs") or {}).items()
        if str(v).strip().lower() == "spare"
    ]


def total_outputs(inv: dict) -> int:
    return sum(len(d.get("outputs") or {}) for d in inv["devices"])


def violations(inv: dict) -> list[str]:
    errs = []
    names = [d["name"] for d in inv["devices"]]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        errs.append(f"duplicate names: {sorted(dupes)}")
    for d in inv["devices"]:
        gangs = inv["gangs"].get(d["model"])
        if gangs and set(d.get("outputs") or {}) != {f"l{i}" for i in range(1, gangs + 1)}:
            errs.append(f"{d['name']}: outputs do not match {gangs}-gang model")
    for model, b in budget(inv).items():
        if b["assigned_owned"] > b["owned"]:
            errs.append(f"{model}: {b['assigned_owned']} assigned but only {b['owned']} owned")
    return errs


def render_markdown(inv: dict) -> str:
    b = budget(inv)
    lines = [
        "# Device inventory",
        "",
        "Generated from `inventory/devices.yaml` by `scripts/inventory.py --write`. Do not edit by hand.",
        "",
        "## Budget",
        "",
        "| Model | Owned | Assigned (owned) | To buy | Spare |",
        "|---|---:|---:|---:|---:|",
    ]
    for model, v in b.items():
        lines.append(f"| {model} | {v['owned']} | {v['assigned_owned']} | {v['to_buy']} | {v['spare']} |")
    lines += [
        "",
        f"Relay outputs assigned: {total_outputs(inv)}. Spare outputs: "
        + (", ".join(f"`{s}`" for s in spare_outputs(inv)) or "none")
        + ".",
        "",
        "## Devices",
        "",
        "| Name | Model | Status | Location | Outputs |",
        "|---|---|---|---|---|",
    ]
    for d in inv["devices"]:
        outs = ", ".join(f"{k}: {v}" for k, v in (d.get("outputs") or {}).items())
        lines.append(f"| `{d['name']}` | {d['model']} | {d['status']} | {d['location']} | {outs} |")
    if inv.get("wishlist"):
        lines += ["", "## Wishlist (priority order)", ""]
        for w in inv["wishlist"]:
            lines.append(f"- {w['model']} — {w['location']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--path", type=pathlib.Path, default=DEFAULT_PATH)
    args = ap.parse_args(argv)
    inv = load(args.path)
    errs = violations(inv)
    if args.write:
        DOC_PATH.write_text(render_markdown(inv))
        print(f"wrote {DOC_PATH}")
    if args.check or not args.write:
        for e in errs:
            print("ERROR:", e)
        print("ok" if not errs else f"{len(errs)} violation(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
