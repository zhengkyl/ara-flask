import csv
import os

from ara_flask.ara import Ara

from dotenv import load_dotenv
import ast

load_dotenv()

ara = Ara(os.environ["DB_URI"])

with open("animes.csv") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",")

    header = True
    # found = False
    for row in spamreader:
        if header:
            header = False
            continue

        # if int(row[0]) == 40269:
        #     found = True

        # if not found:
        #     continue

        try:
            ara.add_anime(
                row[0],
                row[1],
                row[2],
                ast.literal_eval(row[3]),
                row[4],
                int(float(row[5])) if row[5] else 0,
                int(float(row[6])) if row[6] else 0,
                row[7],
                int(float(row[8])) if row[8] else 0,
                row[9],
                row[10],
                row[11],
            )
        except:
            print("dupe: " + row[0])

        # break
