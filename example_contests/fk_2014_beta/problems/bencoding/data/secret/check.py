import sys

# def parse(s):
#     at = 0

#     def next():
#         if at == len(s):
#             return None

#         if s[at] == 'i':
#             at += 1
#             no = 0
#             while at < len(s) and ord('0') <= ord(s[at]) <= ord('9'):
#                 no = no * 10 + (ord(s[at]) - ord('0'))
#                 at += 1

#             if at == len(s) or s[at] != 'e':
#                 return None

#             at += 1
#             return no
#         elif s[at] == 'l':
#             at += 1
#             l = []

#             while at < len(s) and s[at] != 'e':
#                 it = next()
#                 if it is None:
#                     return None
#                 l.append(it)

#             if at == len(s) or s[at] != 'e':
#                 return None

#             at += 1
#         elif s[at] == 'd':
#             at += 1
#             d = {}

#             while at < len(s) and s[at] != 'e':
#                 k = next()
#                 if k is None:
#                     return None
#                 v = next()
#                 if v is None:
#                     return None

#                 if type(k) is not str:
#                     return None

#                 if k in d:
#                     return None

#                 d[k] = v

#             if at == len(s) or s[at] != 'e':
#                 return None

#             at += 1
#         elif ord('0') <= ord(s[at]) <= ord('9'):
#             l = 0
#             while at < len(s) and ord('0') <= ord(s[at]) <= ord('9'):
#                 l = l * 10 + (ord(s[at]) - ord('0'))
#                 at += 1

#             if at == len(s) or s[at] != ':':
#                 return None

#             at += 1

#             res = ''
#             for _ in range(l):
#                 if at == len(s):
#                     return None

#                 res += s[at]
#                 at += 1

#             return res
#         else:
#             return None

#     res = next()
#     if at != len(s):
#         return None

#     return res

# OOPS. Parsed the wrong type of string. Well, gotta start over..

def parse(s):
    global at
    at = 0
    def next():
        global at
        if at == len(s):
            return None

        if s[at] == '"':
            at += 1
            res = ''
            while at < len(s) and s[at] != '"':
                res += s[at]
                at += 1

            if at == len(s) or s[at] != '"':
                return None

            at += 1
            return res
        elif ord('0') <= ord(s[at]) <= ord('9'):
            res = 0
            while at < len(s) and ord('0') <= ord(s[at]) <= ord('9'):
                res = res * 10 + (ord(s[at]) - ord('0'))
                at += 1

            return res
        elif s[at] == '[':
            at += 1
            res = []
            while at < len(s) and s[at] != ']':
                n = next()
                if n is None:
                    return None
                res.append(n)
                if at == len(s):
                    return None

                if s[at] == ']':
                    break
                elif s[at] == ',':
                    at += 1
                    continue
                else:
                    return None

            if at == len(s) or s[at] != ']':
                return None

            at += 1
            return res
        elif s[at] == '{':
            at += 1
            res = {}
            while at < len(s) and s[at] != '}':
                k = next()
                if k is None or type(k) is not str:
                    return None

                if at == len(s) or s[at] != ':':
                    return None

                at += 1
                v = next()
                if v is None:
                    return None

                if k in res:
                    return None

                res[k] = v

                if at == len(s):
                    return None

                if s[at] == '}':
                    break
                elif s[at] == ',':
                    at += 1
                    continue
                else:
                    return None

            if at == len(s) or s[at] != '}':
                return None

            at += 1
            return res
        else:
            return None

    res = next()
    if at != len(s):
        return None

    return res


def check(obtained, expected):

    o = parse(obtained.strip())
    e = parse(expected.strip())

    assert e is not None

    return o == e

def main():
    obtained = sys.argv[1]
    expected = sys.argv[2]

    if obtained == '-':
        obtained = sys.stdin.read()
    else:
        with open(obtained, 'r') as f:
            obtained = f.read()

    if expected == '-':
        expected = sys.stdin.read()
    else:
        with open(expected, 'r') as f:
            expected = f.read()

    expected = expected.strip()
    obtained = obtained.strip()

    # print(expected)
    # print(parse(expected))
    # print(obtained)
    # print(parse(obtained))

    if check(expected=expected, obtained=obtained):
        return 0
    else:
        sys.stdout.write('Wrong Answer\n')
        return 1

if __name__ == '__main__':
    sys.exit(main())

