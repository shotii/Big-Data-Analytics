import re
import csv

class ImdbReader(object):
    filename = ""

    def __init__(self, filename):
        self.filename = filename

    def get_movies_and_quotes(self):
        counter = 0
        current_movie = ""
        movie_quotes = dict()

        with open(self.filename, "r", encoding="ISO-8859-1") as imdb_data:
            for line in imdb_data:
                # Write movie title to dict as key
                if line.startswith("#"):
                    movie_quotes[line] = list()
                    current_movie = line
                # Skip the introductory text
                elif counter < 14:
                    counter += 1
                # Skip some strange parts starting with brackets
                elif line.startswith("["):
                    continue
                # Obviously, lines starting with space belong to previous quotes
                elif re.match(r'\s', line):
                    if movie_quotes[current_movie]:
                        movie_quotes[current_movie][-1] += line
                elif line not in ['\n', '\r\n']:
                    quote = line.split(":")
                    # Since none of the above condition hold, its hard to say to which part this line belongs, skip it
                    if len(quote) == 1:
                        continue
                    else:
                        movie_quotes[current_movie].append(quote[1])

        return movie_quotes



def main():
    imdb_reader = ImdbReader("imbdb-quotes.txt")
    dic = imdb_reader.get_movies_and_quotes()

    count2 = 0
    # Write the dictionary to csv file
    with open("quotes.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for movie in dic:
            if count2 > 10:
                break
            count2 += 1
            tmpList = list()
            tmpList.append(movie)

            for quote in dic[movie]:
                tmpList.append(quote)

            writer.writerow(tmpList)

    count = 0
    #for x in dic:
    #    if count > 10:
    #        break
    #    count += 1
    #    print(x)
    #    print(dic[x])

if __name__ == "__main__":
    main()



