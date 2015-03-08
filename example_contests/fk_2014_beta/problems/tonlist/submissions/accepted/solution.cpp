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
    string pat, line;
    getline(cin, pat);

    int n = 0;
    getline(cin, line);

    for (int i = 0; i < size(line); i++)
        n = n * 10 + line[i] - '0';

    int idx = 0;
    while (idx < size(pat) && pat[idx] != '*') idx++;

    for (int i = 0; i < n; i++)
    {
        getline(cin, line);
        bool ok = true;

        if (idx == size(pat))
        {
            ok = pat == line;
        }
        else
        {
            int l = 0,
                r = size(line) - 1,
                at;

            at = 0;
            while (l <= r && at < idx)
            {
                ok = ok && pat[at] == line[l];
                l++;
                at++;
            }

            ok = ok && at == idx;

            at = size(pat) - 1;
            while (l <= r && at > idx)
            {
                ok = ok && pat[at] == line[r];
                r--;
                at--;
            }

            ok = ok && at == idx;
        }

        if (ok)
        {
            printf("Passar\n");
        }
        else
        {
            printf("Passar ekki\n");
        }
    }

    return 0;
}

