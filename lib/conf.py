import re


# This just uses a single pass over the text, opposed to multiple .replace() calls.
def multiple_replace(d, text):
    if not d:
        return text
    # Create a regular expression  from the dictionary keys
    regex = re.compile("|".join(map(re.escape, d.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda m: d[m.group()], text)


def insert_conf(data, config, filename=""):
    # All the starting positions of __EPSILON_
    locations = [m.start() for m in re.finditer('__EPSILON_', data)]

    # Extract a dict of configuration
    d = {}
    for loc in locations:
        i = int(loc)
        while data[i].isalnum() or data[i] == "_":
            i += 1
        key = data[loc:i]
        try:
            d[key] = config[key.replace("__", "").replace("EPSILON_", "")]
        except KeyError:
            print("Invalid key %s in file %s" % (key, filename))
    # replace it
    return multiple_replace(d, data)
