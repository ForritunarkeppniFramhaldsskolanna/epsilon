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
    int n;
    scanf("%d\n", &n);

    ii *pop = new ii[n];
    for (int i = 0; i < n; i++)
    {
        scanf("%d %d\n", &pop[i].first, &pop[i].second);
    }

    int rt = 0,
        rc = 0;

    for (int t = 0; t < 3000; t++)
    {
        int cnt = 0;
        for (int i = 0; i < n; i++)
        {
            if (pop[i].first <= t && t <= pop[i].first + pop[i].second - 1)
            {
                cnt++;
            }
        }

        if (cnt > rc)
        {
            rc = cnt;
            rt = t;
        }
    }

    printf("%d %d\n", rt, rc);

    return 0;
}

