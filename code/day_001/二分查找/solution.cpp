#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int search(vector<int>& nums, int target) {
        int left = 0;
        int right = nums.size()-1;
        int middle = 0;

        while(left <= right){
            middle = (right+left)/2;
            printf("left: %d, right: %d, middle: %d\n", left, right, middle);
            
            if(nums[middle] < target) {
                left = middle+1;
            }else if(nums[middle] > target) {
                right = middle-1;
            }else{
                return middle;
            }
        }
        return -1;
    }
};

int main(){
    Solution solution;
    vector<int> nums = {-1,0,3,5,9,12};
    int target = 9;
    int result = solution.search(nums, target);
    if (result != -1) {
        cout << "Target found at index: " << result << endl;
    } else {
        cout << "No target found." << endl;
    }
    return 0;
}