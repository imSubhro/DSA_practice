#include<stdio.h>
#include<stdlib.h>


// void selectionSort(int arr[], int n){

//     for(int i=0;i<n-1;i++){
//         int mini= i;
//         for(int j=i+1;j<n;j++){
//             if(arr[j]<arr[mini]){
//                 mini =j;
//             }
//             int temp=arr[mini];
//             arr[mini]=arr[i];
//             arr[i]=temp;
//         }

//     }
// }


// void bubblesort(int arr[], int n)
// {
//     for(int i=n-1; i>=0;i--){
//         for(int j=0;j<=i-1;j++){
//             if(arr[j]>arr[j+1]){
//                 int temp= arr[j+1];
//                 arr[j+1]=arr[j];
//                 arr[j]=temp;
//             }
//         }

//     }

// }



// void insertion(int arr[], int n){
//     for(int i=0; i<=n-1;i++){
//         int j=i;
//         while(j>0 && arr[j-1]> arr[j]){
//             int temp=arr[j-1];
//             arr[j-1]=arr[j];
//             arr[j]= temp;
//             j--;
//         }
//     }
// }


// void PP(int arr[],int n) {
//         for (int i = 0; i < n; ++i) {
//             printf("%d  ", arr[i]);
//         }
//         printf("\n");
// }



// int main(){

//     int arr[]={41,85,79,20,52,3};


//     // printf("Enter nums :");
//     // for(int i=0;i<100;i++){
//     //     scanf("%d", &arr[i]);
//     // }
//     int n = sizeof(arr)/ sizeof(arr[0]);

//     selectionSort(arr,n);
//     // bubblesort(arr,n);
//     // insertion(arr,n);


//     printf("Sorted array in Acsending Order:\n");
//     PP(arr, n);

//     return 0;

// }


// MERGE_SORT

void merge(int arr[],int s, int e){
    int mid=(s+e)/2;
    int len1= mid-s+1;
    int len2= e-mid;

    int first[len1];
    int second[len2];

    int k=s;

    for(int i=0;i<len1;i++){
        first[i]=arr[k++];
    }

    k= mid+1;
    for(int i=0;i<len2;i++){
        second[i]=arr[k++];
    }


int index1=0;
int index2=0;

k=s;

while(index1<len1 && index2<len2){

    if(first[index1]<second[index2]){
        arr[k++]= first[index1++];
    }
    else{
        arr[k++]= second[index2++];
    }
}

    while(index1<len1 ){
        arr[k++] = first[index1++];
    }
    while(index2<len2){
        arr[k++]=second[index2++];
    }

}

void mergeSort(int arr[], int s, int e){
    if(s>=e){
        return;
    }

    int mid= (s+e)/2;

    mergeSort(arr,s,mid);
    mergeSort(arr, mid+1,e);

    merge(arr,s,e);

}


void PP(int arr[],int n) {
        for (int i = 0; i < n; ++i) {
            printf("%d  ", arr[i]);
        }
        printf("\n");
}

int main(){

    int arr[]={23,45,6,55,9,39};
    int n= sizeof(arr)/sizeof(arr[0]);

    mergeSort(arr,0,n-1);
    printf("Sorted array in Acsending Order:\n");
    PP(arr, n);

    return 0;
}




// QUICK_SORT

// int partition(int arr[], int low, int high){
//     int pivot = arr[high];
//     int i= low-1;

//     for(int j=low;j<=high;j++){
//         if(arr[j]<pivot){
//             i++;
//             int temp= arr[i];
//             arr[i]= arr[j];
//             arr[j]= temp;
//         }
//     }
//     int t= arr[i+1];
//     arr[i+1]=arr[high];
//     arr[high]=t;

//     return(i+1);
// }


// void quickSort(int arr[], int low , int high){
//     if(low<high){
//         int pi = partition(arr, low , high);
//         quickSort(arr, low, pi-1);
//         quickSort(arr, pi+1, high);

//     }
// }


// void PP(int arr[],int n) {
//         for (int i = 0; i < n; ++i) {
//             printf("%d  ", arr[i]);
//         }
//         printf("\n");
// }

// int main(){

//     int arr[]={23,45,6,55,9,39};
//     int n= sizeof(arr)/sizeof(arr[0]);

//     quickSort(arr,0,n-1);
//     printf("Sorted array in Acsending Order:\n");
//     PP(arr, n);

//     return 0;
// }