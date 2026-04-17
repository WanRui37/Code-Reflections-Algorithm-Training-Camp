class Solution {
public:
    vector<vector<string>> result;
    vector<string> path;

    void back(string s, int index){
        if(left > right){
            result.push_back(path);
            return;
        }

        for(int i=left; i<right; i++){
            if(s[i] != s[right-i]){
                return ;
            }
        }
        path.push_back(s[left:right]);

        for()
        back(s, left, right)
    }

    vector<vector<string>> partition(string s) {
        back(s, 0);
        return result;
    }
};