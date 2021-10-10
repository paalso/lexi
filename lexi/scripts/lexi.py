#!/usr/bin/env python
import sys
import json
import difflib


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


def capitalize_each_token(collocation):
    return " ".join(token.capitalize() for token in collocation.split())


TEXT_TRANSFORMS = (
    lambda text: text,
    lambda text: text.lower(),
    lambda text: text.capitalize(),
    capitalize_each_token,
    lambda text: text.upper(),
)

LEXICON_FILE = "lexi/data/lexicon.json"
CUTOFF = 0.85


def main():
    args = sys.argv
    if len(args) != 2:
        print("Usage: lexi word or lexi \"words collocation\"")
        sys.exit(2)
    word = args[1]

    with open(LEXICON_FILE, "r") as f:
        lexicon = json.load(f)

        # We process the main possible forms of a word / collocation,
        # in case it is entered with errors in the case of letters
        for text_transform in TEXT_TRANSFORMS:
            transformed_word = text_transform(word)
            dfns = lexicon.get(transformed_word)    # definiens

            if dfns:
                print(transformed_word)
                print("\n".join(dfns))
                sys.exit(0)

        # If no such form is found, we try to find similar words,
        # in case grammatical errors were made
        dfds = lexicon.keys()       # definiendums
        similar_words = difflib.get_close_matches(word, dfds, cutoff=CUTOFF)

        if not word.islower():
            similar_words.extend(
                difflib.get_close_matches(word.lower(), dfds, cutoff=CUTOFF))

        similar_words.extend(
            difflib.get_close_matches(
                capitalize_each_token(word), dfds, cutoff=CUTOFF))

        similar_words.extend(
            difflib.get_close_matches(word.upper(), dfds, cutoff=CUTOFF))

        if len(similar_words) == 0:
            no_word_exit()

        similar_words = sorted(set(similar_words))

        if len(similar_words) == 1:
            similar_word, = similar_words

            answer = input(
                ("Did you mean '{}' instead? Enter y if yes, " +
                 "any other key if no: ").format(similar_word))
            if answer.lower() == "y":
                similar_word_output(lexicon, similar_word)
            no_word_exit()

        # i.e. len(similar_words) > 1
        answer = input(
            ("Did you mean one of the words '{}' instead? " +
             "Enter word id if yes, any other key if no: ")
            .format(numerize_items(similar_words)))
        try:
            answer = int(answer)
        except ValueError:
            no_word_exit()

        if answer < 1 or answer > len(similar_words):
            no_word_exit()

        similar_word = similar_words[answer - 1]
        similar_word_output(lexicon, similar_word)


if __name__ == '__main__':
    main()
