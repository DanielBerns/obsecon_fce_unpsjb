from pathlib import Path
from context import components
from collections import Counter
from components.helpers import get_resource

home = Path("~", "Data", "mynlp").expanduser()
origin_path = get_resource(home, "article_code", ".csv")
target_path = get_resource(home, "article_code", ".txt")
cc = Counter()

codes = list()
with open(origin_path, "r") as origin:
    for line in origin:
        info = line[:-1]
        parts = info.split(",")
        ll = len(parts)
        cc[ll] += 1
        for pp in parts:
            if pp:
                codes.append(pp[1:-1])
        print(info, "----------", ll)
with open(target_path, "w") as target:
    for number, value in enumerate(set(codes)):
        print(number, value)
        target.write(f'"{value:s}",' + "\n")
