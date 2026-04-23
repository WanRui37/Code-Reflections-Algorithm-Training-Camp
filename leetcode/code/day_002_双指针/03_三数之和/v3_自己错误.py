class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        
        result = []

        nums_sorted = sorted(nums)
        for left_1 in range(0, len(nums_sorted)-2):
            right   = len(nums_sorted)-1
            left_2  = left_1+1
        
            while(left_2 < right):
                if nums_sorted[left_1] + nums_sorted[left_2] + nums_sorted[right] == 0:
                    result.append([nums_sorted[left_1], nums_sorted[left_2], nums_sorted[right]])
                    break
                elif nums_sorted[left_1] + nums_sorted[left_2] + nums_sorted[right] < 0:
                    left_2 += 1
                elif nums_sorted[left_1] + nums_sorted[left_2] + nums_sorted[right] > 0:
                    right -= 1

        return result