class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        n = len(coins)
        dp = [[0] * (amount + 1) for _ in range(n)]

        # 初始化：凑出金额0都只有1种方法，什么都不选
        for i in range(n):
            dp[i][0] = 1

        # 初始化第0种硬币
        for j in range(0, amount + 1):
            if j % coins[0] == 0:
                dp[0][j] = 1

        # 动态规划
        for i in range(1, n):
            for j in range(1, amount + 1):
                if j < coins[i]:
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - coins[i]]

        return dp[n - 1][amount]