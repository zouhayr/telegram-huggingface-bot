import requests

# Remplacez ceci par votre jeton Hugging Face
HF_TOKEN = "HF_TOKEN"
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased"

# Fonction pour interroger l'API Hugging Face
def test_huggingface_api(text):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": text}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Vérifie si la requête a réussi (code 200)
        print("Réponse brute de l'API :", response.text)  # Affiche la réponse brute
        return response.json()  # Essaie de convertir en JSON
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {e}")
        print(f"Code de statut : {response.status_code}")
        print(f"Réponse brute : {response.text}")
        return None
    except ValueError:
        print("Erreur : La réponse n'est pas un JSON valide")
        print(f"Réponse brute : {response.text}")
        return None

# Tester l'API avec un texte simple
if __name__ == "__main__":
    test_text = "Bonjour, comment ça va ?"
    result = test_huggingface_api(test_text)
    if result:
        print("Résultat de l'API (JSON décodé) :", result)
