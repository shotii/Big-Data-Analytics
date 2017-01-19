from collections import defaultdict


@outputSchema("m:map[]")
def word_count(bag):
    word_dict = defaultdict(int)

    if bag is None:
        return word_dict

    for tuple in bag:
        # The bag has tuples which have only one entry and that is the text
        line = tuple[0]
        
        if line is None:
            continue

        for word in line.split():
            word_dict[word] = word_dict[word] + 1

    return word_dict
