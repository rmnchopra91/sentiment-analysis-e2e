from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
import gradio as gr
import requests

# You can check any other model in the Hugging Face Hub
pipe = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

# We define the app
app = FastAPI()

# We define that we expect our input to be a string
class RequestModel(BaseModel):
   input: str

API_URL = "http://localhost:8000/sentiment"

@app.post("/sentiment")
async def get_response(request: RequestModel):
   prompt = request.input
   response = pipe(prompt)
   label = response[0]["label"]
   score = response[0]["score"]
   return {"answer": label, "score": score, "label": label}

def get_answer_from_api(question):
    response = requests.post(API_URL, json={"input": question})
    if response.status_code == 200:
        data = response.json()
        return data["answer"], data["score"], data["label"]
    else:
        return f"Error occurred while fetching the answer: {response.text}", 0, "NEGATIVE"

def process_question(question):
    answer, score, label = get_answer_from_api(question)
    image_path = "./images/positive.png" if label == "POSITIVE" else "./images/negetive.png"
    return answer, f"Score: {score}", image_path

iface = gr.Interface(
    fn=process_question,
    inputs=gr.Textbox(label="Input"),
    outputs=[
        gr.Textbox(label="Sentiment"),
        gr.Label(label="Score"),
        gr.Image(label="Sentiment Image", type="filepath", width=200, height=200)
    ],
    title="Sentiment Analysis Classification",
    description="Enter a text to get its sentiment, score, and a visual representation."
)

# Combine Gradio interface with FastAPI
app = gr.mount_gradio_app(app, iface, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
