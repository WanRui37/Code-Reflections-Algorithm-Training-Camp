#include<iostream>
#include<vector>
using namespace std;

class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int slow = 0;
        int total_num = nums.size();
        for(int fast=0; fast<total_num; fast++){
            if(nums[fast] != val){
                nums[slow] = nums[fast];
                slow++;
            }
        }
        return slow;
    }
};

int main(){
    vector<int> nums = {0,1,2,2,3,0,4,2};
    int val = 2;
    Solution solution;
    int newLength = solution.removeElement(nums, val);
    cout << "New length: " << newLength << endl;
    cout << "Modified array: ";
    for (int i = 0; i < newLength; i++) {
        cout << nums[i] << " ";
    }
    cout << endl;
    return 0;
}