class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        pre = 0
        maxAns = nums[0]

        for x in nums:
            pre = max(pre + x, x)
            maxAns = max(maxAns, pre)

        return maxAns


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        dp = [0] * len(nums)
        dp[0] = nums[0]
        result = nums[0]

        for i in range(1, len(nums)):
            dp[i] = max(dp[i - 1] + nums[i], nums[i])
            result = max(result, dp[i])

        return result