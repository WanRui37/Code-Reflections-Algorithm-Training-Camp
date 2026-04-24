class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        window = set()
        ans = 0

        for right in range(len(s)):
            # 1. 右指针加入窗口
            while s[right] in window:
                # 2. 不合法就收缩左边界
                window.remove(s[left])
                left += 1

            window.add(s[right])

            # 3. 更新答案
            ans = max(ans, right - left + 1)

        return ans