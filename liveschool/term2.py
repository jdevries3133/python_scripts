import csv
from pprint import pprint

from teacherhelper import Helper


hp = Helper.read_cache()


with open("data.csv", "r") as fp:
    rd = csv.DictReader(fp)

    map = {}
    name_to_n_zeroes = {}
    for row in rd:
        key = row["Date"] + row["Student"]

        map.setdefault(key, 0)
        map[key] += 1

        if map[key] == 3:
            name_to_n_zeroes.setdefault(row["Student"], 0)
            name_to_n_zeroes[row["Student"]] += 1

print("--- Zero Counts ---")
for name, n_zeroes in name_to_n_zeroes.items():
    print(name, n_zeroes)
    st = hp.find_nearest_match(name)
    if st is None:
        raise Exception(f"no match for {name}")

    st.n_zeroes = n_zeroes


for hr in hp.homerooms.values():
    print("\n")
    print("##### ", hr.teacher, " #####")
    for s in hr.students:
        if hasattr(s, "n_zeroes"):
            print(s.name, s.n_zeroes)
