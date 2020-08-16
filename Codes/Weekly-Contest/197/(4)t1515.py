class Solution:
    def getMinDistSum(self, positions: List[List[int]]) -> float:
        def cost(c, all_points):
            tot = 0
            for i in all_points:
                tot += ((i[0]-c[0])**2+(i[1]-c[1])**2)**0.5
            return tot
        def gradient(c, all_points):
            dx, dy = 0, 0
            for i in all_points:
                dx += (c[0] - i[0])/(((i[0]-c[0])**2+(i[1]-c[1])**2)**0.5)
                dy += (c[1] - i[1])/(((i[0]-c[0])**2+(i[1]-c[1])**2)**0.5)
            s = (dx ** 2 + dy ** 2) ** 0.5
            dx = dx/s
            dy = dy/s
            return ([dx, dy])#得到梯度向量
        all_points = positions
        x = [0.5, 0.55] # 出发点
        theta = 0.03 # 学习率
        loop_max = 10000   # 最大迭代次数(防止死循环)
        epsilon = 1e-8  #设置阈值
        xb = x
        for i in range(loop_max):
            cost1 = cost(x, all_points) #梯度更新前的损失函数值
            gd = gradient(x, all_points)
            xi = [x[0] - theta * gd[0],x[1]-theta*gd[1]]#梯度更新后的新的点
            costi = cost(xi, all_points)#更新后的损失函数值
            if cost1 - costi > epsilon:#更新前损失函数值减去更新后的差大于阈值，继续循环
                x = xi
                cost1 = costi
            elif costi - cost1 > epsilon: #更新后损失函数值减去更新前的差大于阈值，说明步长过大，需要调小
                theta = theta * 0.3
            else:
                break
        c = x
        return cost(c,all_points)