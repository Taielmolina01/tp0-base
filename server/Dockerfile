FROM python:3.9.7-slim
COPY server/main.py /main.py
COPY server/common /common
COPY server/tests /tests
RUN python -m unittest tests/test_common.py
RUN pip install debugpy
ENTRYPOINT ["/bin/sh"]
