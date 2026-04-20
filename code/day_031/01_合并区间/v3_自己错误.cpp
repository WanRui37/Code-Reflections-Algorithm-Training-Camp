class Solution {
public:
    static bool cmp(vector<int>& a, vector<int>& b) {
        return a[1] < b[1];
    }

    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), cmp);

        vector<vector<int>> result;

        int end = intervals[0][1];
        int start = intervals[0][0];
        for(int i=1; i<intervals.size(); i++) {
            if(end < intervals[i][0]){
                result.push_back({start, end});
                start = intervals[i][0];
                end = intervals[i][1];
            } else {
                start = min(start, intervals[i][0]);
                end = intervals[i][1];
            }
        }

        return result;
    }
};