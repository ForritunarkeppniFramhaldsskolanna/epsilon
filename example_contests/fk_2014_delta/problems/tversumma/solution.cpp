#include <algorithm>
#include <bitset>
#include <cassert>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <list>
#include <map>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <utility>
#include <vector>
using namespace std;

#define all(o) (o).begin(), (o).end()
#define allr(o) (o).rbegin(), (o).rend()
const int INF = 2147483647;
typedef long long ll;
typedef pair<int, int> ii;
typedef vector<int> vi;
typedef vector<ii> vii;
typedef vector<vi> vvi;
typedef vector<vii> vvii;
template <class T> int size(T &x) { return x.size(); }

// assert or gtfo

string digitsum(string s)
{
    int res = 0;
    for (int i = 0; i < size(s); i++)
    {
        res += s[i] - '0';
    }

    stringstream ss;
    ss << res;
    return ss.str();
}

int main()
{
    string s;
    getline(cin, s);

    while (size(s) > 1)
    {
        cout << s << endl;
        s = digitsum(s);
    }

    cout << s << endl;

    return 0;
}

