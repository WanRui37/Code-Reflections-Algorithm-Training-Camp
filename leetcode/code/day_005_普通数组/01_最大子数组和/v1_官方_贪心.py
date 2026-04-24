class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        result = nums[0]
        cur_sum = 0

        for num in nums:
            cur_sum += num
            result = max(result, cur_sum)

            # 如果当前和已经是负数，说明它对后面没有帮助
            if cur_sum < 0:
                cur_sum = 0

        return result