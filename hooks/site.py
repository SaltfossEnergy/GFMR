"""Make the single-source Markdown notices available to the site footer."""

from pathlib import Path

from markdown import markdown
from markupsafe import Markup


def on_env(env, *, config, files):
    includes = Path(config.config_file_path).parent / "includes"
    for name in ("notice", "disclaimer"):
        env.globals[f"gfmr_{name}"] = Markup(
            markdown((includes / f"{name}.md").read_text(encoding="utf-8"))
        )
    return env
