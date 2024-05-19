from data.db_session import global_init, create_session
from data.chunks import Chunks
from data.requests_table import Request

global_init()

ses = create_session()


def add_chunk(chunk: str):
    new = Chunks(text=chunk)
    ses.add(new)
    ses.commit()
    return new.id


def add_to_faiss(chunk_id: str):
    chunk_id = int(chunk_id)
    chunk = ses.query(Chunks).filter(Chunks.id == chunk_id).first()
    req = Request(text=chunk.text)
    ses.add(req)
    return ses.commit()
