import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

names = [m.name.replace("models/", "") for m in client.models.list()]
print("All:", [n for n in names if "gemini" in n or "gemma" in n])

gemini = [n for n in names if "gemini" in n and "flash" in n][:4]

def try_model(n, tries=1):
    for i in range(tries):
        try:
            r = client.models.generate_content(model=n, contents="Say hi in 3 words.")
            print("OK  ", n, "->", r.text.strip())
            return
        except Exception as e:
            print("FAIL", n, i + 1, str(e)[:50])
            time.sleep(2)

try_model("gemma-4-26b-a4b-it", tries=3)
for n in gemini:
    try_model(n)