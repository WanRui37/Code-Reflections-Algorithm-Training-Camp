class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:  # 如果没有房屋，返回0
            return 0

        if len(nums) == 1:  # 如果只有一个房屋，返回该房屋的金额
            return nums[0]

        # 情况二：不抢劫第一个房屋
        prev_max = 0  # 上一个房屋的最大金额
        curr_max = 0  # 当前房屋的最大金额
        for num in nums[1:]:
            temp = curr_max  # 临时变量保存当前房屋的最大金额
            curr_max = max(prev_max + num, curr_max)  # 更新当前房屋的最大金额
            prev_max = temp  # 更新上一个房屋的最大金额
        result1 = curr_max

        # 情况三：不抢劫最后一个房屋
        prev_max = 0  # 上一个房屋的最大金额
        curr_max = 0  # 当前房屋的最大金额
        for num in nums[:-1]:
            temp = curr_max  # 临时变量保存当前房屋的最大金额
            curr_max = max(prev_max + num, curr_max)  # 更新当前房屋的最大金额
            prev_max = temp  # 更新上一个房屋的最大金额
        result2 = curr_max

        return max(result1, result2)