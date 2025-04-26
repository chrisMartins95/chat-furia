# train_model.py
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

def train_model(save_path="model.pkl", vectorizer_path="vectorizer.pkl"):
    intents = {
        "greeting": ["oi", "olá", "bom dia", "boa tarde", "e aí", "oi chatbot", "salve"],
        "favorite_team": ["qual seu time favorito?", "quem é seu time?", "time favorito"],
        "next_game": ["quando é o próximo jogo?", "qual o próximo jogo?", "tem jogo logo?"],
        "bot_name": ["qual seu nome?", "como te chamo?", "qual é o seu nome?"],
        "how_are_you": ["como você está?", "tudo bem?", "como você tá?", "tá bem?"],
    }

    X = []
    y = []
    for intent, examples in intents.items():
        for example in examples:
            X.append(example)
            y.append(intent)

    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vectorized, y)

    # Salvar modelo treinado
    with open(save_path, "wb") as f:
        pickle.dump(model, f)

    # Salvar o vectorizer também
    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)

    return model, vectorizer
