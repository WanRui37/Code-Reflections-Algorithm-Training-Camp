class Solution {
public:
    TreeNode* ArrayToBST(vector<int>& nums, int i) {
        if(i < 0 || i >= nums.size()) {
            return NULL;
        }

        TreeNode* node = new TreeNode(nums[i]);
        // [1] 这里用“i < nums.size()/2”来决定是否递归左子树是错误的：
        //     nums.size()/2 是整段数组的固定中点，而不是当前子问题(子数组)的中点。
        //     递归时子问题的范围并没有被传下去，只传了一个索引 i，导致分治边界丢失。
        if(i < nums.size() / 2) node->left = ArrayToBST(nums, i-1);

        // [2] 同理，这里用“i > nums.size()/2”决定右子树也错误：
        //     你是在拿当前索引 i 和“全局中点”比较，而不是在当前子数组内取中点。
        if(i > nums.size() / 2) node->right = ArrayToBST(nums, i+1);

        // [3] 更关键的问题：递归只做 i-1 / i+1 的线性扩展，并没有把区间一分为二。
        //     这会生成接近“

        node->left = ArrayToBST(nums, i-1);
        node->right = ArrayToBST(nums, i+1);

        return node;
    }
};