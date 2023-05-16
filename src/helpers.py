from sentence_transformers import SentenceTransformer

name = "paraphrase-albert-small-v2"
model = SentenceTransformer(name)


# used for both training and querying
def embed_func(batch):
    return [model.encode(sentence) for sentence in batch]


def create_manifest_url(domain: str):
    return "https://{domain}/.well-known/ai-plugin.json".format(domain=domain)
