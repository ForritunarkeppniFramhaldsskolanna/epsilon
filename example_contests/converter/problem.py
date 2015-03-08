import yaml
data = None
with open("problem.yml", "r") as f:
    data = f.read()
data = yaml.load(data)
i = 0
for example in data["examples"]:
    with open("data/sample/%d.in" % i, "w") as f:
        f.write(example["input"])
    with open("data/sample/%d.ans" % i, "w") as f:
        f.write(example["output"])
    i += 1
