# adapter for stable diffusion api
DEFAULT_API="http://127.0.0.1:7860"
DEFAULT_ENTRY="sdapi/v1/txt2img"

import json
import base64
import requests


def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def save_encoded_image(b64_image: str, output_path: str):
    with open(output_path, 'wb') as image_file:
        image_file.write(base64.b64decode(b64_image))

def sd_default(pos_prompt, neg_prompt, save_path, use_model=None):
    txt2img_url = f'{DEFAULT_API}/{DEFAULT_ENTRY}'
    data = {
        'prompt': pos_prompt,
        'negative_prompt': neg_prompt,
        'sampler_index': 'DPM++ 2M SDE Karras',
        'seed': 1234,
        'steps': 20,
        'width': 512,
        'height': 512,
        'cfg_scale': 8
    }

    if use_model:
        model_title = get_model_names()[use_model]
        data["override_settings"] = data.get("override_settings", {})
        data["override_settings"].update({"sd_model_checkpoint": model_title})

    print(data)

    response = submit_post(txt2img_url, data)
    save_encoded_image(response.json()['images'][0], save_path)
    return save_path


# tools for frontend
import os
# the upper level of base dir and in "stable-diffusion-webui" folder
DEFAULT_SD_REPO_DIR=os.path.join(os.path.dirname(os.environ.get('PROJECT_BASE_DIR')), "stable-diffusion-webui")
DEFAULT_MODEL_DIR=os.path.join(DEFAULT_SD_REPO_DIR, "models/Stable-diffusion")
API_ENTRY="sdapi/v1/sd-models"

def get_model_names():
    # get from the api
    url = f'{DEFAULT_API}/{API_ENTRY}'
    response = requests.get(url)
    # parse the response
    models = {
        model["model_name"]: model["title"] for model in response.json()
    }
    return models
