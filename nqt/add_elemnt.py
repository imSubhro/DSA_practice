def array_add_elemnent_beginning(arr,x):
    # Create a new array with the new element at the beginning
    arr.insert(0, x)
    return arr

def array_add_elemnent_end(arr,x):
    # Create a new array with the new element at the end
    arr.append(x)
    return arr

def array_add_elemnent_at_position(arr,x,pos):
    # Create a new array with the new element at the specified position
    arr.insert(pos, x)
    return arr


# Driver code
arr = [1, 2, 3, 4, 5]
x = 6
pos = 2

print("Original array:", arr)
print("Array after adding element at the beginning:", array_add_elemnent_beginning(arr.copy(), x))
print("Array after adding element at the end:", array_add_elemnent_end(arr.copy(), x))
print("Array after adding element at position", pos, ":", array_add_elemnent_at_position(arr.copy(), x, pos))

    