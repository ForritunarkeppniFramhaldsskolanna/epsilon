#include <iostream>
#include <cstring>
using namespace std;

void output(bool *arr, int n)
{
    for (int j = 1; j <= n; j++)
    {
        if (j != 1)
        {
            cout << " ";
        }

        if (arr[j])
        {
            cout << j;
        }
        else
        {
            cout << "X";
        }
    }

    cout << endl;
}

int main()
{
    int n;
    cin >> n;

    bool *arr = new bool[n + 1];
    memset(arr, 1, n + 1);

    arr[1] = false;
    for (int i = 2; i*i <= n; i++)
    {
        output(arr, n);

        if (!arr[i])
        {
            continue;
        }

        for (int k = 2; k*i <= n; k++)
        {
            arr[k*i] = false;
        }
    }

    output(arr, n);

    delete[] arr;

    return 0;
}
