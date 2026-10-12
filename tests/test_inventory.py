import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import inventory  # noqa: E402

INV = inventory.load(pathlib.Path(__file__).resolve().parents[1] / "inventory/devices.yaml")
NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def test_names_unique():
    names = [d["name"] for d in INV["devices"]]
    assert len(names) == len(set(names)), "duplicate friendly names"


def test_names_valid():
    bad = [d["name"] for d in INV["devices"] if not NAME_RE.match(d["name"])]
    assert bad == [], f"invalid friendly names: {bad}"


def test_outputs_match_model():
    for d in INV["devices"]:
        gangs = INV["gangs"].get(d["model"])
        if gangs is None:
            assert "outputs" not in d, f"{d['name']} has outputs but model has no gangs"
            continue
        assert set(d["outputs"]) == {f"l{i}" for i in range(1, gangs + 1)}, d["name"]


def test_owned_not_exceeded():
    b = inventory.budget(INV)
    over = {m: v for m, v in b.items() if v["assigned_owned"] > v["owned"]}
    assert over == {}, f"more owned devices assigned than in stock: {over}"


def test_budget_matches_spec():
    b = inventory.budget(INV)
    assert b["MINI-ZB2GS"]["to_buy"] == 3
    assert b["MINI-ZB2GS"]["spare"] == 0
    assert b["SNZB-03PR2"]["spare"] == 0
    assert b["SNZB-04PR1"]["spare"] == 0
    assert inventory.spare_outputs(INV) == ["storage_fans_c.l2"]


def test_total_outputs():
    assert inventory.total_outputs(INV) == 26  # 25 needed + 1 spare


def test_render_markdown_lists_every_device():
    md = inventory.render_markdown(INV)
    for d in INV["devices"]:
        assert f"`{d['name']}`" in md
