#!/usr/bin/env python
import difflib
import json
import sys
import lexi

LEXICON_FILE = "lexi/data/data.json"
CUTOFF = 0.85


def numerize_items(items):
    return ", ".join(f"{i} - {item}" for i, item in enumerate(items, 1))


def no_word_exit():
    print("The word doesn't exist. Please check it")
    sys.exit(1)


def similar_word_output(lexicon, similar_word):
    dfns = lexicon[similar_word]
    print(similar_word)
    print("\n".join(dfns))
    sys.exit(0)


def main():
    args = sys.argv
    if len(args) != 2:
        print("Usage: lexi word or lexi \"words collocation\"")
        sys.exit(2)
    word = args[1]
    print(word)

    with open(LEXICON_FILE, "r") as f:
        lexicon = json.load(f)
        dfds = lexicon.keys()

        dfns = lexicon.get(word)
        if dfns:
            print("\n".join(dfns))
            sys.exit(0)

        similar_words = difflib.get_close_matches(word, dfds, cutoff=CUTOFF)

        if len(similar_words) == 0:
            no_word_exit()

        if len(similar_words) == 1:
            similar_word, = similar_words
            answer = input(
                ("Did you mean '{}' instead? Enter Y if yes, " + \
                "any other key if no: ").format(similar_word))
            if answer.upper() == "Y":
                similar_word_output(lexicon, similar_word)
            no_word_exit()

        # i.e. len(similar_words) > 1
        answer = int(input(
            ("Did you mean one of the words '{}' instead? " + \
            "Enter word id if yes, any other key if no: ")
            .format(numerize_items(similar_words))))
        try:
            answer = int(answer)
        except:
            no_word_exit()

        if answer < 1 or answer > len(similar_words):
            no_word_exit()

        similar_word = similar_words[answer - 1]
        similar_word_output(lexicon, similar_word)


if __name__ == '__main__':
    main()
