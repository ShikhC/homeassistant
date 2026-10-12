#!/usr/bin/env bash
# Lint and check the HA config locally. Never contacts the HA instance.
set -euo pipefail
cd "$(dirname "$0")/.."
VENV=.venv/bin

echo "== yamllint"
$VENV/yamllint config addons inventory

echo "== dashboard files referenced by configuration.yaml exist"
$VENV/python - <<'EOF'
import sys, yaml, pathlib
class Loader(yaml.SafeLoader): pass
for tag in ("!include", "!include_dir_named", "!include_dir_merge_named",
            "!include_dir_list", "!include_dir_merge_list", "!secret", "!env_var"):
    Loader.add_constructor(tag, lambda l, n: None)
cfg = yaml.load(pathlib.Path("config/configuration.yaml").read_text(), Loader) or {}
missing = []
for key, dash in ((cfg.get("lovelace") or {}).get("dashboards") or {}).items():
    f = pathlib.Path("config") / dash["filename"]
    if not f.exists():
        missing.append(f"{key}: {f}")
if missing:
    print("missing dashboard files:", *missing, sep="\n  "); sys.exit(1)
print("ok")
EOF

echo "== hass check_config"
$VENV/hass --script check_config -c config

echo "== pytest"
# exit 5 = no tests collected; acceptable before the first test file exists
$VENV/pytest -q || [ $? -eq 5 ]
