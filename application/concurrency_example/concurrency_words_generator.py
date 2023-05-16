import concurrent.futures
import itertools
from application.logging.loggers import get_core_logger
from application.config.paths import OUTPUT_DATA_PATH
import os


def write_word_to_file(word: str):
    with open(OUTPUT_DATA_PATH, "a") as file_to_write:
        file_to_write.write(f"{word}\n")


def concurrency_example():

    alphabet: str = os.getenv("ALPHABET")
    word_length: int = int(os.getenv("WORD_LENGTH", default=3))
    start_word: int = int(os.getenv("START_WORD", default=0))
    amount_of_words: str | int = os.getenv("AMOUNT_OF_WORDS", default="")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", default=1000))

    logger = get_core_logger()
    words = []

    if amount_of_words == "":
        amount_of_words = len(alphabet) ** word_length - start_word
    else:
        amount_of_words = int(amount_of_words)
        amount_of_words = min(len(alphabet) ** word_length - start_word, amount_of_words)

    logger.info("Start generate words")
    for i in range(start_word, start_word + amount_of_words, chunk_size):
        chunk_size_actual = min(chunk_size, start_word + amount_of_words - i)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            args = [(alphabet, word_length, index) for index in range(i, i + chunk_size_actual)]
            results = executor.map(generate_word, args)
            words.extend(list(results))

    logger.info("Finish generate words")

    for word in words:
        write_word_to_file(word)


def generate_word(args: tuple[str, int, int]) -> str:
    logger = get_core_logger()
    logger.info(f"Generate word with args: {args}")

    alphabet, word_length, index = args
    indices = itertools.product(range(len(alphabet)), repeat=word_length)
    indices = itertools.islice(indices, index, None, None)
    word = "".join([alphabet[i] for i in next(indices)])
    return word
