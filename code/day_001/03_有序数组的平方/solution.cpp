#include<iostream>
#include<vector>
using namespace std;

class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        int i,j=0;
        int k=nums.size()-1;
        vector<int> result(k+1);
        for(i=0, j=k; i<=j; ){
            if(nums[i] * nums[i] > nums[j] * nums[j]){
                result[k--] = nums[i] * nums[i];
                i++;
            } else{
                result[k--] = nums[j] * nums[j];
                j--;
            }
        }
        return result;
    }
};

int main(){
    vector<int> nums = {-4,-1,0,3,10};
    Solution solution;
    vector<int> result = solution.sortedSquares(nums);
    cout << "Sorted squares: ";
    for (int i = 0; i < result.size(); i++) {
        cout << result[i] << " ";
    }
    cout << endl;
    return 0;
}