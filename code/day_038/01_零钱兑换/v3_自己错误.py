class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        n = len(coins)
        dp = [[float(inf)]*(amount+1) for _ in range(n)]

        for i in range(n):
            dp[i][0] = 0

        for i in range(n):
            for j in range(coins[i], amount+1):
                if dp[i][j-coins[i]] != inf or dp[i-1][j] != inf :
                    dp[i][j] = min(dp[i-1][j], dp[i][j-coins[i]]+1)
        print(dp)
        if dp[-1][-1] != inf:
            return dp[-1][-1]
        else:
            return -1