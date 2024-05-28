-  `\+ - * / % ^ `运算，以及sin,cos,tan等lua math库自带的计算函数

![1](assets/1.png)

![1](assets/2.png)

![1](assets/3.png)

![1](assets/4.png)



阶乘、平均数、方差、随机数、弧度转度、度转弧度、对数 计算支持

- 输入e调用e (需要在计算上下文中)
![1](assets/5.png)

- 输入pi调用π (可直接调用)
![1](assets/6.png)

目前已实现函数
- 随机数
rdm(...)
![1](assets/7.png)

- 正弦
sin(x)
![1](assets/8.png)

- 双曲正弦
sinh(x)
![1](assets/9.png)

- 反正弦
asin(x)
![1](assets/10.png)

- 余弦
cos(x)
![1](assets/11.png)

- 双曲余弦
![1](assets/12.png)

- 反余弦
acos(x)
![1](assets/13.png)

- 正切
tan(x)
![1](assets/14.png)

- 双曲正切
tanh(x)
![1](assets/15.png)

- 反正切
atan(x)
![1](assets/16.png)

- 返回以弧度为单位的点(x,y)相对于x轴的逆时针角度。y是点的纵坐标，x是点的横坐标
- 返回范围从−π到π （以弧度为单位），其中负角度表示向下旋转，正角度表示向上旋转
- 与atan(y/x)相比，能够正确处理边界情况（例如x=0）
atan2(y, x)
![1](assets/17.png)

- 将角度从弧度转换为度
deg(x)
![1](assets/18.png)

- 将角度从度转换为弧度
rad(x)
![1](assets/19.png)

- 返回 x*2^y
ldexp(x, y)
![1](assets/20.png)

- 返回 e^x
exp(x)
![1](assets/21.png)

- x的平方根 sqrt(x) = x^0.5
sqrt(x)
![1](assets/22.png)

- x为底的对数, log(10, 100) = log(100) / log(10)
log(x, y)
![1](assets/23.png)

- 自然数e为底的对数
loge(x)
![1](assets/24.png)

- 10为底的对数
log10(x)
![1](assets/25.png)

- 平均值
avg(...)
![1](assets/26.png)

- 方差
var(...)
![1](assets/27.png)

- 阶乘. 支持 12! 或者 fact(12) 两种调用方式
fact(x)
![1](assets/28.png)