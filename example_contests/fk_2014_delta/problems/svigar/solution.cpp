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
    string line;
    getline(cin, line);

    int cnt = 0;
    bool ok = true;

    for (int i = 0; i < size(line); i++)
    {
        if (line[i] == '(')
        {
            cnt++;
        }
        else if (line[i] == ')')
        {
            cnt--;
            ok = ok && cnt >= 0;
        }
        else
        {
            assert(false);
        }
    }

    ok = ok && cnt == 0;

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

