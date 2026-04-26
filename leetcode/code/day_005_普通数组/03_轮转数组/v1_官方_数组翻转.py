class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n

        def reverse(left, right):
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1

        # 1. 整体反转
        reverse(0, n - 1)

        # 2. 反转前 k 个
        reverse(0, k - 1)

        # 3. 反转后 n - k 个
        reverse(k, n - 1)