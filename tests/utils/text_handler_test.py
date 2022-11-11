from time import time
from tests.utils.test_text import test_text  # 200개 문장
from utils.text.text_handler import string_to_sentence_list


def test_string_to_sentence_list():
    sut = string_to_sentence_list(test_text)
    assert isinstance(sut, list)


def test_custom_benchmark():
    start = time()
    string_to_sentence_list(test_text * 1000)  # 문장 20만개
    end = time()
    assert end - start <= 2


def test_benchmark(benchmark):
    benchmark(string_to_sentence_list, test_text)
