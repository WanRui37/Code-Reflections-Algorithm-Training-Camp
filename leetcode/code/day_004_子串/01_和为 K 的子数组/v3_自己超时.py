class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0

        for right in range(len(nums)):
            left = 0
            while left <= right:
                sum_num = sum(nums[left:right+1])
                if sum_num == k:
                    count += 1
                left += 1
            
        return count