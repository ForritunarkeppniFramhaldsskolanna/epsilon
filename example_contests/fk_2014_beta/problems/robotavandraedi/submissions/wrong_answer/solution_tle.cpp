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

char **arr;
int n, m;
bool **visited;

bool can_escape(int x, int y)
{
    visited = new bool*[n];
    for (int i = 0; i < n; i++)
    {
        visited[i] = new bool[m];
        memset(visited[i], 0, m);
    }

    queue<ii> Q;
    Q.push(ii(x, y));
    visited[x][y] = true;

    bool res = false;

    while (!Q.empty())
    {
        ii cur = Q.front(); Q.pop();

        if (cur.first == 0 || cur.second == 0 || cur.first == n - 1 || cur.second == m - 1)
        {
            res = true;
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

                    if (ci >= 0 && cj >= 0 && ci < n && cj < m && arr[ci][cj] == '.' && !visited[ci][cj])
                    {
                        visited[ci][cj] = true;
                        Q.push(ii(ci, cj));
                    }
                }
            }
        }
    }

    for (int i = 0; i < n; i++)
        delete[] visited[i];

    delete[] visited;

    return res;
}

int main()
{
    scanf("%d %d\n", &n, &m);

    arr = new char*[n];
    for (int i = 0; i < n; i++)
    {
        arr[i] = new char[m];
        for (int j = 0; j < m; j++)
        {
            scanf("%c", arr[i] + j);
        }

        scanf("\n");
    }

    bool reached_robots = false;
    for (int i = 0; !reached_robots && i < n; i++)
    {
        for (int j = 0; !reached_robots && j < m; j++)
        {
            if (arr[i][j] == 'X' && can_escape(i, j))
            {
                reached_robots = true;
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

