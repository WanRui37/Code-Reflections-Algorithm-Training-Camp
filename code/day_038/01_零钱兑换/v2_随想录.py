class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)  # 创建动态规划数组，初始值为正无穷大
        dp[0] = 0  # 初始化背包容量为0时的最小硬币数量为0

        for i in range(1, amount + 1):  # 遍历背包容量
            for j in range(len(coins)):  # 遍历硬币列表，相当于遍历物品
                if i - coins[j] >= 0 and dp[i - coins[j]] != float('inf'):  # 如果dp[i - coins[j]]不是初始值，则进行状态转移
                    dp[i] = min(dp[i - coins[j]] + 1, dp[i])  # 更新最小硬币数量

        if dp[amount] == float('inf'):  # 如果最终背包容量的最小硬币数量仍为正无穷大，表示无解
            return -1
        return dp[amount]  # 返回背包容量为amount时的最小硬币数量