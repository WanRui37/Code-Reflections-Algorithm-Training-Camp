class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int result=INT_MIN;
        int flag=1;

        if(nums.size()==1) return nums[0];

        for(int i=0; i<nums.size(); i++){

            if(nums[i]>result && flag==1 && result>=0 || result<0) {
                result = nums[i];
                flag = 0;
                continue;
            }
            
            if(result+nums[i] <0){
                flag = 1;
                continue;
            }


            result += nums[i];


            cout << "i:" << i << endl;
            cout << "result:" << result << endl;

        }

        return result;
    }
};