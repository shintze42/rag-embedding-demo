#tools needed for searching
import requests
from qdrant_client import QdrantClient

#connect to Qdrant
qdrant = QdrantClient(host='localhost', port=6333)

#same collection we stored the data in
collection_name = 'my_first_collection'

#the text I want to search for
search_text = 'Pizza is healthy for the soul.'

print(f'Searching for: "{search_text}"')
print('=' * 50)

#Convert search text to embedding using LM Studio
response = requests.post(
        #The address where LM Studio listens for embedding requests
        "http://127.0.0.1:1234/v1/embeddings",
        json={
            "input": search_text,
            "model": "nomic-embed-text"

        }
    )

#Extract the embedding
search_embedding = response.json()['data'][0]['embedding']

print(f'Converted search text to {len(search_embedding)} numbers')

#Search Qdrant for similar embeddings
results = qdrant.query_points(
    collection_name=collection_name,
    query=search_embedding,
    limit=3
).points

print(f'\nTop 3 most similar results: \n')

#Display the results
for i, result in enumerate(results, start=1):
    print(f'{i}. "{result.payload["text"]}"')
    print(f' Similarity score: {result.score:.4f}')
    print()