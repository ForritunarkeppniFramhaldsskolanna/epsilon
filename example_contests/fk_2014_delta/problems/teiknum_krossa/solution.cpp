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

char arr[1100][1100];

#define VALID(i,j) ((i) >= 0 && (i) < n && (j) >= 0 && j < n && arr[i][j] == '#')

int main()
{
    int n;
    scanf("%d\n", &n);

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            scanf("%c", arr[i] + j);
        }

        scanf("\n");
    }

    bool ok = true;
    for (int i = 0; ok && i < n; i++)
    {
        for (int j = 0; ok && j < n; j++)
        {
            if (arr[i][j] == '#')
            {
                ok = ok && VALID(i,j);
                ok = ok && VALID(i+1,j);
                ok = ok && VALID(i+2,j);
                ok = ok && VALID(i+1,j-1);
                ok = ok && VALID(i+1,j+1);

                if (!ok)
                    break;

                arr[i][j] = '.';
                arr[i+1][j] = '.';
                arr[i+2][j] = '.';
                arr[i+1][j-1] = '.';
                arr[i+1][j+1] = '.';
            }
        }
    }

    if (ok)
        printf("Jebb\n");
    else
        printf("Neibb\n");

    return 0;
}

