
def derive_collection_name(topic: str) -> str:
    return f"c_{topic[19:].replace('/','_')}"