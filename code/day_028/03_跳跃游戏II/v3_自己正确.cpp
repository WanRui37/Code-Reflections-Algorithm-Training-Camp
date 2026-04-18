class Solution {
public:
    int jump(vector<int>& nums) {
        int curDis = 0;
        int nextDis = 0;
        int step = 0;

        if(nums.size()==1) return 0;
        for(int i=0; i<nums.size(); i++){
            nextDis = max(i+nums[i], nextDis);
            cout << "i:" << i << endl;
            cout << "nextDis:" << nextDis << endl;

            if(i == curDis){
                step++;
                curDis = nextDis;
                if(nextDis >= nums.size()-1) break;
            }
        }

        return step;
    }
};