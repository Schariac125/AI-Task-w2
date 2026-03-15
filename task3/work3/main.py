import numpy as np

def main():
    #创建目标矩阵
    data_matrix=np.arange(100)
    data_matrix=np.reshape(data_matrix,(10,10))
    #提取出中心的4*4矩阵
    son_matrix=data_matrix[4:8,4:8]
    #创建布尔索引，把大于75的全部替换为0
    bool_idx=(data_matrix>75)
    data_matrix[bool_idx]=0
    #整体缩放
    data_matrix[np.arange(10),np.arange(10)]*=0.8
    #找出最大值与其索引
    maxx: int
    maxx=np.max(data_matrix)
    max_idx=np.argmax(data_matrix)
    row_idx,col_idx=np.unravel_index(max_idx,data_matrix.shape)
if __name__=="__main__":
    main()