# Numpy的简单使用

## 1.前置知识

- py的基本语法
- 一些基本的线性代数知识

## 2.代码

```python
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
```

## 3.反思

这个任务真的非常简单，看完cs231n的那个Numpy速成就可以马上上手了，如果遇到不会的求助一下AI大概也能知道个差不多。