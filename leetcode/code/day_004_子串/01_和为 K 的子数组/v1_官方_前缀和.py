class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        preSum = 0
        count = 0

        # key: 某个前缀和
        # value: 这个前缀和出现了几次
        hashmap = collections.defaultdict(int)

        # 前缀和为 0 出现 1 次
        # 这是为了处理从下标 0 开始的子数组
        hashmap[0] = 1

        for num in nums:
            preSum += num

            # 看之前有没有 preSum - k
            # 如果有，说明存在若干个子数组和为 k
            count += hashmap[preSum - k]

            # 记录当前前缀和
            hashmap[preSum] += 1

        return count


'''''''''''''''
'''逐步打印情况'''
'''''''''''''''

from typing import List
import collections

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        preSum = 0
        count = 0
        hashtable = collections.defaultdict(int)
        hashtable[0] = 1

        print("初始状态：")
        print("preSum =", preSum)
        print("count =", count)
        print("hashtable =", dict(hashtable))
        print("-" * 40)

        for ii in range(len(nums)):
            print(f"第 {ii} 轮，当前 nums[{ii}] = {nums[ii]}")

            preSum += nums[ii]
            print("更新后的 preSum =", preSum)

            target = preSum - k
            print("需要查找的前缀和 preSum - k =", target)
            print(f"hashtable[{target}] =", hashtable[target])

            count += hashtable[target]
            print("更新后的 count =", count)

            hashtable[preSum] += 1
            print("加入当前 preSum 后：")
            print("hashtable =", dict(hashtable))

            print("-" * 40)

        return count