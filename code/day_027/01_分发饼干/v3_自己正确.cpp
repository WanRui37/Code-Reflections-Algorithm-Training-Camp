class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums, int startIndex) {
        if(path.size() > 1){
            result.push_back(path);
        }
        unordered_set<int> st;

        for(int i=startIndex; i<nums.size(); i++){
            if(st.count(nums[i])) continue;
            if(path.size() >=1 && nums[i]>=path[path.size()-1] || path.size()==0){
                st.insert(nums[i]);
                path.push_back(nums[i]);
                backtracking(nums, i+1);
                path.pop_back();
            }
        }
    }

    vector<vector<int>> findSubsequences(vector<int>& nums) {
        result.clear();
        path.clear();
        backtracking(nums, 0);
        return result;
    }
};