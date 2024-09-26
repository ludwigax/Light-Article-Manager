import sys
import numpy as np
import pickle as pkl

def similarity_calculate(query, vector_base):
    """
    Calculate the similarity scores between the query vector and the vector base.

    :param query: A 1*n or n-dimensional vector (numpy array)
    :param vector_base: An x*n dimensional vector base (numpy array)
    :return: A vector of scores of dimension x (numpy array)
    """
    if not isinstance(query, np.ndarray):
        raise ValueError("Query should be a numpy array")
    if not isinstance(vector_base, np.ndarray):
        raise ValueError("Vector base should be a numpy array")

    if query.ndim == 1:
        query = query.reshape(1, -1)

    dot_product = np.dot(vector_base, query.T).flatten()
    norms_query = np.linalg.norm(query)
    norms_base = np.linalg.norm(vector_base, axis=1)

    with np.errstate(divide='ignore', invalid='ignore'):
        scores = dot_product / (norms_base * norms_query)
    
    return np.nan_to_num(scores)

def main(temp_file):
    with open(temp_file, "rb") as f:
        data = pkl.load(f)
    
    query = data["query"]
    vector_base = data["vector_base"]

    scores = similarity_calculate(query, vector_base)
    data["scores"] = scores

    with open(temp_file, "wb") as f:
        pkl.dump(data, f)


if __name__=="__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        raise ValueError("Only one argument is allowed")
    elif len(args) == 0:
        raise ValueError("No argument provided")
    
    temp_file = args[0]
    main(temp_file)