import math
import random

def mergesort(input):
    """
    given an array of n length
    return a sorted array
    """

    if len(input) <= 1:
        return input

    cut = len(input) // 2  # floored quotient
    top = mergesort(input[:cut])
    bottom = mergesort(input[cut:])

    i = 0
    j = 0

    output = []
    for x in range(len(input)):
        if top[i] < bottom[j]:
            output.append(top[i])
            i += 1
            if i >= len(top):
                output += bottom[j:]
                break
        else:
            output.append(bottom[j])
            j += 1
            if j >= len(bottom):
                output += top[i:]
                break

    return output






# Test 1

n = 53
original = range(1, n+1, 1)
input = list(original)
random.shuffle(input)
output = mergesort(input)

print 'unsorted:', input
print 'sorted:', output
if '|'.join([str(i) for i in original]) == '|'.join([str(i) for i in output]):
    print "Sort successfull"
print ''


# Test 2 - text, with duplicates

original = ['alpha', 'and', 'and', 'and', 'andromodia', 'b', 'c', 'd', 'and', 'e', 'x']
input = list(original)
random.shuffle(input)
output = mergesort(input)

print 'unsorted:', input
print 'sorted:', output
if '|'.join([str(i) for i in original]) == '|'.join([str(i) for i in output]):
    print "Sort successfull"
print ''


