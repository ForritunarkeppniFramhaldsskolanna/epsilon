#include <cstdio>
#include <iostream>
#include <string>
using namespace std;

int main()
{
    int n, m;
    scanf("%d %d\n", &n, &m);

    int *arr = new int[n];
    for (int i = 0; i < n; i++)
        arr[i] = i;

    for (int i = 0; i < m; i++)
    {
        string line;
        getline(cin, line);

        for (int j = 0; j < n - 1; j++)
        {
            if (line[2 * j + 1] == '-')
            {
                swap(arr[j], arr[j + 1]);
            }
        }
    }

    for (int i = 0; i < n; i++)
        printf("%c", arr[i] + 'A');

    // char *res = new char[n];
    // for (int i = 0; i < n; i++)
    //     res[arr[i]] = 'A' + i;

    // for (int i = 0; i < n; i++)
    //     printf("%c", res[i]);

    printf("\n");

    return 0;
}
