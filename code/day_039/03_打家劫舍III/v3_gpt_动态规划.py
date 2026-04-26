class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def traversal(node):
            if node is None:
                return [0, 0]

            left = traversal(node.left)
            right = traversal(node.right)

            # 不偷当前节点：左右孩子偷不偷都行，取最大
            not_rob = max(left[0], left[1]) + max(right[0], right[1])

            # 偷当前节点：左右孩子不能偷
            rob = node.val + left[0] + right[0]

            return [not_rob, rob]

        result = traversal(root)
        return max(result)