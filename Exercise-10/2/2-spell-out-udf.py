from num2words import num2words

@outputSchema("text:chararray")
def replace_numbers(lower_bound, upper_bound, text):
    new_text = list()
    intervall = range(lower_bound, upper_bound+1)

    new_text = list()
    # Loop through text line by line and replace numbers in intervall lb and ub
    for line in text.split('\n'):
        new_line = list()

        for word in line.split():
            for val in intervall:
                if str(val) in word:
                    word = word.replace(str(val), num2words(val))

            new_line.append(word)

        new_text.append(' '.join(new_line))

    return '\n'.join(new_text)

