class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height)-1
        max_S = 0
        while(left < right):
            cur_S = min(height[left], height[right]) * (right - left)
            max_S = max(max_S, cur_S)

            if(height[left] < height[right]):
                left += 1
            else:
                right -= 1

        return max_S