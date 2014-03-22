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

bool is_open(char c)
{
    return c == '(' || c == '{' || c == '[';
}

char closing(char c)
{
    if (c == '(') return ')';
    if (c == '{') return '}';
    if (c == '[') return ']';
    assert(false);
}

int main()
{
    string line;
    getline(cin, line);

    bool ok = true;
    stack<char> par;

    for (int i = 0; i < size(line); i++)
    {
        if (is_open(line[i]))
        {
            par.push(line[i]);
        }
        else
        {
            ok = ok && !par.empty() && closing(par.top()) == line[i];
            if (!par.empty()) par.pop();
        }
    }

    ok = ok && par.empty();

    if (ok)
    {
        printf("Ja\n");
    }
    else
    {
        printf("Nei\n");
    }

    return 0;
}

