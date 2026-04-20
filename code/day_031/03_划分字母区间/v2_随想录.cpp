class Solution {
public:
    static bool cmp(vector<int> &a, vector<int> &b) {
        return a[0] < b[0];
    }
    // 记录每个字母出现的区间
    vector<vector<int>> countLabels(string s) {
        vector<vector<int>> hash(26, vector<int>(2, INT_MIN));
        vector<vector<int>> hash_filter;
        for (int i = 0; i < s.size(); ++i) {
            if (hash[s[i] - 'a'][0] == INT_MIN) {
                hash[s[i] - 'a'][0] = i;
            }
            hash[s[i] - 'a'][1] = i;
        }
        // 去除字符串中未出现的字母所占用区间
        for (int i = 0; i < hash.size(); ++i) {
            if (hash[i][0] != INT_MIN) {
                hash_filter.push_back(hash[i]);
            }
        }
        return hash_filter;
    }
    vector<int> partitionLabels(string s) {
        vector<int> res;
        // 这一步得到的 hash 即为无重叠区间题意中的输入样例格式：区间列表
        // 只不过现在我们要求的是区间分割点
        vector<vector<int>> hash = countLabels(s);
        // 按照左边界从小到大排序
        sort(hash.begin(), hash.end(), cmp);
        // 记录最大右边界
        int rightBoard = hash[0][1];
        int leftBoard = 0;
        for (int i = 1; i < hash.size(); ++i) {
            // 由于字符串一定能分割，因此,
            // 一旦下一区间左边界大于当前右边界，即可认为出现分割点
            if (hash[i][0] > rightBoard) {
                res.push_back(rightBoard - leftBoard + 1);
                leftBoard = hash[i][0];
            }
            rightBoard = max(rightBoard, hash[i][1]);
        }
        // 最右端
        res.push_back(rightBoard - leftBoard + 1);
        return res;
    }
};