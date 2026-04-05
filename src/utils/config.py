import json


PATH = "src/utils/config.json"


def get_data() -> dict:
    return json.load(open(PATH, "r"))["config"]


def edit_config(place, value):
    config = json.load(open(PATH, "r"))

    if len(place) == 1:
        config["config"][place[0]] = value
    elif len(place) == 2:
        config["config"][place[0]][place[1]] = value

    json.dump(config, open(PATH, "w"))


def reset_config():
    config = json.load(open(PATH, "r"))
    config["config"] = config["reset"]
    json.dump(config, open(PATH, "w"))
