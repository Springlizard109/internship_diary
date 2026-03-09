import streamlit as st
from graph import build_graph

graph = build_graph()

st.title("AI Knowledge Assistant")

with st.form("ask_form"):
    question = st.text_input("Ask a question")
    submit = st.form_submit_button("Ask")

if submit and question:

    with st.spinner("Thinking..."):
        result = graph.invoke({"question": question})

    st.subheader("Answer")
    st.write(result["answer"])