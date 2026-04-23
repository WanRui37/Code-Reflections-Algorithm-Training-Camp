class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashtable = dict()
        for i, num in enumerate(nums):
            if target-num not in hashtable:
                hashtable[num] = i
            else:
                return [hashtable[target-num], i]
        return []