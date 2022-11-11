def string_to_sentence_list(text: str):
    sentences = []
    first_index = 0
    for index in range(len(text)):
        if text[index] in [".", "!", "?"]:
            sentence = text[first_index : index + 1].strip()
            if len(sentence) > 0:
                sentences.append(sentence)
            first_index = index + 1
    return sentences
