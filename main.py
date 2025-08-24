from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

DIFY_HOST   = os.getenv("DIFY_HOST", "https://dify-ai.tkamc.com")
DIFY_KEY    = os.getenv("DIFY_API_KEY")
DEFAULT_TOP = 5

@app.route("/search", methods=["POST"])
def search():
    data   = request.json
    query  = data["query"]
    kbs    = data["kb_list"]
    top_k  = data.get("top_k", DEFAULT_TOP)

    all_chunks = []
    for kb in kbs:
        url  = f"{DIFY_HOST}/v1/datasets/{kb}/retrieve"
        body = {"query": query, "retrieval_model": {"top_k": top_k}}
        resp = requests.post(url, json=body,
                             headers={"Authorization": f"Bearer {DIFY_KEY}"})
        all_chunks.extend(resp.json().get("records", []))

    all_chunks.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(all_chunks[:top_k])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
