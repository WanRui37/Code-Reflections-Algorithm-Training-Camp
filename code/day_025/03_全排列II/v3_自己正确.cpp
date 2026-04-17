class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums, vector<bool>& used) {
        if(path.size() == nums.size()){
            result.push_back(path);
            return;
        }

        unordered_set<int> st;

        for(int i=0; i<nums.size(); i++){
            if(st.find(nums[i]) != st.end()) continue;
            if(used[i]) continue;
            st.insert(nums[i]);
            used[i] = true;
            path.push_back(nums[i]);
            backtracking(nums, used);
            path.pop_back();
            used[i] = false;
        }
    }

    vector<vector<int>> permuteUnique(vector<int>& nums) {
        result.clear();
        path.clear();
        vector<bool> used(nums.size(), false);
        backtracking(nums, used);
        return result;
    }
};