M = [[0, 1, 1, 0],
     [1, 0, 1, 1],
     [1, 1, 0, 1],
     [0, 1, 1, 0]]


def find_path(M, u, v, path, buffer=None):
    buffer = buffer or [u]
    if u == v:
        path.append(buffer[:])
        return
    for j, val in enumerate(M[u]):
        if j not in buffer and val == 1:
            buffer.append(j)
            find_path(M, j, v, path, buffer)
            buffer.pop()
    return path


print(find_path(M, 0, 3, path=[]))
