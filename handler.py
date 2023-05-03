#!/usr/bin/env python
""" Contains the handler function that will be called by the serverless. """

import json
import runpod
import whisperx
from faster_whisper import WhisperModel
from app import generate

# Load models into VRAM here so they can be warm between requests

global model, model_a, metadata
model_name = "medium.en"
lang = "en"
device = "cuda"
compute_type = "float32"

model = WhisperModel(model_name, device=device, compute_type=compute_type)

# load alignment model and metadata
model_a, metadata = whisperx.load_align_model(language_code=lang, device=device)


def handler(event):
    """
    This is the handler function that will be called by the serverless.
    """
    global model, model_a, metadata

    print(event)

    model_inputs = event.get("input")

    if not model_inputs:
        return "error: model_inputs not found"

    output = generate(model, model_a, metadata, model_inputs)

    # return the output that you want to be returned like pre-signed URLs to output artifacts
    return output


runpod.serverless.start({"handler": handler})
