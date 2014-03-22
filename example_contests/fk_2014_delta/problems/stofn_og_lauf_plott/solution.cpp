#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
    int n;
    cin >> n;

    vector<int> arr[10];
    for (int i = 0; i < n; i++)
    {
        int x;
        cin >> x;
        arr[x/10].push_back(x % 10);
    }

    for (int i = 0; i < 10; i++)
    {
        int m = arr[i].size();
        if (m > 0)
        {
            sort(arr[i].begin(), arr[i].end());

            cout << i << " ";
            for (int j = 0; j < m; j++)
            {
                cout << arr[i][j];
            }

            cout << endl;
        }
    }

    return 0;
}
