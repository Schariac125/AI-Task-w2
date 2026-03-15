import numpy as np


def main():
    # 创建两个数组
    points_A = np.random.randint(0, 101, size=(5, 2))
    points_B = np.random.randint(0, 101, size=(8, 2))
    # 距离矩阵
    diff = points_A[:, np.newaxis, :] - points_B[np.newaxis, :, :]
    distance_matrix = np.sqrt(np.sum(diff**2, axis=2))
    # 轴向数据聚合
    min_toB = np.min(distance_matrix, axis=1)
    # 元素查找
    mask = distance_matrix < 20
    B_nearA = np.any(mask, axis=0)
    targetB = np.where(B_nearA)[0]


if __name__ == "__main__":
    main()
