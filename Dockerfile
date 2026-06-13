FROM python:3.11-slim

RUN addgroup --system --gid 1000 appuser && \
    adduser --system --uid 1000 --ingroup appuser appuser

WORKDIR /app
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app.py servicer.py store.py kvstore_pb2.py kvstore_pb2_grpc.py ./

EXPOSE 8000

USER appuser

CMD ["python", "app.py"]