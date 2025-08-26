from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import re

documento = Path("docs/politicas.pdf")
if documento.suffix == ".pdf":
    loader = PyPDFLoader(str(documento))
else:
    loader = TextLoader(str(documento), encoding="utf-8")
docs = loader.load()  

def buscar_resposta_sentenca(docs, pergunta, top_n=1):
    pergunta_lower = pergunta.lower()
    keywords = [w for w in re.findall(r'\w+', pergunta_lower) if len(w) > 2]

    candidatos = []

    for doc in docs:
        texto = doc.page_content
        texto = texto.replace("\n", " ")
        sentencas = re.split(r'(?<=[.!?])\s+', texto)
        for s in sentencas:
            s_lower = s.lower()
            score = sum(1 for kw in keywords if kw in s_lower)
            if score > 0:
                candidatos.append((score, s.strip()))

    candidatos.sort(reverse=True)
    if candidatos:
        return " ".join([c[1] for c in candidatos[:top_n]])
    else:
        return "Desculpe, não encontrei a resposta no documento."

print("🤖 Chatbot OFFLINE iniciado! (digite 'sair' para encerrar)\n")
while True:
    pergunta = input("Você: ")
    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("🤖 Chatbot: Até mais!")
        break
    resposta = buscar_resposta_sentenca(docs, pergunta)
    print("🤖 Chatbot:", resposta, "\n")
