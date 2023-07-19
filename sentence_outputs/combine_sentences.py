
fi1 = open("two_articles_saved.txt", "r")
fi2 = open("two_articles.txt", "r")

fo = open("two_articles_combined.txt", "w")
for line in fi1:
    fo.write(line)

for line in fi2:
    fo.write(line)

