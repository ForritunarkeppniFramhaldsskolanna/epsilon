#include <vector>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <bitset>
#include <algorithm>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <string>
#include <cstring>
#include <fstream>
#include <cassert>
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
template <class T> int size(T x) { return x.size(); }

// assert or gtfo

int gcd(int a, int b)
{
    return b == 0 ? a : gcd(b, a % b);
}

int main()
{
    int a, b;
    scanf("%d %d\n", &a, &b);

    int g = gcd(a, b);
    a /= g;
    b /= g;

    printf("%d", a/b);
    a %= b;

    if (a > 0)
    {
        printf(".");

        vector<int> digits;
        map<int, int> seen;

        for (int i = 0; a != 0; i++)
        {
            if (seen.find(a) != seen.end())
            {
                int start = seen[a];
                for (int j = 0; j < start; j++)
                {
                    printf("%d", digits[j]);
                }

                printf("(");

                for (int j = start, cnt = digits.size(); j < cnt; j++)
                {
                    printf("%d", digits[j]);
                }

                printf(")");
                break;
            }

            seen[a] = i;

            a *= 10;
            digits.push_back(a/b);
            a %= b;
        }

        if (a == 0)
        {
            for (int i = 0, cnt = digits.size(); i < cnt; i++)
            {
                printf("%d", digits[i]);
            }
        }
    }

    printf("\n");
    return 0;
}

