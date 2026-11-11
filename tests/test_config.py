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


def test_urls_set_in_yaml():
    # The homeassistant: block disables URL editing in the UI, so the URLs
    # must live here. Remote access is Tailscale (spec §3).
    ha = CFG["homeassistant"]
    assert ha["external_url"] == "http://homeassistant.tail0b5409.ts.net:8123"
    assert ha["internal_url"] == "http://homeassistant.local:8123"
