class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        n = len(coins)
        INF = float('inf')
        dp = [[INF] * (amount + 1) for _ in range(n)]

        # 初始化：金额 0 都需要 0 枚硬币
        for i in range(n):
            dp[i][0] = 0

        # 初始化第 0 行：只用 coins[0]
        for j in range(amount + 1):
            if j % coins[0] == 0:
                dp[0][j] = j // coins[0]

        # 动态规划
        for i in range(1, n):
            for j in range(1, amount + 1):
                if j < coins[i]:
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - coins[i]] + 1)

        return dp[n - 1][amount] if dp[n - 1][amount] != INF else -1