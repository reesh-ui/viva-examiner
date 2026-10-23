# Viva Examiner

Our app helps university students practice viva exams using Gemma 4: it asks a viva question on any topic, then scores the student's answer and gives feedback.

## How Gemma is used
Gemma 4 does the main work: it generates the viva question and grades the student's answer. We call `gemma-4-26b-a4b-it` (with `gemma-4-31b-it` as a retry) through the Gemini API.

## Model and license
Gemma 4, released under the Apache 2.0 license.

## How to run
1. `pip install google-genai python-dotenv streamlit`
2. Create a `.env` file with `GEMINI_API_KEY=your_key`
3. `streamlit run app.py`

## License
MIT