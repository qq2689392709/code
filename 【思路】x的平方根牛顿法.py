class Solution:
    def mySqrt(self, x):

        b = x                               # 改写一下，显得更清楚
        x_c, y_c = b, b * b - b             # 初始化切点坐标
        while abs(y_c) > 1e-4:              # 满足阈值条件
            x_n = x_c - y_c / (2 * x_c)     # 计算下一个切点横坐标，推导公式见上文
            y_n = x_n * x_n - b             # 计算下一个切点纵坐标，推导公式见上文
            x_c, y_c = x_n, y_n             # 更新当前坐标

        return int(x_c)                     # 取出结果的整数部分即可

if __name__ == '__main__':

    print(Solution().mySqrt(4))
