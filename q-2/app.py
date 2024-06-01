import streamlit as st
import time
import google.generativeai as genai
import json
import os
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core import (Settings, StorageContext)
from llama_index.core import (
    load_index_from_storage,
    load_indices_from_storage,
    load_graph_from_storage,
)


# Using the embedding model to Gemini
Settings.embed_model = GeminiEmbedding(
    model_name="models/embedding-001", api_key=os.environ["GEMINI_API_KEY"]
)
Settings.llm = Gemini(model_name="models/gemini-1.5-pro",
                      api_key=os.environ["GEMINI_API_KEY"])


if "convo" not in st.session_state:
    st.session_state["convo"] = []

if "index" not in st.session_state:
    storage_context = StorageContext.from_defaults(
        docstore=SimpleDocumentStore.from_persist_dir(
            persist_dir="./context"),
        vector_store=SimpleVectorStore.from_persist_dir(
            persist_dir="./context"
        ),
        index_store=SimpleIndexStore.from_persist_dir(
            persist_dir="./context"),
    )

    st.session_state["index"] = load_index_from_storage(storage_context)


st.title("Luke Skywalker Chatbot")


def stream_data(text: str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)


for message in st.session_state["convo"]:
    with st.chat_message("Gemini"):
        st.markdown("fdsfdsfsd")


if prompt := st.chat_input("What is up?"):
    with st.chat_message("User"):
        st.markdown(prompt)

    chat_engine = st.session_state["index"].as_chat_engine(
        chat_mode="condense_plus_context", verbose=True)

    response = chat_engine.chat(prompt)

    with st.chat_message("Gemini"):
        st.markdown(response)
