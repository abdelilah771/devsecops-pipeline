# 🐍 Guide : Récupération des Logs avec FastAPI (Python)

Ce document explique comment créer un microservice léger avec **FastAPI** pour lire et analyser les logs stockés dans MongoDB par le service principal (Node.js/Express).

## 📋 Prérequis

Puisque les données sont déjà dans MongoDB, nous allons utiliser **Motor** (le driver asynchrone MongoDB pour Python) et **Pydantic** pour la validation des données.

### 1. Installation des dépendances

Créez un dossier pour votre service Python et installez les paquets nécessaires :

```bash
pip install fastapi "uvicorn[standard]" motor pydantic python-dotenv
```

## 🚀 Implémentation

Voici le code complet pour une application FastAPI (`main.py`) qui se connecte à votre base de données existante.

### Structure du Fichier `main.py`

```python
import os
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, BeforeValidator
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from typing_extensions import Annotated

# 1. Configuration & Connexion BDD
load_dotenv() # Charge les variables d'environnement du fichier .env

# Récupérer l'URL depuis le .env (la même que votre projet Node.js)
MONGO_URL = os.getenv("DATABASE_URL")
if not MONGO_URL:
    raise ValueError("La variable DATABASE_URL n'est pas définie dans le fichier .env")

# Connexion au client MongoDB
client = AsyncIOMotorClient(MONGO_URL)
# Important : Prisma stocke généralement les données dans une base spécifique, souvent définie dans l'URL
# Si votre URL est mongodb://host:port/ma_base, on récupère "ma_base"
db = client.get_default_database() 
logs_collection = db["Log"] # Nom de la collection définie dans Prisma ("Log")

app = FastAPI(title="LogReader Service", description="API de lecture des logs via FastAPI")

# 2. Modèles de Données (Pydantic)
# Ces modèles doivent correspondre à votre schéma Prisma

# Helper pour gérer les ObjectId de MongoDB comme des chaînes de caractères
PyObjectId = Annotated[str, BeforeValidator(str)]

class LogSchema(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    log_data: dict | str | list  # Peut être JSON ou String selon votre schéma
    repo_name: str
    author: str
    pipeline_name: str
    run_id: str
    timestamp_original: Optional[datetime] = None
    timestamp_received: datetime
    provider: str

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

# 3. Endpoints (Routes)

@app.get("/")
async def root():
    return {"message": "Service de lecture de logs FastAPI opérationnel"}

@app.get("/logs", response_model=List[LogSchema])
async def get_logs(
    skip: int = 0, 
    limit: int = 100, 
    provider: Optional[str] = None,
    repo_name: Optional[str] = None
):
    """
    Récupère une liste de logs avec pagination et filtres optionnels.
    """
    query = {}
    
    # Ajout des filtres si présents
    if provider:
        query["provider"] = provider.upper() # Assure la correspondance avec l'ENUM Prisma (GITHUB, GITLAB...)
    if repo_name:
        query["repo_name"] = repo_name

    # Récupération asynchrone depuis MongoDB
    cursor = logs_collection.find(query).skip(skip).limit(limit).sort("timestamp_received", -1)
    logs = await cursor.to_list(length=limit)
    
    return logs

@app.get("/logs/{log_id}", response_model=LogSchema)
async def get_log_by_id(log_id: str):
    """
    Récupère un log unique par son ID MongoDB.
    """
    from bson import ObjectId
    
    try:
        obj_id = ObjectId(log_id)
    except:
        raise HTTPException(status_code=400, detail="Format d'ID invalide")

    log = await logs_collection.find_one({"_id": obj_id})
    
    if log is None:
        raise HTTPException(status_code=404, detail="Log non trouvé")
        
    return log

@app.get("/stats/providers")
async def get_provider_stats():
    """
    Exemple d'agrégation : Compte le nombre de logs par provider.
    """
    pipeline = [
        {"$group": {"_id": "$provider", "count": {"$sum": 1}}}
    ]
    stats = await logs_collection.aggregate(pipeline).to_list(length=None)
    return stats
```

## ⚙️ Configuration

1.  Assurez-vous d'avoir un fichier `.env` à la racine de votre dossier Python contenant l'URL de connexion :
    ```env
    DATABASE_URL="mongodb://votre_utilisateur:votre_mot_de_passe@localhost:27017/votre_base_de_donnees"
    ```
    *(Utilisez la même chaîne que dans le fichier `.env` de votre projet Node.js)*.

## 🏃‍♂️ Lancement

Lancez le serveur de développement :

```bash
uvicorn main:app --reload
```

L'API sera accessible sur `http://127.0.0.1:8000`.

## 📚 Documentation Automatique

FastAPI génère automatiquement une documentation interactive. Une fois le serveur lancé, visitez :

*   **Swagger UI :** `http://127.0.0.1:8000/docs`
*   **ReDoc :** `http://127.0.0.1:8000/redoc`

## 💡 Pourquoi utiliser FastAPI pour la lecture ?

1.  **Performance** : FastAPI est extrêmement rapide et gère nativement l'asynchrone, idéal pour lire de grands volumes de logs.
2.  **Data Science** : En utilisant Python, vous pouvez facilement intégrer des bibliothèques comme *Pandas* ou *Scikit-learn* pour analyser les logs, détecter des anomalies ou générer des statistiques complexes directement depuis cet endpoint.
