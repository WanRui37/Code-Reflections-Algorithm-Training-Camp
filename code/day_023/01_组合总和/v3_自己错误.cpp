class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backstack(vector<int>& candidates, int target, int sum){
        if(sum == target){
            result.push_back(path);
            return;
        }

        if(sum > target) return;

        for(int i=0; i<candidates.size(); i++){
            path.push_back(candidates[i]);
            sum += candidates[i];
            backstack(candidates, target, sum);
            sum -= candidates[i];
            path.pop_back();
        }
    }
    
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        backstack(candidates, target, 0);
        return result;
    }
};