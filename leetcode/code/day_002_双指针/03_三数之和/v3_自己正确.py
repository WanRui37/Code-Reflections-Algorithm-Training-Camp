class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        result = []
        nums.sort()

        for i in range(len(nums) - 2):
            # 第一个数去重
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left = i + 1
            right = len(nums) - 1

            while left < right:
                s = nums[i] + nums[left] + nums[right]

                if s == 0:
                    result.append([nums[i], nums[left], nums[right]])

                    # 第二个数去重
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1

                    # 第三个数去重
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1

                elif s < 0:
                    left += 1
                else:
                    right -= 1

        return result