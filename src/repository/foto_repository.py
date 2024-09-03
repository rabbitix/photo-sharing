from src.repository.adapters.queue_adapter import QueueAdapter


class FotoRepository:
    def __init__(self):
        self.queue_adapter = QueueAdapter()

    async def enqueue_sending_picture(self, item, **kwargs):
        await self.queue_adapter.enqueue(item, **kwargs)

    async def get_queue_worker(self):
        await self.queue_adapter.queue_worker()
