class Solution {
public:
    vector<string> result;
    string path;
    unordered_map<string, string> map={
        {'2':'abc',
         '3':'def',
         '4':'ghi',
         '5':'jkl',
         '6':'mno',
         '7':'pqrs',
         '8':'tuv',
         '9':'wxyz'}
    };

    void backtracking(string digits, int index){
        if(path.size() == digits.size()){
            result.push_back(path);
            return ;
        }

        string list = map[digits[index]];

        for(int i=0; i<list.size(); i++){
            path += list[i];
            backtracking(digits);
            path -= list[i];
        }
    }

    vector<string> letterCombinations(string digits) {
        result.clear();
        path.clear();
        backtracking(digits, 0);
        return result;
    }
};