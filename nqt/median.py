def getMedian(arr,n):
    arr.sort() #sorting the array elements

    if n%2 == 0 :   #if arr has  even elemnts
        ind1 = n//2 - 1 #index of the first middle element
        ind2 = n//2 #index of the second middle element
        print(f"Median: {(arr[ind1] + arr[ind2]) / 2}")
    else: #if arr has odd elements
        ind = n//2
        print(f"Median: {arr[ind]}")

num = int(input("Enter the number of elements in the array: "))
arr = list(map(int, input("Enter elements: ").split()))     
getMedian(arr,num)
