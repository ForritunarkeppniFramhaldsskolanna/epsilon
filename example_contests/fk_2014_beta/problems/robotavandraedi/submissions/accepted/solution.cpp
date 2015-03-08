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
    int n, m;
    scanf("%d %d\n", &n, &m);

    char **arr = new char*[n];
    for (int i = 0; i < n; i++)
    {
        arr[i] = new char[m];
        for (int j = 0; j < m; j++)
        {
            scanf("%c", arr[i] + j);
        }

        scanf("\n");
    }

    queue<ii> Q;
    Q.push(ii(0, 0));

    bool reached_robots = false;
    while (!Q.empty())
    {
        ii cur = Q.front(); Q.pop();

        if (arr[cur.first][cur.second] == 'X')
        {
            reached_robots = true;
            break;
        }

        for (int di = -1; di <= 1; di++)
        {
            for (int dj = -1; dj <= 1; dj++)
            {
                if ((di == 0) ^ (dj == 0))
                {
                    int ci = cur.first + di,
                        cj = cur.second + dj;

                    if (ci >= 0 && cj >= 0 && ci < n && cj < m && (arr[ci][cj] == '.' || arr[ci][cj] == 'X'))
                    {
                        if (arr[ci][cj] == '.')
                        {
                            arr[ci][cj] = '%';
                        }

                        Q.push(ii(ci, cj));
                    }
                }
            }
        }
    }

    if (reached_robots)
    {
        printf("Death to humans\n");
    }
    else
    {
        printf("We are safe\n");
    }

    for (int i = 0; i < n; i++)
        delete[] arr[i];

    delete[] arr;

    return 0;
}

