class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        target = abs(target);
        int sum = accumulate(nums.begin(), nums.end(), 0);

        int target_new = (target+sum)/2;
        vector<int> dp(target_new+1, 0);
        int nums_len = nums.size();
        
        for(int j=nums[0]; j<=target_new; j++) {
            dp[j] = nums[0];
        }

        for(int i=1; i<nums_len; i++) {
            for(int j=target_new; j>=0; j--) {
                dp[j] = max(dp[j], dp[j-nums[i]]+nums[i]);
            }
        }

        return dp[target_new];
    }
};