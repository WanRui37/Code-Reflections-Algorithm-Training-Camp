class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        # dp[][j]和为j的组合的总数
        dp = [[0] * (target+1) for _ in nums]
        
        for i in range(len(nums)):
            dp[i][0] = 1

        # 这里不能初始化dp[0][j]。dp[0][j]的值依赖于dp[-1][j-nums[0]]

        for j in range(1, target+1):
            for i in range(len(nums)):
                
                if j - nums[i] >= 0:
                    dp[i][j] = (
                        # 不放nums[i]
                        # i = 0 时，dp[-1][j]恰好为0，所以没有特殊处理
                        dp[i-1][j] +
                        # 放nums[i]。对于和为j的组合，只有试过全部物品，才能知道有几种组合方式。所以取最后一个物品dp[-1][j-nums[i]]
                        dp[-1][j-nums[i]]
                    )
                else:
                    dp[i][j] = dp[i-1][j]
        return dp[-1][-1]