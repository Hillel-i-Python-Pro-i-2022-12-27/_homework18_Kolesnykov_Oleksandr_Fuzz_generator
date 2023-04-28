import concurrent.futures
import itertools
from string import ascii_lowercase, digits
from application.logging.loggers import get_core_logger
from application.config.paths import OUTPUT_DATA_PATH


def get_data():
    alphabet = "".join([ascii_lowercase, digits])

    word_length = input("Введите длину слов (цифрой): ")
    if not word_length.isdigit():
        word_length = 3
    else:
        word_length = int(word_length)

    start_word = input("Введите номер слова, с которого начнём старт или нажмите Enter что бы начать с начала: ")
    if start_word.isdigit():
        start_word = int(start_word)
    else:
        start_word = 0

    amount_of_words = input("Введите желаемое количество слов (цифрой)или нажмите Enter что бы создать все варианты: ")
    if amount_of_words.isdigit():
        amount_of_words = int(amount_of_words)
    else:
        amount_of_words = None

    return alphabet, word_length, start_word, amount_of_words


def write_word_to_file(word):
    with open(OUTPUT_DATA_PATH, "a") as file_to_write:
        file_to_write.write(f"{word}\n")


def concurrency_example():
    alphabet, word_length, start_word, amount_of_words = get_data()
    logger = get_core_logger()
    words = []

    if amount_of_words is None:
        amount_of_words = len(alphabet) ** word_length - start_word
    else:
        amount_of_words = min(len(alphabet) ** word_length - start_word, amount_of_words)

    logger.info("Start generate words")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        args = [(alphabet, word_length, index) for index in range(start_word, start_word + amount_of_words)]
        results = executor.map(generate_word, args)
        words = list(results)

    logger.info("Finish generate words")
    for word in words:
        # logger.info(f'{word}')
        write_word_to_file(word)


def generate_word(args):
    logger = get_core_logger()
    logger.info(f"Generate word with args: {args}")

    alphabet, word_length, index = args
    indices = itertools.product(range(len(alphabet)), repeat=word_length)
    indices = itertools.islice(indices, index, None, None)
    indices = list(indices)[0]
    return "".join([alphabet[i] for i in indices])
