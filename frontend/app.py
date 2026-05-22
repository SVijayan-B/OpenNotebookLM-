import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="OpenNotebookLM++",
    layout="wide",
)

st.title("📘 OpenNotebookLM++")
st.caption("Local, cost-free, multimodal research assistant")

# ------------------------
# Sidebar: Ingestion
# ------------------------
st.sidebar.header("📥 Ingest Data")

uploaded_doc = st.sidebar.file_uploader(
    "Upload Document (PDF / TXT / MD)",
    type=["pdf", "txt", "md"]
)

if uploaded_doc:
    with st.spinner("Uploading document..."):
        files = {"file": (uploaded_doc.name, uploaded_doc, uploaded_doc.type)}
        res = requests.post(f"{API_BASE}/ingest/document", files=files)

    if res.status_code == 200:
        st.sidebar.success("Document ingested successfully")
    else:
        st.sidebar.error("Document ingestion failed")

uploaded_video = st.sidebar.file_uploader(
    "Upload Video (MP4 / MKV)",
    type=["mp4", "mkv"]
)

if uploaded_video:
    with st.spinner("Uploading video & transcribing..."):
        files = {"file": (uploaded_video.name, uploaded_video, uploaded_video.type)}
        res = requests.post(f"{API_BASE}/ingest/video", files=files)

    if res.status_code == 200:
        st.sidebar.success("Video ingested successfully")
    else:
        st.sidebar.error("Video ingestion failed")

# ------------------------
# Main: Query
# ------------------------
st.header("🔍 Ask a Question")

question = st.text_input(
    "Ask a question about your uploaded documents and videos"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            res = requests.post(
                f"{API_BASE}/query",
                json={"question": question}
            )

        if res.status_code != 200:
            st.error("Query failed")
        else:
            data = res.json()

            st.subheader("🧠 Answer")
            st.write(data["answer"])

            if data["sources"]:
                st.subheader("📚 Sources")
                for i, src in enumerate(data["sources"], start=1):
                    if src.get("page") is not None:
                        st.markdown(
                            f"**{i}. {src['source']} — page {src['page']}** "
                            f"(score: {src['score']:.2f})"
                        )
                    else:
                        st.markdown(
                            f"**{i}. {src['source']} — "
                            f"{src['start_time']:.2f}s–{src['end_time']:.2f}s** "
                            f"(score: {src['score']:.2f})"
                        )
            else:
                st.info("No sources available (refused safely).")
