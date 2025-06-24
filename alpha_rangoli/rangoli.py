from string import ascii_lowercase

def alphabet_rangoli(n):
    
    count_alpha = (n*2)-1 
    count_hyphen = count_alpha - 1
    total_count = count_alpha + count_hyphen 

    alphabet = ascii_lowercase[:n]
    alphabet_rangoli = []
    for i in range(n):
        left = alphabet[n:i:-1]
        center = alphabet[i]
        right = alphabet[i+1:n]
        row = "-".join(left + center + right)
        line = row.center(total_count, "-")
        
        alphabet_rangoli.append(line)

        
    len_alpha_rangoli = len(alphabet_rangoli)


    # top
    for t in range(len_alpha_rangoli-1,-1,-1):
        print(alphabet_rangoli[t]) 
    # bottom
    for p in range(1,len_alpha_rangoli):
        print(alphabet_rangoli[p]) 


n = int(input("enter size: "))
alphabet_rangoli(n)
"""
size 3:
----c----
--c-b-c--
c-b-a-b-c
--c-b-c--
----c----

size: 5
--------e--------
------e-d-e------
----e-d-c-d-e----
--e-d-c-b-c-d-e--
e-d-c-b-a-b-c-d-e
--e-d-c-b-c-d-e--
----e-d-c-d-e----
------e-d-e------
--------e--------

size: 10
------------------j------------------
----------------j-i-j----------------
--------------j-i-h-i-j--------------
------------j-i-h-g-h-i-j------------
----------j-i-h-g-f-g-h-i-j----------
--------j-i-h-g-f-e-f-g-h-i-j--------
------j-i-h-g-f-e-d-e-f-g-h-i-j------
----j-i-h-g-f-e-d-c-d-e-f-g-h-i-j----
--j-i-h-g-f-e-d-c-b-c-d-e-f-g-h-i-j--
j-i-h-g-f-e-d-c-b-a-b-c-d-e-f-g-h-i-j
--j-i-h-g-f-e-d-c-b-c-d-e-f-g-h-i-j--
----j-i-h-g-f-e-d-c-d-e-f-g-h-i-j----
------j-i-h-g-f-e-d-e-f-g-h-i-j------
--------j-i-h-g-f-e-f-g-h-i-j--------
----------j-i-h-g-f-g-h-i-j----------
------------j-i-h-g-h-i-j------------
--------------j-i-h-i-j--------------
----------------j-i-j----------------
------------------j------------------

"""
