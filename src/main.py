import logging
import sys

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

load_dotenv(".env")


def main():
    from src.app import App
    from src.config import Config

    config = Config()
    app = App(config)
    app.run()


if __name__ == "__main__":
    main()
