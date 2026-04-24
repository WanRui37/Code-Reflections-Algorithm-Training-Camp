class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        count = 0
        p_dict = dict()
        s_dict = dict()
        left = 0
        result = []

        for pp in p:
            if pp not in p_dict:
                p_dict[pp] = 1
            else:
                p_dict[pp] += 1

        right = len(p) - 1
        while right < len(s):
            left = right - len(p) + 1
            not_element_flag = 0

            if right == len(p)-1:
                for ppp in p_dict:
                    s_dict[ppp] = -p_dict[ppp]

                for sss in s[left:right+1]:
                    if sss in p_dict:
                        s_dict[sss] += 1
                    else:
                        not_element_flag = 1    

            else:
                if s[left-1] not in s_dict:
                    not_element_flag = 0
                else:
                    s_dict[s[left-1]] -= 1
                
                if s[right] not in s_dict:
                    not_element_flag = 1
                    right += 1
                    continue
                else:
                    s_dict[s[right]] += 1

            if not_element_flag == 1:
                right += 1
                continue
            else:
                if set(s_dict.values()) == {0}:
                    result.append(left)
            right += 1

        return result

            