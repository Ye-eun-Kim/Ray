from collections import deque


def solution(maps):
    g = []
    s, e, l = (0, 0), (0, 0), (0, 0)
    r = -1
    dr, dc = [-1, 0, 1, 0], [0, 1, 0, -1]
    for line in maps:
        r += 1
        if 'S' in line:
            idx = line.find('S')
            line = line.replace('S', 'O')
            s = (r, idx)
        if 'L' in line:
            idx = line.find('L')
            line = line.replace('L', 'O')
            l = (r, idx)
        if 'E' in line:
            idx = line.find('E')
            line = line.replace('E', 'O')
            e = (r, idx)
        g.append(list(line))

    n = r + 1
    sr, sc = s
    r, c = sr, sc

    dp = [[(n) ** 2 for _ in range(n)] for _ in range(n)]
    dp[sr][sc] = 0

    visited = []
    q = deque()

    q.append((r, c))

    lever = False

    while q:
        r, c = q.popleft()
        visited.append((r, c))
        if (r, c) == l:
            lever == True
        if lever:
            if (r, c) == e:
                return dp[r][c]
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if 0 <= nr <= n - 1 and 0 <= nc <= n - 1 and g[nr][nc] == 'O':
                if (nr, nc) not in visited:
                    dp[nr][nc] = min(dp[r][c] + 1, dp[nr][nc])
                    q.append((nr, nc))

    answer = dp[e[0]][e[1]]
    return answer if answer != 25 else -1