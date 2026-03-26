# Pandas入门

## 0.基本库导入

这里只做conda的演示，在激活需要的环境的前提下运行如下代码

```
conda install pandas
```

然后在vscode中选择对应的解释器和环境，写下这一行代码，测试是否报错

```python
import pandas as pd # as后面内容非必要
```

## 1.数据创建

### DataFrame：

下面演示一个最简单的创建

```python
data=pd.DataFrame({"1":[1,2],"2":[3,4]}) # 好孩子不要这样写代码
```

这其实是一个字典的形式，创建出来的本质上是一个表格。

当我们没有加入index参数的时候，这个表格的横向是默认的参数，也就是0，1……

其实就是字典里面塞列表（

想要指定横向的参数，那么就需要我们加入index参数，就例如这样子

```python
data = pd.DataFrame({"1": [1, 2], "2": [3, 4]}, index=[5, 6])  # 好孩子不要这样写代码
```

### Series：

Series只需要一个列表就可以创建

```python
data = pd.Series([1, 2, 3, 4, 5])
```

事实上我们可以把Series是作为DataFrame的一个单列，但是它不具有列名，只有一个整体的name。

但好处是，它一样可以使用index参数

```python
data = pd.Series([1, 2, 3, 4, 5], index=[1, 2, 3, 4, 5])
```

Series 和 DataFrame 密切相关。将 DataFrame 视为实际上只是一堆 Series“粘合在一起”会很有帮助。

### 读取数据文件：

大多数情况下，我们是不会手动去撸文件的，一般会用csv来操作，而我们在前面已经用过csv了，这里就不多赘述

可以使用`pd.read_csv()`的形式去读入DataFrame，具体操作是这样的

```python
wine_reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv")
```

并且可以使用`shape`属性来检查生成的DataFrame大小，可以使用`head`命令来查看DataFrame的内容，但这个命令只会读取前五条数据

如果CSV 文件自带一个索引，但 pandas 并未自动识别。为了让 pandas 使用该列作为索引（而不是从头创建新索引），我们可以指定一个 `index_col` 。

```python
wine_reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)
```

## 2.索引，选择，与赋值

### 基于位置

在python中，我们访问对象的属性来获取属性值，例如说一个book对象有title属性，那么就可以写`book.title`来访问它，同样的，读取完一个csv文件之后我们也可以通过访问表头来获取属性

就像我拿泥福教务处那个csv文件的前五个数据来举例子

```python
data = pd.read_csv("information.csv")
a = data.head()
print(a.日期)
# 变量名可以写中文这个对我的世界观冲击还是太大了
```

也可以使用这样子的方法来访问

```python
data = pd.read_csv("information.csv")
a = data.head()
print(a.iloc[0])
```

这个方法其实读取的是第一行的内容，无论是`loc`还是`iloc`都是行优先，列次之，这和原生python中完全不一样的。但这也代表着，获取列变得更麻烦了，但是可以采用这样子的方法

```python
data = pd.read_csv("information.csv")
a = data.head()
print(a.iloc[:, 0])
```

这个截取行和列的方法和`numpy`基本一样，就不多说了。

但是还有一点，这东西可以传列表进去，例如这样子

```python
data = pd.read_csv("information.csv")
a = data.head()
print(a.iloc[[0,2,4], 0])
```

### 基于标签

`loc`运算符可以实现基于标签的选择，例如这个样子

```python
data = pd.read_csv("information.csv")
a = data.head()
print(a.loc[0,"日期"])
```

`iloc` 在概念上比 `loc` 更简单，因为它忽略了数据集的索引。当我们使用 `iloc` 时，我们将数据集视为一个大矩阵（列表的列表），必须通过位置进行索引。相比之下， `loc` 利用索引中的信息来完成工作。由于你的数据集通常具有有意义的索引，使用 `loc` 通常更容易操作。

用这两个东西有一个不得不品的那就是他们的索引方式是不同的，`iloc`就是我们直觉中的左闭右开区间，但是，`loc`却是一个左闭右闭区间，也就是说，在`loc`中使用`0:10`那么他会直接给你索引0-10的所有内容，而不是我们直觉里的0-9。

那么这是为什么呢，看看这个解释吧

> 为何有此差异？请记住 loc 可以索引任何标准库类型：例如字符串。如果我们有一个索引值为 `Apples, ..., Potatoes, ...` 的 DataFrame，并且想要选择“苹果和土豆之间所有按字母顺序排列的水果选项”，那么索引 `df.loc['Apples':'Potatoes']` 比索引类似 `df.loc['Apples', 'Potatoet']` 的方式要方便得多（因为 `t` 在字母表中位于 `s` 之后）。

### 操作索引

在`pandas`中`set_index`是一个很重要的方法，它可以将一个貌似无关的列数据转为一个索引，而通过这个操作，我们就可以直接利用索引进行访问。

### 条件筛选

然而，实际应用中我们还是要用到条件筛选的特性的，例如说我们可以用这样子的语句来检查一行数据的某个属性是不是我们想要的

```python
reviews.country == 'Italy'
```

（这是教学文档的例子）

这个会生成一个布尔值，就可以用它在内部去筛选相关的数据了。

```python
reviews.loc[reviews.country == 'Italy']
```

以福大的csv为例

```python
data = pd.read_csv("information.csv")
a = data.head()
print(a.loc[a.发布单位=="教学运行"])
```

同样的，这是支持两个问题合并的，就像C++里面一样，我们用`&`表示两个条件要同时满足，用`|`表示两个条件满足一个就可以了

照样子以福大的csv为例

```python
data = pd.read_csv("information.csv")
a = data.head()
print(a.loc[(a.发布单位=="教学运行")&(a.日期=="2023-05-24")])
```

还可以这样

```python
data = pd.read_csv("information.csv")
a = data.head()
print(a.loc[(a.发布单位=="教学运行")|(a.日期=="2023-05-24")])
```



`Pandas`内置了一些条件选择器，例如`isin`

`isin`的用法很简单，就是下面这样的

```python
data = pd.read_csv("information.csv")
a = data.head()
b=a.loc[a.发布单位.isin(["教学运行","教研教改"])]
```

感觉本质上还是和上面那种一样的啊，不过这种写法以列表的形式传入，应该会更加灵活一点

还有一种是`isnull`和它的配套方法`notnull`这两个方法允许去高亮显示空和非空的值，可以用这种方法来筛选出来数据中缺少某项数据的项目。

```python
data = pd.read_csv("information.csv")
a = data.head()
b = a.loc[a.文件下载次数.isnull()]
```

### 数据分配

可以这样子将数据分配给DataFrame

```python
reviews['critic'] = 'everyone'
reviews['critic']
```

允许使用可迭代的值

```python
reviews['index_backwards'] = range(len(reviews), 0, -1)
reviews['index_backwards']
```

## 3.汇总函数与映射

### 摘要函数

`pandas`提供了一些方法用于重构数据，例如`describe`方法

```python
reviews.points.describe()
```

这个可以快速的汇总出来几个数据



如果想要获取某列的平均值，那么可以使用`mean`函数来获取平均值，就例如这样

```python
reviews.points.mean()
```

想要查看唯一值的列表，那么可以使用`unique`函数来进行操作

```python
reviews.taster_name.unique()
```

如果同时还要出现的频率，那么可以使用`value_counts`方法

```python
reviews.taster_name.value_counts()
```



我们可以利用map方法来对DataFrame中的每一个Series进行修改，就例如说，我们想要以平均数为基准对数据进行调整就可以这么做

```python
review_points_mean = reviews.points.mean()
reviews.points.map(lambda p: p - review_points_mean)
```

传递给map方法的参数应该是一个Series，其实也就是其中一列（



apply也是一样的，但是更加自由一点，可以对行进行操作

```python
def remean_points(row):
    row.points = row.points - review_points_mean
    return row

reviews.apply(remean_points, axis='columns')
```

如果我们用 `axis='index'` 调用 `reviews.apply()` ，那么就不是传递一个函数来转换每一行，而是需要提供一个函数来转换每一列。

请注意， `map()` 和 `apply()` 分别返回经过转换的新 Series 和 DataFrame。它们不会修改被调用的原始数据。如果我们查看 `reviews` 的第一行，可以看到它仍然保留着原始的 `points` 值。



但是，其实还有更快的（

```python
review_points_mean = reviews.points.mean()
reviews.points - review_points_mean
```

更快的代价是，不灵活

## 4.分组与排序

pandas提供了`groupby()`方法来对数据进行分组，其实本质上可以视为这个操作是我们在做切片，把表格中的几个数据切片下来干活

就例如这样子

```python
reviews.groupby('points').points.count()
```

这里感觉有必要将一个`groupby`函数返回的是一个什么对象，我直觉以为返回的是一个DataFrame对象，但实际上不是的，返回的是一个DataFrameGroupBy对象。可以将这个对象理解为是一个中间产物，只有我们对这个对象使用了sum方法才能把它变成一个DataFrame对象

当然，可以用apply方法去访问这个数据切片并且做处理

```python
reviews.groupby('winery').apply(lambda df: df.title.iloc[0])
```

同样的，支持更加灵活的方法，也就是通过列表的形式一下子切一大片下来

```python
reviews.groupby(['country', 'province']).apply(lambda df: df.loc[df.points.idxmax()])
```



`agg`方法是一个很有意思的东西，这个东西允许我们同时允许一系列不同的函数，例如这个样子

```python
reviews.groupby(['country']).price.agg([len, min, max])
```

### 多重索引

事实上，利用`groupby`传递列表进行数据拆分的时候会默认生成一个具有多重索引的结果，这个特性可以帮助我们更精准的去定位结果，就例如这个样子

| **country**   | **province**         | **len** |
| ------------- | -------------------- | ------- |
| **Argentina** | **Mendoza Province** | 3264    |
|               | **Other**            | 536     |
| **Australia** | **New South Wales**  | 85      |
|               | **Victoria**         | 322     |

但是这个时候的问题就出现了，一旦我们想要直接通过country去访问里面的数据，那么会直接报错，因为这个时候country是索引，而不是普通的列，需要用到loc去访问

多重索引与常规索引最大的不同点就在于它具有多个层级，那么要怎么去访问，直观的思路是套一大堆loc去访问，但是这种方法理论上确实是可以访问，但是有点小众且变态。最好的方法是通过传入元组的方法去访问

例如这样`df.loc[('China', 'Guangdong'), 'description']`

当然也可以用范围切片，这样子`df.loc[idx[:, 'California':'New York'], :]`

如果想要跨越外层索引直接找内层，可以用`.xs`方法，这样`df.xs('Tuscany', level='province')`

可以利用``reset_index()``方法把多重索引转回常规索引

### 排序

如果我们想要按特定的顺序获取值，那么就需要对数据进行排序，利用`sort_value()`方法就相当方便。

```python
countries_reviewed = countries_reviewed.reset_index()
countries_reviewed.sort_values(by='len')
```

（想要怎么排自己填，默认升序）

如果我们想要降序的怎么办呢？加入一个参数，就像这样

```python
countries_reviewed.sort_values(by='len', ascending=False)
```

按照索引值排序可以使用`sort_index`这个方法具有相同的参数和默认顺序

你知道的，by那个参数还可以传列表，也就是可以多个列进行排序

## 5.数据类型与缺失值

DataFrame 或 Series 中列的数据类型被称为 dtype。

完全由字符串组成的列是不会有自己的类型的，会被赋予object类型

通过使用 `astype()` 函数，可以在有意义的情况下将一列从一种类型转换为另一种类型。例如

```python
reviews.points.astype('float64')
```

### 缺失数据

缺失的条目会被赋予NaN值，由于一些原因，这个数据类型是`float64`

我们前面说过了如何去找到缺失的数据类型，利用`pd.notnull`，配套方法是`pd.isnull`

我们可以利用`fillna()`方法来对缺失值进行替换，例如这样子

```python
reviews.region_2.fillna("Unknown")
```

非空值替换可以使用`replace()`方法

```python
reviews.taster_twitter_handle.replace("@kerinokeefe", "@kerino")
```

## 6.重命名与合并

### 重命名

`rename`方法允许我们去更改索引名称/列名，例如这样

```python
reviews.rename(columns={'points': 'score'})
```

详细一点讲，就是这样子的

```python
df.rename(columns={'旧列名': '新列名'}, index={'旧索引': '新索引'}, inplace=False)
```

甚至有更疯狂的，可以同时修改多个列名

```python
df = df.rename(columns={
    'description': 'desc',
    'points': 'score',
    'price': 'cost'
})
```

也可以用函数作批量处理，例如说想要把所有列名都变成大写，或者去掉空格啥的

```python
# 将所有列名变为大写
df = df.rename(columns=str.upper)

# 去掉列名前后的空格
df = df.rename(columns=lambda x: x.strip())
```

如果说，我们要改一整个层级的名称呢，要用另一个方法`rename_axis`

```python
# 修改多重索引的名字
df = df.rename_axis(['Nation', 'Region'], axis='index')
```

### 合并

合并最常用的是这三个方法``merge`、`join`、`concat`，然而，大多数情况下

`merge`可以实现的大部分功能`join`也做得到。

最简单的合并方法就是`concat`给定一个元素列表，这个函数就会沿着某个轴把这些元素压合在一起

举一个例子

```python
canadian_youtube = pd.read_csv("../input/youtube-new/CAvideos.csv")
british_youtube = pd.read_csv("../input/youtube-new/GBvideos.csv")

pd.concat([canadian_youtube, british_youtube])
```

这个方法就是实现了把这几个视频合并起来研究，大多数情况下返回的是一个新的DataFrame

只有当你合并的对象**全部都是 Series**，并且是**纵向合并**（`axis=0`，默认值）时，返回的才是一个长 Series。

返回的对象永远是新的，不会修改原始数据

concat方法在做的工作是堆叠，主要是行变多了，但join做到工作是对齐，也就是列变多了

举个例子

> 没问题，我们用一个**“老师点名册”**和**“考试成绩单”**的例子，让你秒懂 `concat` 和 `join` 的区别。
>
> 假设我们有两张小表格：
>
> Python
>
> ```
> import pandas as pd
> 
> # 表1：学生名单 (df1)
> df1 = pd.DataFrame({
>     'Name': ['Alice', 'Bob'],
>     'Age': [15, 16]
> }, index=[0, 1])
> 
> # 表2：新转来的学生名单 (df2)
> df2 = pd.DataFrame({
>     'Name': ['Charlie', 'David'],
>     'Age': [14, 15]
> }, index=[2, 3])
> 
> # 表3：考试成绩 (df3) - 注意索引和 df1 是对应的
> df3 = pd.DataFrame({
>     'Score': [95, 88]
> }, index=[0, 1])
> ```
>
> ------
>
> ### 1. 使用 `concat`：就像“接龙”
>
> **场景：** 学期中旬，班里新转来了两个学生（Charlie 和 David），你需要把他们的名单**接在原名单下面**。
>
> Python
>
> ```
> # 纵向堆叠：把 df2 贴在 df1 下面
> result_concat = pd.concat([df1, df2])
> ```
>
> **结果：** 变成了一个 4 行的表格。它只是简单地把行数变多了。
>
> ------
>
> ### 2. 使用 `join`：就像“填表”
>
> **场景：** 考试结束了，你手里有一份成绩单（df3），你想根据**学生的编号（索引）**，把分数填到原名单（df1）的右边。
>
> Python
>
> ```
> # 横向合并：根据索引把 df3 的列加到 df1 旁边
> result_join = df1.join(df3)
> ```
>
> **结果：** 依然是 2 行，但多了一列 `Score`。它是根据左边的索引 `0, 1` 去找右边对应的 `0, 1`。
>
> ------
>
> ### 3. 核心区别总结图解
>
> | **操作**     | **动作** | **结果变化**         | **你的直观感受**                         |
> | ------------ | -------- | -------------------- | ---------------------------------------- |
> | **`concat`** | **堆叠** | 主要是**行**变多了。 | 像是在文档后面**续写**了几页。           |
> | **`join`**   | **对齐** | 主要是**列**变多了。 | 像是在现有的表格右边**增加**了一项信息。 |
>
> ------
>
> ### 4. 进阶：如果索引对不上会怎样？
>
> 这是 `join` 最厉害的地方。假设成绩单（df3）里只有编号 `0`（Alice）的成绩，没有编号 `1`（Bob）的：
>
> Python
>
> ```
> df3_short = pd.DataFrame({'Score': [95]}, index=[0])
> result = df1.join(df3_short)
> ```
>
> **结果：**
>
> - Alice (索引0) 的 Score 是 95。
> - Bob (索引1) 因为在 df3 里找不到，他的 Score 会自动变成 **`NaN`**。
>
> 而 `concat(axis=1)` 如果遇到索引对不上，它会把所有的索引都列出来，导致表格变得非常零碎（很多空洞）。
>
> ------
>
> ### 总结建议
>
> - 如果你想**增加行**（比如合并 1 月和 2 月的销售额）：用 **`concat`**。
> - 如果你想**增加列**（比如给用户表增加一列“家庭住址”）：用 **`join`** 或 **`merge`**。