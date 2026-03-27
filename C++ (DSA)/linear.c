#include <stdio.h>

// Function to search for an element in an array
int search(int arr[], int n, int x) {
  for (int i = 0; i < n; i++) {
    if (arr[i] == x) {
      return i;
    }
  }
  return -1;
}

// Function to input an array from the user 
void input(int arr[], int n) {
  for (int i = 0; i < n; i++) {
    printf("Enter element : ", i);
    scanf("%d", &arr[i]);
  }
}

// Function to display an array
void display(int arr[], int n) {
  printf("The array is: ");
  for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
  }
  printf("\n");
}

int main() {
  int n, x;
  printf("Enter the size of the array: ");
  scanf("%d", &n);

  int arr[n];
  input(arr, n);
  display(arr, n);

  printf("Enter the element to search for: ");      
  scanf("%d", &x);

  int index = search(arr, n, x);
  if (index == -1) {
    printf("Element not found\n");
  } else {
    printf("Element found at index %d\n", index);
  }
  return 0;
}