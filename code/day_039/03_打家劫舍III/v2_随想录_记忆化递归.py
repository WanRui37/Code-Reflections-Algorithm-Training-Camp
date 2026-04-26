class Solution:
    memory = {}
    def rob(self, root: TreeNode) -> int:
        if root is None:
            return 0
        if root.left is None and root.right  is None:
            return root.val
        if self.memory.get(root) is not None:
            return self.memory[root]
        # 偷父节点
        val1 = root.val
        if root.left:
            val1 += self.rob(root.left.left) + self.rob(root.left.right)
        if root.right:
            val1 += self.rob(root.right.left) + self.rob(root.right.right)
        # 不偷父节点
        val2 = self.rob(root.left) + self.rob(root.right)
        self.memory[root] = max(val1, val2)
        return max(val1, val2)