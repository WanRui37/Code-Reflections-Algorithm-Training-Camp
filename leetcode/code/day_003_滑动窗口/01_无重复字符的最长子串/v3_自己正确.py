class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_len = 0
        left = 0

        hashmap = dict()
        for i in range(len(s)):
            if s[i] not in hashmap:
                hashmap[s[i]] = i
                current_len = i - left +1
            else:
                if left < hashmap[s[i]]+1:
                    left = hashmap[s[i]]+1
                hashmap[s[i]] = i
                current_len = i - left +1

            max_len = max(max_len, current_len)

        return max_len