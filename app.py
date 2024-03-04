from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from jina import Document, Flow
import pickle

# Load indexed data from pickle file
with open('indexed_data.pickle', 'rb') as handle:
    indexed_data = pickle.load(handle)

# Create Flow for querying
f = Flow().add(name='encoder', uses='jinahub://TransformerTorchEncoder/latest', install_requirements=True)\
         .add(uses='jinahub://AnnLiteIndexer/latest', install_requirements=True,
              uses_with={'columns': [('supplier', 'str'), ('price', 'float'),
                                     ('attr_t_product_type', 'str'), ('attr_t_product_colour', 'str')],
                         'n_dim': 768})

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    tags: dict

@app.post("/search/", response_model=List[SearchResult])
async def search(query_request: QueryRequest):
    query_text = query_request.query
    query = Document(text=query_text)
    print("Hello")
    # Search for similar documents
    with f:
        results = f.search(query)

    # Process results and prepare for rendering
    search_results = []
    for match in results[0].matches:
        search_results.append(SearchResult(tags=match.tags))
    print(search_results)
    return search_results


