from application.concurrency_example.concurrency_words_generator import concurrency_example
from application.logging.init_logging import init_logging


def main():
    concurrency_example()


if __name__ == "__main__":
    init_logging()
    main()
