from __future__ import annotations

import sys
from pathlib import Path

from streamlit.web import cli as streamlit_cli


def main() -> int:
    app_path = Path(__file__).resolve().parent.parent / "monitor_ui.py"
    sys.argv = ["streamlit", "run", str(app_path), "--server.address=0.0.0.0"]
    return streamlit_cli.main()


if __name__ == "__main__":
    raise SystemExit(main())
