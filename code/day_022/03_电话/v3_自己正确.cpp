class Solution {
public:
    vector<string> result;
    string path;

    unordered_map<char, string> mp = {
        {'2', "abc"},
        {'3', "def"},
        {'4', "ghi"},
        {'5', "jkl"},
        {'6', "mno"},
        {'7', "pqrs"},
        {'8', "tuv"},
        {'9', "wxyz"}
    };

    void backtracking(const string& digits, int index) {
        if (index == digits.size()) {
            result.push_back(path);
            return;
        }

        string letters = mp[digits[index]];
        for (int i = 0; i < letters.size(); i++) {
            path += letters[i];
            backtracking(digits, index + 1);
            path.pop_back();
        }
    }

    vector<string> letterCombinations(string digits) {
        result.clear();
        path.clear();

        if (digits.size() == 0) return result;

        backtracking(digits, 0);
        return result;
    }
};