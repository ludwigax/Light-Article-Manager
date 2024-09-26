import sys
import json
import warnings

import numpy as np
import pickle as pkl
from FlagEmbedding import BGEM3FlagModel

from typing import List, Dict, Any, Union

warnings.filterwarnings("ignore")

def generate_embedding(
        sentence: Union[List[str], str], 
        model_name: str = "BAAI/bge-m3", 
        use_fp16: bool = True,
        batch_size: int = 32
    ) -> Dict[str, Any]:
    if isinstance(sentence, str):
        sentence = [sentence]

    model = BGEM3FlagModel(model_name, use_fp16=use_fp16)
    vector_dict = model.encode(
        sentence, batch_size=batch_size, max_length=8192, 
        return_sparse=True, return_colbert_vecs=False
    )
    return vector_dict

def main(temp_file):
    with open(temp_file, "rb") as f:
        data = pkl.load(f)
    
    sentence = data["sentence"]
    model_name = data["model_name"]
    use_fp16 = data["use_fp16"]
    batch_size = data["batch_size"]

    vector_dict = generate_embedding(sentence, model_name, use_fp16, batch_size)
    data["vector_dict"] = vector_dict

    with open(temp_file, "wb") as f:
        pkl.dump(data, f)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        raise ValueError("Only one argument is allowed")
    elif len(args) == 0:
        raise ValueError("No argument provided")
    
    temp_file = args[0]
    main(temp_file)
