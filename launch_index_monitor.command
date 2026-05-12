#!/bin/bash
# ─────────────────────────────────────────────────────────────
#  CFFEX Index Futures Monitor — launcher
#  Double-click this file to start the Streamlit dashboard.
# ─────────────────────────────────────────────────────────────

# 1. Change to the folder containing this script (project root)
cd "$(dirname "$0")" || { echo "ERROR: Cannot cd to script directory."; read -r -p "Press Enter to exit..."; exit 1; }

# 2. Tushare token — use existing env var or prompt once
if [ -z "$TUSHARE_TOKEN" ] && [ -z "$TS_TOKEN" ]; then
    echo "──────────────────────────────────────────────"
    echo "  No TUSHARE_TOKEN / TS_TOKEN found in env."
    read -r -p "  Enter your Tushare token (or press Enter to skip): " _token
    if [ -n "$_token" ]; then
        export TUSHARE_TOKEN="$_token"
        echo "  Token set for this session."
    else
        echo "  Skipped — running in offline/cached mode."
    fi
    echo "──────────────────────────────────────────────"
fi

# 3. Optional: activate a virtual environment if one exists here
for _venv in ".venv" "venv" "env"; do
    if [ -f "$_venv/bin/activate" ]; then
        echo "Activating virtualenv: $_venv"
        # shellcheck disable=SC1090
        source "$_venv/bin/activate"
        break
    fi
done

# 4. Check that streamlit is available
if ! command -v streamlit &>/dev/null; then
    echo ""
    echo "ERROR: 'streamlit' not found."
    echo "Install it with:  pip install streamlit streamlit-autorefresh pandas tushare"
    read -r -p "Press Enter to exit..."
    exit 1
fi

# 5. Launch the dashboard
echo ""
echo "Starting CFFEX Index Futures Monitor…"
echo "Open your browser at http://localhost:8501"
echo "(Press Ctrl+C in this window to stop)"
echo ""

streamlit run monitor_ui.py \
    --server.headless false \
    --server.port 8501 \
    --browser.gatherUsageStats false

# Keep the Terminal window open if streamlit exits unexpectedly
read -r -p "Monitor stopped. Press Enter to close..."
