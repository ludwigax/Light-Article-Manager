import transformers
import torch

from transformers import LlamaForCausalLM, AutoTokenizer, TextIteratorStreamer, TextStreamer

import warnings
import threading
import time
import json
import os
import os.path as osp

from typing import Dict, List

warnings.filterwarnings("ignore")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
model_id = "C:/Users/Ludwig/Python Code/asr_prj/pretrained/Meta-Llama-3.1-8B-Instruct"
MODEL_KWARGS = {
    "torch_dtype": torch.bfloat16,
    "device_map": "auto",
}
TOKENIZER_KWARGS = {
    "truncation": True,
}
GENERATION_KWARGS = {
    "max_new_tokens": 512,
}

MESSAGES = "You are a standard machine, and you both process and respond in Chinese."

class Message:
    def __init__(self, system=None, ):
        self._dict = []

        if system is not None:
            self.add_role("system", system)
        else:
            self.add_role("system", MESSAGES)

    def add_role(self, role="user", content=""):
        if len(self._dict) and self._dict[-1]["role"] == role:
            self._dict[-1]["content"] += "\n" + content
        else:
            self._dict.append({"role": role, "content": content})

    def dict(self):
        return self._dict
    
    def print(self):
        for message in self._dict:
            print(f"{message['role']}: {message['content']}")

def prepare_model() -> Dict[str, object]:
    model = LlamaForCausalLM.from_pretrained(model_id, **MODEL_KWARGS)
    model.eval()
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    streamer = TextIteratorStreamer(tokenizer=tokenizer, **TOKENIZER_KWARGS, skip_prompt=True)
    return {"model": model, "tokenizer": tokenizer, "streamer": streamer}

def stream_start(model: torch.nn.Module, generate_kwargs: Dict):
    thread = threading.Thread(target=model.generate, kwargs=generate_kwargs)
    thread.start()
    return thread

def stream_generate(streamer):
    generate_text = ""
    for new_text in streamer:
        generate_text += new_text
        print(new_text, end="", flush=True)
    print()

    return generate_text

def stream_generate_call(streamer, ostream: callable):
    generate_text = ""
    for new_text in streamer:
        generate_text += new_text
        ostream(new_text)
    ostream("[END]")

    return generate_text

def cycle(model: torch.nn.Module, tokenizer: transformers.PreTrainedTokenizer, streamer: TextStreamer, message: Message, generation_kwargs: Dict={}, tokenizer_kwargs: Dict={}):
    inputs = tokenizer.apply_chat_template(
        message.dict(),
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
        **tokenizer_kwargs,
    )

    generative_kwargs = {
        **inputs, **generation_kwargs, "streamer": streamer
    }
    thread = stream_start(model, generative_kwargs)
    generate_text = stream_generate(streamer)

    thread.join()
    return generate_text


def add_content(prompt, role):
    return {"role": role, "content": prompt}

if __name__ == "__main__":
    meta = prepare_model()

    conversation = Message()

    y = input("Should we use saved messages? (y/n) ")
    
    if y == "y" and osp.exists("messages.json"):
        with open("messages.json", "r", encoding="utf-8") as f:
            conversation._dict = json.load(f)

    print("Loaded messages:")
    conversation.print()

    print()
    print("**----------------------------------**")
    print()

    while True:
        prompt = input(">>> ")
        if prompt == "EXIT":
            break

        conversation.add_role("user", prompt)

        generate_text = cycle(
            **meta,
            message=conversation,
            generation_kwargs=GENERATION_KWARGS, 
            tokenizer_kwargs=TOKENIZER_KWARGS
        )

        conversation.add_role("assistant", generate_text)


    with open("messages.json", "w", encoding="utf-8") as f:
        json.dump(conversation.dict(), f, indent=4, ensure_ascii=False)