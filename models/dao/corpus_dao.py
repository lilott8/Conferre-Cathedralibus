import colorlog
from models.corpus import Corpus


class CorpusDao(object):

    def __init__(self, db):
        self.logger = colorlog.getLogger(classmethod.__name__)
        self.db = db

    async def save(self, url: str, domain: str, path: str, title: str, hash: str):
        self.db.add(Corpus(
            url=url,
            domain=domain,
            path=path,
            title=title,
            hash=hash
        ))
        await self.db.commit()