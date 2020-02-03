# 矩阵翻转
x = 5
y = 4
a = [[x for x in range(j,j+y)] for j in range(0,x*x,x)]

for i in a:
    print(i)

print()

def rotate(angle,arr):
    angle = angle // 90

    for _ in range(angle):
        y_len = len(arr)
        x_len = len(arr[0])
        arr = [[arr[y][x] for y in range(y_len)][::-1] for x in range(x_len)]


    for i in arr:
        print(i)

rotate(90,a)
