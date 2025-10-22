#Import brings in the tools I need.
#requests lets Python talk to other programs over the internet (or locally, like LM Studio)
import requests
#json helps format data in a way computers understand (like a universal language)
import json 
#QdrantClient is the main tool for talking to Qdrant (like how requests talks to LM studio)
from qdrant_client import QdrantClient
#distance tells Qdrant how to measure similarity between embeddings (we'll use COSINE), vectorparams is used for configuration for how big our embeddings are (768 numbers), and pointstruct is a container for packagin up an embedding with its data before sorting
from qdrant_client.models import Distance, VectorParams, PointStruct

#Connect to Qdrant (running on port 6333)
qdrant = QdrantClient(host="localhost", port=6333)

#Create a collection (like a table) to store embeddings
collection_name = "my_first_collection"

#Check if collection already exists, if not, create it
if not qdrant.collection_exists(collection_name):
    #creating it (assuming it doens't exist)
    qdrant.create_collection(
        #naming the collection_name (variable we've set to 'my_first_collection')
        collection_name=collection_name,
        #configuration for the vectors we'll store, the size tells Qdrant 'every embedding I store will be 768 numbers long
        #the distance = COSINE tells Qdrant how to measure similarity between vectors, Cosine similarity means the angle between vectors (standard for text embeddings)
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
    print(f'Created collection: {collection_name}')

#Creating a variable - text - and storing a sentence in it
#text = "The cat sat on the mat"

#Creating a list of sentences (replacing the single sentence stored as a variable above)
sentences = [
    'The cat sat on the mat',
    'A dog played in the park',
    'I love eating pizza',
    'Cats are popular pets',
    'Dogs need daily exercise'
]

#loop to go through each of the sentences listed in the list 'sentences'
for i, text in enumerate(sentences, start=1):
    #requests.post() is like knocking on LM Stuidio's door and handing it a note (the json).
    #the response is LM Studio's reply
    response = requests.post(
        #The address where LM Studio listens for embedding requests
        "http://127.0.0.1:1234/v1/embeddings",
        json={
            "input": text,
            "model": "nomic-embed-text"

        }
    )

    #This extracts just the embedding numbers from LM Studio's response
    #LM Studio sends all kinds of info. back, but I only want the actual numbers
    #This section digs into the response and pulls the numbers and stores them in the variable "embedding"
    embedding = response.json()["data"][0]["embedding"]

    #This prints the original text, then prints how many numbers are in the embedding, and finally shows just the first 10 numbers 
    #(so it doens't flood the screen.)
    print(f"Text: {text}")
    print(f"Embedding length: {len(embedding)}")
    print(f"First 10 numbers: {embedding [:10]}")

    #Store the embedding in Qdrant
    #upsert means update or insert (if an item with this ID already exists, update it, if it doesn't exist, instert it as new)
    qdrant.upsert(
        #Tells qdrant which collection to store in, uses the variable we created earlier ('my_first_collection')
        #Essentially saying "put this in the 'my_first_collection' table"
        collection_name=collection_name,
        #A list of items to store. points is Qdrant's term for 'data entries'. The [] means it's a list, so I can store multiple points at once.
        points=[
            #Packages up everything about this one embedding (fills out a 'form' with everything Qdrant needs)
            PointStruct(
                #gives this embedding a unique ID (like a primary key in a database)
                id=i,
                #embedding represents the 768 numbers we're trying to store
                vector=embedding,
                #this is extra metadata to store alongside the embedding
                payload={'text': text}
            )
        ]
    )

    print(f'\nStored embedding #{i} in Qdrant!')
print(f'All {len(sentences)} embeddings stored in Qdrant.')