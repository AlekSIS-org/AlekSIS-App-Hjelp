import json

def parse_icon_names():
    icons = []

    with open('icons_meta.json') as json_file:
        data = json.load(json_file)

    for obj in data:
        name = obj["name"]
        icons.append((name, name))

    return icons

if __name__ == "__main__":
    print(parse_icon_names())
