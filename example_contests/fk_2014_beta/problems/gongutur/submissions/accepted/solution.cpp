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
#include <complex>
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

double edist(complex<double> p1, complex<double> p2){
    return sqrt( (p2.real() - p1.real()) * (p2.real() - p1.real()) + (p2.imag() - p1.imag()) * (p2.imag() - p1.imag()) );
}

int main()
{
    int n;
    scanf("%d\n", &n);
    double res = 0.0;
    complex<double> last, cur;

    for (int i = 0; i < n; i++)
    {
        double x, y;
        scanf("%lf %lf\n", &x, &y);
        cur = complex<double>(x, y);
        if (i > 0)
            res += edist(last, cur);

        last = cur;
    }

    printf("%0.10lf\n", res);

    return 0;
}

