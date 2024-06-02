# app/streaming.py
from flask_sse import sse

def stream_responses(responses):
    sse.publish(responses, type='response')
