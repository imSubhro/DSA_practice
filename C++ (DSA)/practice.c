#include<stdio.h>
#include<stdlib.h>


void selesort(int arr[], int n){

  for (int i=0; i<n-1;i++){
    int mini = i;
    for(int j=i+1;j<n;j++){
      if(arr[j]<arr[mini]){
      mini=j;
      }
    int temp=arr[mini];
    arr[mini]= arr[i];
    arr[i]= temp;
    }
  }
}

void pp(int arr[],int n){
  for(int i=0;i<n;++i){
    printf("%d ", arr[i]);
  }
  printf("\n");
}

int main(){

  int arr[]={53,4,34,2,100,8};
//   printf("The array is :");
//   for(int i=0;i<100;i++){
//     printf("%d", arr[i]);
//   }
  int n = sizeof(arr)/sizeof(arr[0]);

  selesort(arr,n);

  printf("sorted array: ");
  pp(arr,n);

  return 0;

}