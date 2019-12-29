REGEXP = r"([a-c])([+-]?)=([a-c]?)([+-]?\d+)?"

def calculate(data, findall):
    matches = findall(REGEXP)  # Если придумать хорошую регулярку, будет просто

    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        # Если бы могло быть только =, вообще одной строкой все считалось бы, вот так:
        if not s:
            data[v1] = data.get(v2, 0) + int(n or 0)
        else:
            s = -1 if s == "-" else 1
            data[v1] += s * (data.get(v2, 0) + int(n or 0))

    return data

