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
    ll n;
    cin >> n;

    ll res = 0;
    ll a = 0,
       b = 0;

    for (ll i = 0; a < n || b < n; i++)
    {
        int ones = 0;
        ll t = i;
        while (t)
        {
            ones++;
            t &= t - 1;
        }

        if (ones % 2 == 0)
        {
            if (++a == n)
            {
                res += i;
            }
        }
        else
        {
            if (++b == n)
            {
                res += i;
            }
        }
    }

    cout << res << endl;

    return 0;
}

