// #include<stdio.h>
// #include<stdlib.h>

// int reversearr(int arr[], int n){

//     int array[n];
//     for(int i=0;i<n;i++){
//         array[i]= arr[n-i-1];
//     }

//     for(int i=0;i<n;i++){
//         printf("%d ", array[i]);
//     }
// }

// int main(){
//     // int arr[]={1,2,3 ,4,6};
//     // int size= sizeof(arr)/sizeof(arr[0]);

//     int n;
//     printf("Enter the size : ");
//     int *arr = (int*)malloc(n*sizeof(int));
//     scanf("%d", &n);

//     printf("enter the array :");
//     for(int i=0;i<n;i++){
//         scanf("%d", &arr[i]);
//     }

//     reversearr(arr,n);

//     return 0;
// }

// #include<stdio.h>
// int main(){
//     int i={1,2,3,4,5,6,7,8,9,10};
//     int a[i];
//     // int b[10]={2,4,6,8,10,12,14,16,18,20};
//     // int c[10]={3,6,9,12,15,18,21,24,27,30};
//     // for(i=-20;i<=10;i++)
//     printf("%d",*&a[3]);
// }

#include <stdio.h>
int main()
{
    int i, n, mx = 0, mx2=0, diff;
    int a[] = {2, 4, 8, 1, 6, 7, 10, 5, 3, 20};
    n = sizeof(a) / sizeof(a[0]);
    for (i = 0; i <= (n - 1); i++)
    {
        if (mx < a[i]){
        mx = a[i];
            if(mx2<mx && mx2<a[i])
            mx2;
        }
    }
    printf("%d %d",mx,mx2);
}
