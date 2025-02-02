#Starter code for disjoint set exercise
#Naive implementation without any optimizations

size,queries = map(int,input().split()) 

parent = list(range(size)) # each element is its own root at first.

set_sizes = [1] * size

def find(x):
   
    if parent[x] == x:
        return x
    parent[x] = find(parent[x])
    return parent[x]

def union(x,y):
    
    root_x = find(x)
    root_y = find(y)
   
    if root_x != root_y:
        if set_sizes[root_x] < set_sizes[root_y]:
            parent[root_x]=root_y
            set_sizes[root_y]+=set_sizes[root_x]
        elif set_sizes[root_x] > set_sizes[root_y]:
            parent[root_y]=root_x
            set_sizes[root_x]+=set_sizes[root_y]
        else:
            if root_x  < root_y:
                parent[root_y]=root_x
                set_sizes[root_x]+=set_sizes[root_y]
            else:
                parent[root_x]=root_y
                set_sizes[root_y] += set_sizes[root_x]

if __name__ == "__main__":
    for _ in range(queries):
        x, y = map(int,input().split())
        union(x,y)
        print(*parent)
