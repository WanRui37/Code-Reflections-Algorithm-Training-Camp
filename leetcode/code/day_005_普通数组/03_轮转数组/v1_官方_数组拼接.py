class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n  # 处理 k > n 的情况
        nums[:] = nums[-k:] + nums[:-k]  # 切片赋值