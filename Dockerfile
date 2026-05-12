FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY index_pricing ./index_pricing
COPY monitor_ui.py realtime_adapter.py price_indices.py hk_highcap_report.py ./

RUN pip install --upgrade pip && pip install .

EXPOSE 8501

CMD ["streamlit", "run", "monitor_ui.py", "--server.address=0.0.0.0", "--server.port=8501"]
