def a(n, m):
    weight = range(m)
    dp = [[0]*(n+1) for _ in range(m)]

    for i in range(m):
        dp[i][0] = 1

    for j in range(n+1):
        for i in range(m):
            if j < weight[i] :
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = dp[i-1][j] + dp[-1][j-weight[i]]

    return dp[-1][-1]

n, m = map(int, input().split())

print(a(n, m))