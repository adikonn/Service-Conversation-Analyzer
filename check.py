from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
model_kwargs = {"device": "cuda"}
encode_kwargs = {"normalize_embeddings": False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)


docs = []
with open("reg.txt", encoding="UTF8") as f:
    for line in f.readlines():
        docs.append(Document(line))


db = FAISS.from_documents(docs, embeddings)


def hybrid_search(query):
    return BM25Retriever.from_documents(db.similarity_search(query, k=5), k=3).invoke(
        query
    )


# print(hybrid_search("машинист"))

from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

fstring = """Respond in russian. Respond Y or N based on how well the following message follows the specified format. Grade only based on the format:

Format: {format}

DATA:
---------
Message: {message}
---------
Write out a short explanation in russian for each criterion. You should explicitly specify the reason, then respond with Y or N on a new line. Answer only Y or only N not both. Keep it really short and precise. Speak russian only."""

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(fstring)


def validate(format, message):
    return llm.invoke(prompt.format(format=format, message=message))


def check_msg(message):
    ans = []
    for f in hybrid_search(message):
        print(f, message)
        output = validate(f.page_content, message)
        print(output)
        ans.append((output, output.split("\n")[-1].strip() == "Y"))
    reasons, states = zip(*ans)
    return any(states), reasons
