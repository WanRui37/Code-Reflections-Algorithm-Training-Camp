class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        s_len, p_len = len(s), len(p)
        if s_len < p_len:
            return []

        ans = []
        p_count = [0] * 26
        window = [0] * 26

        # 先统计 p
        for ch in p:
            p_count[ord(ch) - ord('a')] += 1

        left = 0
        for right in range(s_len):
            # 1. 右指针加入窗口
            window[ord(s[right]) - ord('a')] += 1

            # 2. 如果窗口长度超过 p_len，就收缩左边
            while right - left + 1 > p_len:
                window[ord(s[left]) - ord('a')] -= 1
                left += 1

            # 3. 当窗口长度刚好等于 p_len 时，判断是否匹配
            if right - left + 1 == p_len and window == p_count:
                ans.append(left)

        return ans