

class Scraper(object):

    def __init__(self, conf):
        self.seed = conf.get("seed")
        self.interval = conf.get("scrape_interval")
        self.corpus_dir = conf.get("corpus_dir")
        self.max_concurrent_tasks = conf.get("max_concurrent_tasks")
        self.request_delay = conf.get("request_delay")
        self.per_domain_delay = conf.get("per_domain_delay")

    def __repr__(self):
        return "Scraper: stuff to see, but not added..."
