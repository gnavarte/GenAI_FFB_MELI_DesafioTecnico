from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

load_dotenv()
app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("La variable de entorno MONGO_URI no está configurada")

# Configuración de conexión a MongoDB con certifi
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["dna_database"]
dna_collection = db["dna_sequences"]

class DNARequest(BaseModel):
    dna: List[str]

def is_mutant(dna):
    n = len(dna)
    sequence_count = 0  # Contador de secuencias encontradas

    # Verificación horizontal
    for row in range(n):
        for col in range(n - 3):
            if dna[row][col] == dna[row][col + 1] == dna[row][col + 2] == dna[row][col + 3]:
                sequence_count += 1
                if sequence_count > 1:
                    return True

    # Verificación vertical
    for row in range(n - 3):
        for col in range(n):
            if dna[row][col] == dna[row + 1][col] == dna[row + 2][col] == dna[row + 3][col]:
                sequence_count += 1
                if sequence_count > 1:
                    return True

    # Verificación diagonal descendente
    for row in range(n - 3):
        for col in range(n - 3):
            if dna[row][col] == dna[row + 1][col + 1] == dna[row + 2][col + 2] == dna[row + 3][col + 3]:
                sequence_count += 1
                if sequence_count > 1:
                    return True

    # Verificación diagonal ascendente
    for row in range(3, n):
        for col in range(n - 3):
            if dna[row][col] == dna[row - 1][col + 1] == dna[row - 2][col + 2] == dna[row - 3][col + 3]:
                sequence_count += 1
                if sequence_count > 1:
                    return True

    return False

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/mutant/")
def check_mutant(dna_request: DNARequest):
    dna_sequence = dna_request.dna
    dna_str = "".join(dna_sequence)

    existing_record = dna_collection.find_one({"dna": dna_str})
    if existing_record:
        if existing_record["is_mutant"]:
            return {"message": "Mutant detected"}
        else:
            raise HTTPException(status_code=403, detail="Forbidden: Not a mutant")

    is_mutant_result = is_mutant(dna_sequence)
    dna_collection.insert_one({"dna": dna_str, "is_mutant": is_mutant_result})

    if is_mutant_result:
        return {"message": "Mutant detected"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden: Not a mutant")

@app.get("/stats")
def stats():
    count_mutants = dna_collection.count_documents({"is_mutant": True})
    count_humans = dna_collection.count_documents({"is_mutant": False})
    total = count_mutants + count_humans
    ratio = count_mutants / total if total > 0 else 0

    return {
        "count_mutant_dna": count_mutants,
        "count_human_dna": count_humans,
        "ratio": ratio
    }
