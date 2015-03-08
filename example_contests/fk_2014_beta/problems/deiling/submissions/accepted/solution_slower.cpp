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
    int a, b;
    scanf("%d %d\n", &a, &b);

    int first = a/b;
    a %= b;

    int gen = 5000;
    int *digs = new int[gen];
    for (int i = 0; i < gen; i++)
    {
        a *= 10;
        digs[i] = a/b;
        a %= b;
    }

    bool found = false;
    for (int len = 1; !found && len <= gen/2; len++)
    {
        int cnt = 0;
        int at = gen - len;
        while (at >= 0)
        {
            bool ok = true;
            for (int i = 0; ok && i < len; i++)
            {
                ok = digs[at + i] == digs[gen - len + i];
            }

            if (!ok)
                break;

            cnt++;
            at -= len;
        }

        if (cnt * len > gen / 2)
        {
            found = true;
            int start = gen - len;
            while (start - 1 >= 0 && digs[start + len - 1] == digs[start - 1])
                start--;

            printf("%d", first);

            if (start == 0 && len == 1 && digs[start] == 0)
                break;

            printf(".");
            for (int i = 0; i < start; i++)
                printf("%d", digs[i]);

            if (len == 1 && digs[start] == 0)
                break;

            printf("(");
            for (int i = 0; i < len; i++)
                printf("%d", digs[start + i]);
            printf(")");
        }
    }

    printf("\n");

    assert(found);

    return 0;
}

