from task3_hashtable_strings import HashTableChaining


def count_word_occurrences(text):
    table = HashTableChaining()
    result = []

    words = text.split()

    for word in words:
        prev = table.get(word)
        if prev is None:
            table.put(word, 1)
            result.append(1)
        else:
            table.put(word, prev + 1)
            result.append(prev + 1)

    return result


if __name__ == "__main__":
    print("WORD OCCURRENCE COUNTER")

    text1 = "the cat sat on the mat the cat"
    print("\nInput: ", text1)
    print("Output:", " ".join(map(str, count_word_occurrences(text1))))
    
    text2 = "Hello hello HELLO hello"
    print("\nInput: ", text2)
    print("Output:", " ".join(map(str, count_word_occurrences(text2))))

    text3 = "word   word    word"
    print("\nInput: ", repr(text3))
    print("Output:", " ".join(map(str, count_word_occurrences(text3))))

    text4 = "single"
    print("\nInput: ", text4)
    print("Output:", " ".join(map(str, count_word_occurrences(text4))))

    text5 = "   "
    print("\nInput: ", repr(text5))
    print("Output:", count_word_occurrences(text5))