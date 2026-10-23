import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

MODELS = ["gemma-4-26b-a4b-it", "gemma-4-31b-it"]


def ask(prompt):
    start = time.time()
    for _ in range(3):
        for m in MODELS:
            try:
                r = client.models.generate_content(model=m, contents=prompt)
                return r.text, f"{m} ({time.time() - start:.1f}s)"
            except Exception:
                time.sleep(1)
    return None, None


st.title("Viva Examiner")
st.caption("Practice your viva with Gemma 4")

topic = st.text_input("Course / topic", placeholder="e.g. Operating Systems")

if st.button("Ask me a question") and topic:
    with st.spinner("Examiner is thinking..."):
        q, used = ask(
            f"You are a strict but fair university viva examiner for a "
            f"BS Computer Science student.\n"
            f"Topic: {topic}\n"
            f"Ask ONE short viva question strictly about this topic, answerable "
            f"in 3-4 sentences. Output only the question."
        )
    if q is None:
        st.error("Gemma server is busy right now. Please click the button again.")
    else:
        st.session_state.q = q
        st.session_state.used = used
        st.session_state.pop("feedback", None)

if "q" in st.session_state:
    st.subheader("Question")
    st.write(st.session_state.q)
    answer = st.text_area("Your answer")
    if st.button("Evaluate my answer") and answer:
        with st.spinner("Evaluating your answer..."):
            fb, used = ask(
                f"You are a strict viva examiner.\n"
                f"Viva question: {st.session_state.q}\n"
                f"Student answer: {answer}\n\n"
                f"Grade ONLY what the student actually wrote. Do not assume, "
                f"add, or credit anything they did not say. If the answer is "
                f"short or incomplete, give a low mark.\n"
                f"Format:\nMarks: x/10\nWhat was good: ...\n"
                f"What was missing: ...\nShort model answer: (3-4 sentences)"
            )
        if fb is None:
            st.error("Gemma server is busy right now. Please click Evaluate again.")
        else:
            st.session_state.feedback = fb
            st.session_state.used = used

if "feedback" in st.session_state:
    st.subheader("Feedback")
    st.write(st.session_state.feedback)

if "used" in st.session_state:
    st.caption(f"Model: {st.session_state.used}")