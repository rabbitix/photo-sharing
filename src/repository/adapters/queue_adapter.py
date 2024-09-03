import asyncio
import logging


class QueueAdapter:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def enqueue(self, item, **kwargs):
        job = (item, kwargs)
        await self.queue.put(job)

    async def queue_worker(self):
        while True:
            job = await self.queue.get()
            logging.info("get a new job. remaining jobs: %s" % self.queue.qsize())
            await job[0](**job[1])
