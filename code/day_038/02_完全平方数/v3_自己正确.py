import math
from typing import List

class Solution:
    def numSquares(self, n: int) -> int:
        squares = [i * i for i in range(1, int(math.sqrt(n)) + 1)]
        m = len(squares)
        INF = float('inf')

        dp = [[INF] * (n + 1) for _ in range(m)]

        # 初始化：凑成 0 都需要 0 个数
        for i in range(m):
            dp[i][0] = 0

        # 初始化第 0 行：只能用 1
        for j in range(n + 1):
            dp[0][j] = j

        # 动态规划
        for i in range(1, m):
            for j in range(1, n + 1):
                if j < squares[i]:
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - squares[i]] + 1)

        return dp[m - 1][n]