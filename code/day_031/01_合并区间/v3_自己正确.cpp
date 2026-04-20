class Solution {
public:
    static bool cmp(const vector<int>& a, const vector<int>& b) {
        return a[0] < b[0];
    }

    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        if (intervals.size() == 0) return {};

        sort(intervals.begin(), intervals.end(), cmp);

        vector<vector<int>> result;
        int start = intervals[0][0];
        int end = intervals[0][1];

        for (int i = 1; i < intervals.size(); i++) {
            if (end < intervals[i][0]) {
                result.push_back({start, end});
                start = intervals[i][0];
                end = intervals[i][1];
            } else {
                end = max(end, intervals[i][1]);
            }
        }

        result.push_back({start, end});
        return result;
    }
};