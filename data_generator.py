# Yasmin Heimann

import sys
import pandas as pd
import numpy as np
from random import shuffle, sample, choices
import re

pattern = re.compile(r"[A-Za-z0-9_\s:]+")
PRE_PROCESS = False
TO_EXCEL = False

MOVIE_SIZES = [5, 10, 20, 40, 60, 100, 150, 200, 500, 750]
NAMES_SIZE = [4, 15, 25, 20, 22, 50, 40, 80, 300, 400]
RATES = ["NA", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
BIAS = [60, 3, 3, 3, 4, 4, 4, 5, 5, 5, 4]
CATEGORIES = ["Dramatic", "Funny", "Scary", "Surprising", "Weird", "Artistic", "WellPlayed"]
CAT_RATES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
CAT_SIZES = [5, 10, 60, 120]

def check_shuffle(p_names, names):
    pre = np.array(pd.read_excel(p_names, header=None))
    sum = 0
    for i in range(len(pre)):
        if pre[i] == names[i]:
            sum += 1
    if (sum/len(pre)) < 0.2:
        return 0
    return -1


def text_pattern(s):
    if type(s) is not str:
        return False
    found = pattern.match(s)
    if found is not None and len(found.group(0)) == len(s):
        return True
    return False


def fix_str(s):
    s = s.replace(" ", "")
    s = s.replace(":", "_")
    return s


def pre_process_list(base_path):
    # read files
    p_movies = base_path + "movies_raw.xlsx"
    p_names = base_path + "names_raw.xlsx"
    movies = np.array(pd.read_excel(p_movies, header=None))
    names = np.array(np.array((pd.read_excel(p_names, header=None))))
    # distinct names
    # movies = np.unique(movies)
    names = np.unique(names)
    # shuffle(movies)
    shuffle(names)

    # only A-Za-z1-9, no spaces
    movies = pd.DataFrame([fix_str(m[0]) for m in movies if text_pattern(m[0])])
    names = pd.DataFrame(names)
    if TO_EXCEL:
        movies.to_excel(base_path + "movies.xlsx", index=False)
        names.to_excel(base_path + "names.xlsx", index=False)
    return movies, names


def create_output1(i, sampled_movies, base_path):
    for size in CAT_SIZES:
        row_samples = [choices(CAT_RATES, k=size) for j in range(MOVIE_SIZES[i])]
        for k, row in enumerate(row_samples):
            row.insert(0, sampled_movies[k])
        #categories = [''] * (size + 1)
        df = pd.DataFrame(data=np.array(row_samples)) #, columns=categories)
        df.to_csv(base_path + "outputs\\output1_" + str(MOVIE_SIZES[i]) + "set_" + str(size) + ".txt", sep=" ", index=False, header=False)


def create_output2(names, i, sampled_movies, base_path):
    sampled_names = sample(names, NAMES_SIZE[i])
    row_samples = [choices(RATES, BIAS, k=MOVIE_SIZES[i]) for j in range(NAMES_SIZE[i])]
    # edge cases
    for k, row in enumerate(row_samples):
        # if none NA - add one NA
        if "NA" not in row:
            row[0] = "NA"
        # if all NA - add one random rate
        na_count = row.count("NA")
        if na_count == len(row):
            row[0] = 8
        row.insert(0, sampled_names[k])
    sampled_movies.insert(0, '')
    df = pd.DataFrame(data=np.array(row_samples), columns=sampled_movies)
    df.to_csv(base_path + "outputs\\output2_" + str(MOVIE_SIZES[i]) + ".txt", sep=" ", index=False)


def generate_data(base_path):
    if PRE_PROCESS:
        movies, names = pre_process_list(base_path)
    else:
        movies = [m[0] for m in np.array(pd.read_excel(base_path + "movies.xlsx"))]
        names = [m[0] for m in np.array(pd.read_excel(base_path + "names.xlsx"))]
    for i in range(len(MOVIE_SIZES)):
        sampled_movies = sample(movies, MOVIE_SIZES[i])
        create_output1(i, sampled_movies, base_path)
        shuffle(sampled_movies)
        create_output2(names, i, sampled_movies, base_path)


if __name__ == "__main__":
    generate_data(sys.argv[1])

# categories names
# row_samples = [choices(CAT_RATES, k=len(CATEGORIES)) for j in range(MOVIE_SIZES[i])]
#         for k, row in enumerate(row_samples):
#             row.insert(0, sampled_movies[k])
#         categories = CATEGORIES
#         categories.insert(0, '')

