class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums, int startIndex) {
        result.push_back(path);  // 当前路径就是一个子集

        for (int i = startIndex; i < nums.size(); i++) {
            path.push_back(nums[i]);          // 选择 nums[i]
            backtracking(nums, i + 1);        // 递归搜索后面的元素
            path.pop_back();                  // 回溯
        }
    }

    vector<vector<int>> subsets(vector<int>& nums) {
        result.clear();
        path.clear();
        backtracking(nums, 0);
        return result;
    }
};