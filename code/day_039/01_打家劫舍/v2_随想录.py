class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:  # 如果没有房屋，返回0
            return 0

        n = len(nums)
        dp = [[0, 0] for _ in range(n)]  # 创建二维动态规划数组，dp[i][0]表示不抢劫第i个房屋的最大金额，dp[i][1]表示抢劫第i个房屋的最大金额

        dp[0][1] = nums[0]  # 抢劫第一个房屋的最大金额为第一个房屋的金额

        for i in range(1, n):
            dp[i][0] = max(dp[i-1][0], dp[i-1][1])  # 不抢劫第i个房屋，最大金额为前一个房屋抢劫和不抢劫的最大值
            dp[i][1] = dp[i-1][0] + nums[i]  # 抢劫第i个房屋，最大金额为前一个房屋不抢劫的最大金额加上当前房屋的金额

        return max(dp[n-1][0], dp[n-1][1])  # 返回最后一个房屋中可抢劫的最大金额