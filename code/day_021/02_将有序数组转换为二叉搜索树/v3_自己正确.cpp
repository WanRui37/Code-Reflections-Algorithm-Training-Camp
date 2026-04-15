class Solution {
public:
    TreeNode* ArrayToBST(vector<int>& nums, int left, int right) {
        if(left > right) {
            return NULL;
        }

        int mid = left + (right-left) / 2;

        TreeNode* node = new TreeNode(nums[mid]);
        node->left = ArrayToBST(nums, left, mid-1);
        node->right = ArrayToBST(nums, mid+1, right);

        return node;
    }

    TreeNode* sortedArrayToBST(vector<int>& nums) {
        if(nums.size() == 0) return NULL;
        
        TreeNode* node = new TreeNode(nums.size() / 2);

        node = ArrayToBST(nums, 0, nums.size()-1);

        return node;
    }
};