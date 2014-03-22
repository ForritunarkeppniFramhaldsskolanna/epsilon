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

int main()
{
    map<char, string> m;
m['A'] = "4";
m['B'] = "|3";
m['C'] = "(";
m['D'] = "|)";
m['E'] = "3";
m['F'] = "|=";
m['G'] = "6";
m['H'] = "|-|";
m['I'] = "1";
m['J'] = "_|";
m['K'] = "|<";
m['L'] = "|_";
m['M'] = "|\\/|";
m['N'] = "|\\|";
m['O'] = "0";
m['P'] = "|D";
m['Q'] = "(,)";
m['R'] = "|2";
m['S'] = "5";
m['T'] = "+";
m['U'] = "|_|";
m['V'] = "|/";
m['W'] = "\\/\\/";
m['X'] = "><";
m['Y'] = "`/";
m['Z'] = "2";

    string line;
    getline(cin, line);

    for (int i = 0; i < size(line); i++)
    {
        if (m.find(line[i]) == m.end())
        {
            cout << line[i];
        }
        else
        {
            cout << m[line[i]];
        }
    }

    cout << endl;

    return 0;
}

