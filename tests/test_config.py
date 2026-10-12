import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Loader(yaml.SafeLoader):
    pass


for tag in ("!include", "!include_dir_named", "!include_dir_merge_named",
            "!include_dir_list", "!include_dir_merge_list", "!secret", "!env_var"):
    Loader.add_constructor(tag, lambda loader, node: f"{node.tag} {node.value}")

CFG = yaml.load((ROOT / "config/configuration.yaml").read_text(), Loader)


def test_keeps_stock_ui_editor_includes():
    # HA's default configuration.yaml carries these; dropping them silently
    # disables automations/scripts/scenes created in the UI.
    assert CFG["automation"] == "!include automations.yaml"
    assert CFG["script"] == "!include scripts.yaml"
    assert CFG["scene"] == "!include scenes.yaml"
    for f in ("automations.yaml", "scripts.yaml", "scenes.yaml"):
        assert (ROOT / "config" / f).exists(), f
