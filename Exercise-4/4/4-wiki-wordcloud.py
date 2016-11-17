from wordcloud import WordCloud
import csv
import sys

csv.field_size_limit(sys.maxsize)

categories = {}


# Since the categories are provided in the file, it is possible to get them straight instead of using an extra function
def main(search_word, word_threshold):
    # Open the wiki file
    csv_file = open("enwiki-clean.csv", "r")
    reader = csv.reader(csv_file)

    for _, title, _, text, categories_wiki in reader:
        # Count how often the search term appears in the text of an article
        word_occurrence_number = text.count(search_word)

        # Sanatize the categories list
        categories_wiki = categories_wiki.replace("[", "")
        categories_wiki = categories_wiki.replace("]", "")

        # Extract all categories that are seperated by ","
        categories_wiki = categories_wiki.split(",")

        if word_occurrence_number >= word_threshold:
            for category in categories_wiki:
                # Look up in dictionary if category exist and increment its value, else set it to 1.
                categories[category] = categories.get(category, 0) + 1

    wordcloud = WordCloud(relative_scaling = 0.5)
    wordcloud.generate_from_frequencies(list(categories.items()))

    image = wordcloud.to_image()
    print(image.size)
    image.save(search_word + ".png")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
    print(categories)