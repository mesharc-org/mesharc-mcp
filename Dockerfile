# The MeshArc MCP server over stdio. Pass your key at run time:
#   docker build -t mesharc-mcp .
#   docker run -i --rm -e MESHARC_API_KEY=mesharc_... mesharc-mcp
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt server.py ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "server.py"]
