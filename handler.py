#!/usr/bin/env python
""" Contains the handler function that will be called by the serverless. """

import json
import runpod
from faster_whisper import WhisperModel
from app import generate

# Load models into VRAM here so they can be warm between requests

global modelBase, modelMedium


lang = "en"
device = "cpu"  # cuda"
compute_type = "int8"  # float16"
modelBase = None  # WhisperModel("base.en", device=device, compute_type=compute_type)
modelMedium = (
    None  # WhisperModel("medium.en", device=device, compute_type=compute_type)
)


def handler(event):
    """
    This is the handler function that will be called by the serverless.
    """
    global modelBase, modelMedium

    print(event)

    model_inputs = event.get("input")

    if not model_inputs:
        return "error: model_inputs not found"

    type = model_inputs["type"]

    if type == "base_transcribe":
        subtitles_list = generate(modelBase, model_inputs)
        output = json.dumps(subtitles_list)
    else:
        return "invalid type in dict"

    # return the output that you want to be returned like pre-signed URLs to output artifacts
    return output


runpod.serverless.start({"handler": handler})
