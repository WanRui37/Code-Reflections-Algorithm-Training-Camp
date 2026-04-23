def climbing_stairs(n, m):
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 凑成0阶都只有1种方法：什么都不走
    for i in range(m + 1):
        dp[i][0] = 1

    # 动态规划
    for j in range(1, n + 1):      # 先遍历台阶数，保证求排列
        for i in range(1, m + 1):  # 再遍历可选步长
            dp[i][j] = dp[i - 1][j]   # 不把步长i作为最后一步
            if j >= i:
                dp[i][j] += dp[m][j - i]  # 把步长i作为最后一步

    return dp[m][n]

if __name__ == '__main__':
    n, m = map(int, input().split())
    print(climbing_stairs(n, m))