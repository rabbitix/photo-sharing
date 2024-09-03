import logging

import uvicorn
from dotenv import load_dotenv

from src.configs.runtime_config import RuntimeConfig

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(
        "main:app",
        host=RuntimeConfig().SERVE_HOST,
        port=RuntimeConfig().SERVE_PORT,
    )
