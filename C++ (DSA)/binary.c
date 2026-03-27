#include<stdio.h>

void input(int arr[], int n){
    for(int i=0;i<n;i++){
    printf("Enter the element :");
    scanf("%d", &arr[i]);
    }
}


void display(int arr[],int n){
    printf("The array is : ");
    for(int i=0;i<n;i++){
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int search(int arr[],int n, int x){

    int low=0, up=n-1, mid=0;
    
    while(low<=up){
        mid=(low+up)/2;
        if(arr[mid]==x)
        return mid;
        else if(x<arr[mid])
        up=mid-1;
        else
        low=mid+1;
    }
    return -1;
    
}


int main(){

    int n, x;

    printf("Enter the size of array: ");
    scanf("%d", &n);

    int arr[n];

    input(arr,n);
    display(arr,n);

    printf("Enter the key which u want to search: ");
    scanf("%d", &x);

    int index= search(arr, n,x) ;
    if (index == -1) {
    printf("Element not found\n");
    } else {
    printf("Element found at index %d\n", index);
    }
  return 0;
}