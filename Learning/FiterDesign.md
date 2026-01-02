<div align=center><h1>滤波器设计手册</h1></div>

> 

- [ ] **第二阶段：模拟滤波器设计（1-2个月）**
  - [ ] **滤波器基本概念**
    - [ ] 掌握四种基本类型：低通、高通、带通、带阻
    - [ ] 理解关键性能指标：通带/阻带截止频率、纹波、衰减、过渡带
  - [ ] **经典模拟滤波器设计**
    - [ ] **巴特沃斯滤波器**：理解最大平坦特性与设计方法
    - [ ] **切比雪夫滤波器**：区分I型（通带等纹波）和II型（阻带等纹波）
    - [ ] **椭圆滤波器**：理解最陡过渡带特性
    - [ ] **贝塞尔滤波器**：理解线性相位与恒定群延迟特性
  - [ ] **设计步骤与实现**
    - [ ] 学习根据指标选择滤波器类型并确定阶数
    - [ ] 学习计算传递函数（极点/零点位置）
    - [ ] 了解无源RLC电路与有源运放电路实现
- [ ] **第三阶段：数字滤波器设计（2-3个月）**
  - [ ] **离散系统基础**
    - [ ] 掌握离散系统的差分方程与系统函数表示
    - [ ] 理解数字频率（ω）与模拟频率（Ω）的关系
  - [ ] **IIR滤波器设计**
    - [ ] 理解**冲激响应不变法**的原理与局限（可能混叠）
    - [ ] 重点掌握**双线性变换法**的步骤与预畸变校正
    - [ ] 学习设计流程：确定指标 → 转换为模拟原型 → 双线性变换
    - [ ] 了解IIR的常见结构：直接型、级联型、并联型
  - [ ] **FIR滤波器设计**
    - [ ] 理解FIR滤波器实现线性相位的条件与四种类型
    - [ ] 掌握**窗函数法**设计：矩形、汉宁、汉明、凯泽窗等
    - [ ] 了解**频率采样法**与**最优等纹波设计**（Parks-McClellan算法）
    - [ ] 学习FIR的高效结构：直接型、线性相位型
  - [ ] **滤波器分析**
    - [ ] 了解系数量化、舍入噪声等有限字长效应
    - [ ] 掌握判断IIR滤波器稳定性的方法
- [ ] **第四阶段：高级专题与工具实践（1-2个月）**
  - [ ] **多速率信号处理**
    - [ ] 理解抽取与插值的基本操作
    - [ ] 了解多相滤波器结构及其高效性
    - [ ] 学习高效滤波器组（如两通道正交镜像滤波器组QMF）的概念
  - [ ] **自适应滤波器**
    - [ ] 学习LMS（最小均方）与RLS（递推最小二乘）算法的基本原理
    - [ ] 了解其在系统辨识、噪声消除中的应用
  - [ ] **专业工具使用**
    - [ ] 熟练使用MATLAB的Filter Design & Analysis Tool或Python的PyFDA进行图形化设计
    - [ ] 学习使用Simulink进行滤波器系统建模
    - [ ] 了解在FPGA/DSP上实现滤波器的基础：定点化、流水线设计思想

***


# 复变函数基础

## 1. 复数的定义和基础运算

### 1.1 复数的定义
复数是一个可以表示为 $a + bi$ 形式的数，其中 $a$ 和 $b$ 是实数，$i$ 是虚数单位，满足 $i^2 = -1$。

这里 $a$ 称为复数的实部，记作 $\text{Re}(z)$；$b$ 称为复数的虚部，记作 $\text{Im}(z)$。

### 1.2 复数的基础运算

#### 1.2.1 加法和减法
对于两个复数 $z_1 = a + bi$ 和 $z_2 = c + di$：
$$
\begin{align*}
\text{加法：} & z_1 + z_2 = (a + c) + (b + d)i \\
\text{减法：} & z_1 - z_2 = (a - c) + (b - d)i
\end{align*}
$$

#### 1.2.2 乘法
$$
\begin{align*}
z_1 \cdot z_2 &= (a + bi)(c + di) \\
&= ac + adi + bci + bdi^2 \\
&= (ac - bd) + (ad + bc)i
\end{align*}
$$

#### 1.2.3 除法

$$
\frac{z_1}{z_2} = \frac{a + bi}{c + di} = \frac{(a + bi)(c - di)}{(c + di)(c - di)} = \frac{(ac + bd) + (bc - ad)i}{c^2 + d^2}
$$

#### 1.2.4 共轭复数
复数 $z = a + bi$ 的共轭复数定义为 $\bar{z} = a - bi$。共轭运算具有以下性质：
1. $\overline{z_1 + z_2} = \bar{z_1} + \bar{z_2}$
2. $\overline{z_1 \cdot z_2} = \bar{z_1} \cdot \bar{z_2}$
3. $\overline{\left(\frac{z_1}{z_2}\right)} = \frac{\bar{z_1}}{\bar{z_2}}$
4. $z \cdot \bar{z} = |z|^2 = a^2 + b^2$

#### 1.2.5 复数的模
复数 $z = a + bi$ 的模定义为 $|z| = \sqrt{a^2 + b^2}$。模运算具有以下性质：
1. $|z_1 \cdot z_2| = |z_1| \cdot |z_2|$
2. $\left|\frac{z_1}{z_2}\right| = \frac{|z_1|}{|z_2|}$
3. $|z_1 + z_2| \leq |z_1| + |z_2|$（三角不等式）
4. $|z_1 - z_2| \geq ||z_1| - |z_2||$

## 2. 复平面和欧拉公式

### 2.1 复平面
复平面（也称为高斯平面或Argand平面）是一个二维平面，其中横坐标表示复数的实部，纵坐标表示复数的虚部。复数 $z = a + bi$ 在复平面上对应于点 $(a, b)$。

在复平面上，复数还可以用极坐标形式表示：

$$
z = r(\cos\theta + i\sin\theta)
$$

其中：
- $r = |z| = \sqrt{a^2 + b^2}$ 是模
- $\theta = \arg(z) = \arctan\left(\frac{b}{a}\right)$ 是辐角（需要考虑象限）

### 2.2 欧拉公式
欧拉公式建立了复数指数函数与三角函数之间的关系：

$$
e^{i\theta} = \cos\theta + i\sin\theta
$$

由此，复数可以表示为指数形式：

$$
z = re^{i\theta}
$$

#### 2.2.1 欧拉公式的推导
使用泰勒级数展开：

$$
e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots
$$

$$
\cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots
$$

$$
\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots
$$

将 $x = i\theta$ 代入 $e^x$：

$$
e^{i\theta} = 1 + i\theta + \frac{(i\theta)^2}{2!} + \frac{(i\theta)^3}{3!} + \frac{(i\theta)^4}{4!} + \cdots
$$

$$
= 1 + i\theta - \frac{\theta^2}{2!} - i\frac{\theta^3}{3!} + \frac{\theta^4}{4!} + i\frac{\theta^5}{5!} - \cdots
$$

$$
= \left(1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \cdots\right) + i\left(\theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \cdots\right)
$$

$$
= \cos\theta + i\sin\theta
$$

#### 2.2.2 欧拉公式的重要推论
1. 欧拉恒等式：当 $\theta = \pi$ 时，$e^{i\pi} + 1 = 0$
2. 三角函数与指数函数的关系：

$$
\cos\theta = \frac{e^{i\theta} + e^{-i\theta}}{2}, \quad \sin\theta = \frac{e^{i\theta} - e^{-i\theta}}{2i}
$$

3. 复数的乘除运算简化：

$$
z_1 \cdot z_2 = r_1 r_2 e^{i(\theta_1 + \theta_2)}
$$

$$
\frac{z_1}{z_2} = \frac{r_1}{r_2} e^{i(\theta_1 - \theta_2)}
$$

$$
z^n = r^n e^{in\theta} \quad (\text{棣莫弗公式})
$$

## 3. 复变函数及其零点与极点

### 3.1 复变函数的定义
复变函数是从复数域到复数域的映射：
$$
f: D \subseteq \mathbb{C} \to \mathbb{C}
$$
其中 $D$ 是定义域。复变函数可以表示为 $w = f(z)$，其中 $z, w \in \mathbb{C}$。

在滤波器设计中，最常用的是有理函数形式的复变函数：

$$
H(s) = \frac{N(s)}{D(s)} = \frac{b_m s^m + b_{m-1} s^{m-1} + \cdots + b_0}{a_n s^n + a_{n-1} s^{n-1} + \cdots + a_0}
$$

其中 $s$ 是复频率变量，$N(s)$ 和 $D(s)$ 是多项式。

### 3.2 零点
#### 3.2.1 零点的定义
如果 $f(z_0) = 0$，则 $z_0$ 是函数 $f(z)$ 的零点。对于有理函数 $H(s) = \frac{N(s)}{D(s)}$，零点 $s_0$ 满足 $N(s_0) = 0$。

#### 3.2.2 零点的阶数
如果 $f(z)$ 在 $z_0$ 处可以表示为：

$$
f(z) = (z - z_0)^k g(z)
$$

其中 $g(z_0) \neq 0$，则 $z_0$ 是 $f(z)$ 的 $k$ 阶零点。

### 3.3 极点
#### 3.3.1 极点的定义
如果 $f(z)$ 在 $z_0$ 处无定义，且 $\lim_{z \to z_0} |f(z)| = \infty$，则 $z_0$ 是函数 $f(z)$ 的极点。对于有理函数 $H(s) = \frac{N(s)}{D(s)}$，极点 $s_p$ 满足 $D(s_p) = 0$。

#### 3.3.2 极点的阶数
如果 $f(z)$ 在 $z_p$ 处可以表示为：

$$
f(z) = \frac{h(z)}{(z - z_p)^k}
$$

其中 $h(z_p) \neq 0$，则 $z_p$ 是 $f(z)$ 的 $k$ 阶极点。

## 4. 留数及其计算

### 4.1 留数的定义
设 $f(z)$ 在点 $z_0$ 的邻域内除 $z_0$ 外解析，且在 $z_0$ 处有孤立奇点，则 $f(z)$ 在 $z_0$ 处的留数定义为：

$$
\text{Res}(f, z_0) = \frac{1}{2\pi i} \oint_{C} f(z) dz
$$

其中 $C$ 是以 $z_0$ 为中心、半径充分小的正向圆周。

### 4.2 留数的计算

#### 4.2.1 一阶极点
如果 $z_0$ 是 $f(z)$ 的一阶极点，则：

$$
\text{Res}(f, z_0) = \lim_{z \to z_0} (z - z_0) f(z)
$$

#### 4.2.2 $k$ 阶极点
如果 $z_0$ 是 $f(z)$ 的 $k$ 阶极点，则：

$$
\text{Res}(f, z_0) = \frac{1}{(k-1)!} \lim_{z \to z_0} \frac{d^{k-1}}{dz^{k-1}} [(z - z_0)^k f(z)]
$$

#### 4.2.3 有理函数的留数
对于有理函数 $f(z) = \frac{P(z)}{Q(z)}$，如果 $z_0$ 是 $Q(z)$ 的一阶零点且 $P(z_0) \neq 0$，则：

$$
\text{Res}(f, z_0) = \frac{P(z_0)}{Q'(z_0)}
$$

### 4.3 留数定理

#### 4.3.1 留数定理的表述
设 $f(z)$ 在区域 $D$ 内除有限个孤立奇点 $z_1, z_2, \ldots, z_n$ 外处处解析，$C$ 是 $D$ 内一条正向简单闭曲线，且 $z_1, z_2, \ldots, z_n$ 都在 $C$ 的内部，则：

$$
\oint_{C} f(z) dz = 2\pi i \sum_{k=1}^n \text{Res}(f, z_k)
$$

#### 4.3.2 留数定理的应用
留数定理在计算实积分和滤波器设计中非常有用。例如，在计算某些类型的无穷积分时：

$$
\int_{-\infty}^{\infty} f(x) dx = 2\pi i \sum_{\text{上半平面极点}} \text{Res}(f, z_k)
$$

## 5. 共形映射

### 5.1 共形映射的定义
设 $f(z)$ 在区域 $D$ 内解析，且 $f'(z) \neq 0$，则称 $f: D \to \mathbb{C}$ 是一个共形映射。共形映射具有以下性质：
1. **保角性**：映射保持两条曲线在交点处的夹角大小和方向
2. **伸缩率不变性**：在任意点 $z_0$，映射的伸缩率 $|f'(z_0)|$ 与方向无关

### 5.2 常见的共形映射

#### 5.2.1 线性变换

$$
w = az + b, \quad a \neq 0
$$

这是一个旋转、缩放和平移的组合。

#### 5.2.2 分式线性变换（莫比乌斯变换）

$$
w = \frac{az + b}{cz + d}, \quad ad - bc \neq 0
$$

分式线性变换将圆或直线映射为圆或直线。

#### 5.2.3 指数函数

$$
w = e^z
$$

将水平带形区域映射为角形区域。

#### 5.2.4 对数函数

$$
w = \ln z
$$

是指数函数的逆映射。


#### 5.2.5 共形映射的性质
1. **保角性**：保持角度大小和方向
2. **保域性**：将区域映射为区域
3. **边界对应原理**：区域的边界映射为像区域的边界
4. **黎曼映射定理**：任何单连通区域（除了整个复平面）都可以共形映射到单位圆内部

# 信号与系统


## 1、连续信号与离散信号理论

### 1.1 连续信号数学定义与分类

连续信号在数学上定义为定义在连续时间域上的函数，其时间变量 $t$ 在实数域 $\mathbb{R}$ 上连续取值：

$$
x(t): \mathbb{R} \rightarrow \mathbb{C} \quad \text{或} \quad \mathbb{R}
$$

#### 连续信号的分类

1. **确定性信号与随机信号**
   - 确定性信号：完全由确定数学表达式描述
     $$
     x(t) = A\cos(2\pi f_0 t + \phi)
     $$
   - 随机信号：统计特性已知，具体实现不确定

2. **能量信号与功率信号**
   - 能量信号：总能量有限
     $$
     E = \int_{-\infty}^{\infty} |x(t)|^2 dt \lt \infty
     $$
   - 功率信号：平均功率有限
     $$
     P = \lim_{T\to\infty} \frac{1}{T} \int_{-T/2}^{T/2} |x(t)|^2 dt \lt \infty
     $$

3. **周期信号与非周期信号**
   - 周期信号：存在最小正周期 $T_0$
     $$
     x(t + T_0) = x(t), \quad \forall t \in \mathbb{R}
     $$
   - 非周期信号：不存在这样的 $T_0$

#### 典型连续信号

*单位冲激函数：*
$$
\delta(t) = 
\begin{cases}
\infty, & t=0 \\
0, & t \neq 0
\end{cases}
\quad \text{且} \quad \int_{-\infty}^{\infty} \delta(t) dt = 1
$$

*单位阶跃函数：*
$$
u(t) = 
\begin{cases}
1, & t \geq 0 \\
0, & t &lt; 0
\end{cases}
$$

*矩形脉冲：*
$$
\text{rect}\left(\frac{t}{T}\right) = 
\begin{cases}
1, & |t| \leq T/2 \\
0, & |t| \gt T/2
\end{cases}
$$

### 1.2 离散信号数学定义与性质

离散信号在数学上定义为定义在整数时间点上的序列：

$$
x[n]: \mathbb{Z} \rightarrow \mathbb{C} \quad \text{或} \quad \mathbb{R}, \quad n \in \mathbb{Z}
$$

#### 离散信号的运算

1. **移位运算**
   $$
   y[n] = x[n - n_0]
   $$

2. **反褶运算**
   $$
   y[n] = x[-n]
   $$

3. **尺度变换**
   $$
   y[n] = x[an], \quad a \in \mathbb{Z}^+
   $$

#### 典型离散信号

*单位样本序列：*
$$
\delta[n] = 
\begin{cases}
1, & n = 0 \\
0, & n \neq 0
\end{cases}
$$

*单位阶跃序列：*
$$
u[n] = 
\begin{cases}
1, & n \geq 0 \\
0, & n &lt; 0
\end{cases}
$$

*矩形序列：*
$$
R_N[n] = 
\begin{cases}
1, & 0 \leq n \leq N-1 \\
0, & \text{其他}
\end{cases}
$$

### 1.3 连续到离散的转换：采样理论

#### 理想采样模型

理想采样过程可建模为连续信号与冲激串的乘积：

$$
x_s(t) = x(t) \cdot s(t) = x(t) \cdot \sum_{n=-\infty}^{\infty} \delta(t - nT_s)
$$

其中 $T_s$ 为采样周期，$f_s = 1/T_s$ 为采样频率。

#### 采样过程的频域分析

对采样模型取傅里叶变换：

$$
\begin{align*}
X_s(f) &= \mathcal{F}\{x(t) \cdot s(t)\} \\
&= X(f) * S(f) \\
&= X(f) * \left[ f_s \sum_{k=-\infty}^{\infty} \delta(f - kf_s) \right] \\
&= f_s \sum_{k=-\infty}^{\infty} X(f - kf_s)
\end{align*}
$$

这表明采样信号的频谱是原信号频谱的周期性延拓，周期为 $f_s$。

#### 奈奎斯特采样定理的严格证明

**定理：** 设连续信号 $x(t)$ 的最高频率分量为 $f_m$，则当采样频率 $f_s \gt 2f_m$ 时，可以从采样信号 $x_s(t)$ 中无失真地恢复原信号。

**证明：** 考虑采样信号的频域表达式，当 $f_s \gt 2f_m$ 时，频谱的周期延拓不会重叠。通过理想低通滤波器：
$$
H(f) = T_s \cdot \text{rect}\left(\frac{f}{f_s}\right) = 
\begin{cases}
T_s, & |f| &lt; f_s/2 \\
0, & |f| \geq f_s/2
\end{cases}
$$

滤波输出：

$$
\begin{align*}
Y(f) &= X_s(f) \cdot H(f) \\
&= f_s \sum_{k=-\infty}^{\infty} X(f - kf_s) \cdot H(f) \\
&= X(f) \quad \text{(由于 $H(f)$ 只保留中心周期)}
\end{align*}
$$

时域恢复公式：

$$
\begin{align*}
y(t) &= x_s(t) * h(t) \\
&= \left[ \sum_{n=-\infty}^{\infty} x(nT_s)\delta(t-nT_s) \right] * \left[ \frac{\sin(\pi f_s t)}{\pi f_s t} \right] \\
&= \sum_{n=-\infty}^{\infty} x(nT_s) \frac{\sin[\pi f_s (t-nT_s)]}{\pi f_s (t-nT_s)} \\
&= \sum_{n=-\infty}^{\infty} x(nT_s) \text{sinc}[f_s(t-nT_s)]
\end{align*}
$$

### 1.4 离散到连续的转换：信号重建

#### 理想重建

如上述公式所示，理想重建使用 sinc 函数进行插值。

#### 实际重建方法

1. **零阶保持（Zero-Order Hold）**
   $$
   x_{\text{ZOH}}(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \text{rect}\left(\frac{t-nT_s - T_s/2}{T_s}\right)
   $$

2. **一阶保持（First-Order Hold）**
   $$
   x_{\text{FOH}}(t) = \sum_{n=-\infty}^{\infty} \left[ x[n] + \frac{x[n+1]-x[n]}{T_s}(t-nT_s) \right] \cdot \text{rect}\left(\frac{t-nT_s}{T_s}\right)
   $$
## 2、卷积、系统函数与脉冲响应

### 2.1 卷积的数学定义与性质

#### 连续卷积

对于两个连续信号 $x(t)$ 和 $h(t)$，其卷积定义为：

$$
y(t) = (x * h)(t) = \int_{-\infty}^{\infty} x(\tau)h(t-\tau) d\tau
$$

**卷积性质：**

1. **交换律：** $x(t) * h(t) = h(t) * x(t)$
2. **结合律：** $[x(t) * h_1(t)] * h_2(t) = x(t) * [h_1(t) * h_2(t)]$
3. **分配律：** $x(t) * [h_1(t) + h_2(t)] = x(t) * h_1(t) + x(t) * h_2(t)$
4. **平移特性：** 若 $y(t) = x(t) * h(t)$，则 $x(t-t_0) * h(t) = y(t-t_0)$
5. **微分特性：** $\frac{d}{dt}[x(t) * h(t)] = \frac{dx(t)}{dt} * h(t) = x(t) * \frac{dh(t)}{dt}$
6. **积分特性：** $\int_{-\infty}^{t} [x(\tau) * h(\tau)] d\tau = \left[\int_{-\infty}^{t} x(\tau) d\tau\right] * h(t)$

#### 离散卷积

对于两个离散序列 $x[n]$ 和 $h[n]$，其卷积定义为：

$$
y[n] = (x * h)[n] = \sum_{k=-\infty}^{\infty} x[k]h[n-k]
$$

**卷积计算示例：** 设 $x[n] = \{1, 2, 3\}$，$h[n] = \{1, 1, 1\}$，则

$$
\begin{align*}
y[0] &= x[0]h[0] = 1 \\
y[1] &= x[0]h[1] + x[1]h[0] = 1 + 2 = 3 \\
y[2] &= x[0]h[2] + x[1]h[1] + x[2]h[0] = 1 + 2 + 3 = 6 \\
y[3] &= x[1]h[2] + x[2]h[1] = 2 + 3 = 5 \\
y[4] &= x[2]h[2] = 3
\end{align*}
$$

故 $y[n] = \{1, 3, 6, 5, 3\}$。

### 2.2 脉冲响应的物理意义

#### 连续系统脉冲响应

对于连续时间线性时不变系统，脉冲响应 $h(t)$ 定义为系统对单位冲激函数 $\delta(t)$ 的响应：

$$
h(t) = T\{\delta(t)\}
$$

#### 离散系统脉冲响应

对于离散时间线性时不变系统，脉冲响应 $h[n]$ 定义为系统对单位样本序列 $\delta[n]$ 的响应：

$$
h[n] = T\{\delta[n]\}
$$

#### 脉冲响应的物理意义

脉冲响应完全表征了LTI系统的时域特性。任何输入信号 $x(t)$（或 $x[n]$）的输出可以通过输入与脉冲响应的卷积得到：

$$
y(t) = x(t) * h(t) \quad \text{或} \quad y[n] = x[n] * h[n]
$$

### 2.3 系统函数的定义与性质

#### 连续系统系统函数

连续时间LTI系统的系统函数 $H(s)$ 定义为脉冲响应 $h(t)$ 的拉普拉斯变换：

$$
H(s) = \mathcal{L}\{h(t)\} = \int_{-\infty}^{\infty} h(t)e^{-st} dt, \quad s = \sigma + j\omega
$$

当 $s = j\omega$ 时，得到系统的频率响应：

$$
H(j\omega) = \mathcal{F}\{h(t)\} = \int_{-\infty}^{\infty} h(t)e^{-j\omega t} dt
$$

#### 离散系统系统函数

离散时间LTI系统的系统函数 $H(z)$ 定义为脉冲响应 $h[n]$ 的Z变换：

$$
H(z) = \mathcal{Z}\{h[n]\} = \sum_{n=-\infty}^{\infty} h[n]z^{-n}
$$

当 $z = e^{j\omega}$ 时，得到系统的频率响应：

$$
H(e^{j\omega}) = \mathcal{DTFT}\{h[n]\} = \sum_{n=-\infty}^{\infty} h[n]e^{-j\omega n}
$$

#### 系统函数的极零点分析

系统函数通常可表示为有理分式形式：

$$
H(z) = \frac{\sum_{k=0}^{M} b_k z^{-k}}{\sum_{k=0}^{N} a_k z^{-k}} = K \frac{\prod_{k=1}^{M} (1 - z_k z^{-1})}{\prod_{k=1}^{N} (1 - p_k z^{-1})}
$$

其中 $z_k$ 为零点，$p_k$ 为极点，$K$ 为增益常数。

### 2.4 系统稳定性与因果性判据

#### 连续系统

1. **稳定性：** 系统稳定当且仅当 $\int_{-\infty}^{\infty} |h(t)| dt \lt \infty$
2. **因果性：** 系统因果当且仅当 $h(t) = 0$，对于所有 $t \lt 0$
3. **频率域判据：** 稳定系统 $H(s)$ 的所有极点必须位于S平面的左半平面

#### 离散系统

1. **稳定性：** 系统稳定当且仅当 $\sum_{n=-\infty}^{\infty} |h[n]| \lt \infty$
2. **因果性：** 系统因果当且仅当 $h[n] = 0$，对于所有 $n \lt 0$
3. **频率域判据：** 稳定系统 $H(z)$ 的所有极点必须位于Z平面的单位圆内

## 3、线性时不变系统理论

### 3.1 线性系统的数学定义

设 $T\{\cdot\}$ 表示系统算子，对于任意输入信号 $x_1(t)$ 和 $x_2(t)$，以及任意常数 $a$ 和 $b$，系统满足：

$$
T\{a x_1(t) + b x_2(t)\} = a T\{x_1(t)\} + b T\{x_2(t)\}
$$

#### 线性性的验证示例

考虑系统 $y(t) = 2x(t) + 3$，测试其线性性：

$$
\begin{align*}
T\{a x_1(t) + b x_2(t)\} &= 2[a x_1(t) + b x_2(t)] + 3 \\
&= 2a x_1(t) + 2b x_2(t) + 3 \\
a T\{x_1(t)\} + b T\{x_2(t)\} &= a[2x_1(t) + 3] + b[2x_2(t) + 3] \\
&= 2a x_1(t) + 2b x_2(t) + 3(a+b)
\end{align*}
$$

由于 $3 \neq 3(a+b)$（除非 $a+b=1$），故系统非线性。

### 3.2 时不变系统的数学定义

系统满足时不变性，如果对于任意输入 $x(t)$ 和任意时移 $t_0$，有：

$$
\text{若 } y(t) = T\{x(t)\}，则 T\{x(t-t_0)\} = y(t-t_0)
$$

#### 时不变性验证示例

考虑系统 $y(t) = x(2t)$，测试其时不变性：

$$
\begin{align*}
T\{x(t-t_0)\} &= x(2t - t_0) \\
y(t-t_0) &= x(2(t-t_0)) = x(2t - 2t_0)
\end{align*}
$$

由于 $x(2t-t_0) \neq x(2t-2t_0)$，故系统时变。

### 3.3 LTI系统的特征函数与特征值

对于连续时间LTI系统，复指数函数 $e^{st}$ 是特征函数：

$$
T\{e^{st}\} = H(s)e^{st}
$$

其中 $H(s)$ 是对应的特征值，即系统函数。

对于离散时间LTI系统，复指数序列 $z^n$ 是特征函数：

$$
T\{z^n\} = H(z)z^n
$$

### 3.4 LTI系统的微分/差分方程描述

#### 连续系统微分方程

连续时间LTI系统可由常系数线性微分方程描述：

$$
\sum_{k=0}^{N} a_k \frac{d^k y(t)}{dt^k} = \sum_{k=0}^{M} b_k \frac{d^k x(t)}{dt^k}
$$

对两边取拉普拉斯变换（零初始条件）：

$$
\sum_{k=0}^{N} a_k s^k Y(s) = \sum_{k=0}^{M} b_k s^k X(s)
$$

得到系统函数：

$$
H(s) = \frac{Y(s)}{X(s)} = \frac{\sum_{k=0}^{M} b_k s^k}{\sum_{k=0}^{N} a_k s^k}
$$

#### 离散系统差分方程

离散时间LTI系统可由常系数线性差分方程描述：

$$
\sum_{k=0}^{N} a_k y[n-k] = \sum_{k=0}^{M} b_k x[n-k]
$$

对两边取Z变换（零初始条件）：

$$
\sum_{k=0}^{N} a_k z^{-k} Y(z) = \sum_{k=0}^{M} b_k z^{-k} X(z)
$$

得到系统函数：

$$
H(z) = \frac{Y(z)}{X(z)} = \frac{\sum_{k=0}^{M} b_k z^{-k}}{\sum_{k=0}^{N} a_k z^{-k}}
$$

## 4、信号变换域分析

### 4.1 傅里叶变换理论

#### 连续时间傅里叶变换（CTFT）

对于连续时间信号 $x(t)$，其傅里叶变换定义为：

$$
X(\omega) = \int_{-\infty}^{\infty} x(t)e^{-j\omega t} dt
$$

逆变换为：

$$
x(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} X(\omega)e^{j\omega t} d\omega
$$

#### 傅里叶变换的性质

| 性质 | 时域 | 频域 |
|------|------|------|
| 线性性 | $ax_1(t) + bx_2(t)$ | $aX_1(\omega) + bX_2(\omega)$ |
| 时移 | $x(t - t_0)$ | $e^{-j\omega t_0}X(\omega)$ |
| 频移 | $e^{j\omega_0 t}x(t)$ | $X(\omega - \omega_0)$ |
| 时间尺度 | $x(at)$ | $\frac{1}{|a|}X\left(\frac{\omega}{a}\right)$ |
| 微分 | $\frac{d^n x(t)}{dt^n}$ | $(j\omega)^n X(\omega)$ |
| 积分 | $\int_{-\infty}^t x(\tau)d\tau$ | $\frac{1}{j\omega}X(\omega) + \pi X(0)\delta(\omega)$ |
| 卷积 | $x(t) * h(t)$ | $X(\omega)H(\omega)$ |
| 乘积 | $x(t)h(t)$ | $\frac{1}{2\pi}X(\omega) * H(\omega)$ |

#### 常用信号的傅里叶变换

| 时域信号 | 频域表示 |
|----------|----------|
| 矩形脉冲 $\text{rect}\left(\frac{t}{T}\right)$ | $T \cdot \text{sinc}\left(\frac{\omega T}{2}\right) = \frac{2\sin(\omega T/2)}{\omega}$ |
| 冲激函数 $\delta(t)$ | 1 |
| 阶跃函数 $u(t)$ | $\frac{1}{j\omega} + \pi\delta(\omega)$ |
| 高斯脉冲 $e^{-at^2}$ | $\sqrt{\frac{\pi}{a}} e^{-\omega^2/(4a)}$ |

### 4.2 拉普拉斯变换理论

#### 双边拉普拉斯变换

对于连续时间信号 $x(t)$，其双边拉普拉斯变换定义为：

$$
X(s) = \int_{-\infty}^{\infty} x(t)e^{-st} dt, \quad s = \sigma + j\omega
$$

收敛域（ROC）是使积分收敛的所有 $s$ 的集合。

#### 单边拉普拉斯变换

对于因果信号，常用单边拉普拉斯变换：

$$
X(s) = \int_{0^-}^{\infty} x(t)e^{-st} dt
$$

#### 拉普拉斯变换性质

| 性质 | 时域 $x(t)$ | $s$域 $X(s)$ |
|------|-------------|--------------|
| 线性性 | $a_1x_1(t)+a_2x_2(t)$ | $a_1X_1(s)+a_2X_2(s)$ |
| 时移 | $x(t-t_0)u(t-t_0)$ | $e^{-st_0}X(s)$ |
| $s$域平移 | $e^{s_0t}x(t)$ | $X(s-s_0)$ |
| 尺度变换 | $x(at)$ | $\frac{1}{a}X\left(\frac{s}{a}\right)$ |
| 微分 | $\frac{dx(t)}{dt}$ | $sX(s) - x(0^-)$ |
| 积分 | $\int_0^t x(\tau)d\tau$ | $\frac{1}{s}X(s)$ |
| 卷积 | $x(t)*h(t)$ | $X(s)H(s)$ |
| 初值定理 | $\lim_{t\to0^+} x(t)$ | $\lim_{s\to\infty} sX(s)$ |
| 终值定理 | $\lim_{t\to\infty} x(t)$ | $\lim_{s\to0} sX(s)$ |

### 4.3 Z变换理论

#### 双边Z变换

对于离散时间信号 $x[n]$，其双边Z变换定义为：

$$
X(z) = \sum_{n=-\infty}^{\infty} x[n]z^{-n}
$$

收敛域（ROC）是使级数收敛的所有 $z$ 的集合。

#### 单边Z变换

对于因果序列，常用单边Z变换：

$$
X(z) = \sum_{n=0}^{\infty} x[n]z^{-n}
$$

#### Z变换性质

| 性质 | 时域 $x[n]$ | Z域 $X(z)$ |
|------|-------------|----------|
| 线性性 | $a_1x_1[n]+a_2x_2[n]$ | $a_1X_1(z)+a_2X_2(z)$ |
| 时移 | $x[n-n_0]$ | $z^{-n_0}X(z) + \sum_{k=1}^{n_0}x[-k]z^{k-n_0}$ |
| Z域尺度 | $a^n x[n]$ | $X\left(\frac{z}{a}\right)$ |
| 时间翻转 | $x[-n]$ | $X\left(\frac{1}{z}\right)$ |
| 卷积 | $x[n] * h[n]$ | $X(z)H(z)$ |
| 微分 | $nx[n]$ | $-z\frac{dX(z)}{dz}$ |
| 初值定理 | $x[0]$ | $\lim_{z\to\infty} X(z)$ |
| 终值定理 | $\lim_{n\to\infty} x[n]$ | $\lim_{z\to1} (z-1)X(z)$ |

#### 常用Z变换对

$\delta[n] \leftrightarrow 1, \quad \text{ROC: 全平面}$

$u[n] \leftrightarrow \frac{1}{1-z^{-1}}, \quad \text{ROC: } |z| \gt 1$

$a^n u[n] \leftrightarrow \frac{1}{1-az^{-1}}, \quad \text{ROC: } |z| \gt |a|$

$n a^n u[n] \leftrightarrow \frac{az^{-1}}{(1-az^{-1})^2}, \quad \text{ROC: } |z| \gt |a|$

$\cos(\omega_0 n) u[n] \leftrightarrow \frac{1 - z^{-1}\cos\omega_0}{1 - 2z^{-1}\cos\omega_0 + z^{-2}}, \quad \text{ROC: } |z| \gt 1$

### 4.4 离散时间傅里叶变换（DTFT）

对于离散时间信号 $x[n]$，其DTFT定义为：

$$
X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n]e^{-j\omega n}
$$

DTFT是周期为 $2\pi$ 的连续函数。

#### DTFT性质

1. **周期性：** $X(e^{j(\omega+2\pi)}) = X(e^{j\omega})$
2. **线性性：** $ax_1[n] + bx_2[n] \leftrightarrow aX_1(e^{j\omega}) + bX_2(e^{j\omega})$
3. **时移：** $x[n-n_0] \leftrightarrow e^{-j\omega n_0}X(e^{j\omega})$
4. **频移：** $e^{j\omega_0 n}x[n] \leftrightarrow X(e^{j(\omega-\omega_0)})$
5. **卷积：** $x[n]*h[n] \leftrightarrow X(e^{j\omega})H(e^{j\omega})$

### 4.5 离散傅里叶变换（DFT）

对于有限长序列 $x[n]$，$n=0,1,\dots,N-1$，其DFT定义为：

$$
X[k] = \sum_{n=0}^{N-1} x[n] e^{-j\frac{2\pi}{N}kn}, \quad k=0,1,\dots,N-1
$$

逆变换（IDFT）为：

$$
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] e^{j\frac{2\pi}{N}kn}, \quad n=0,1,\dots,N-1
$$

#### DFT与DTFT的关系

DFT是DTFT在频域的均匀采样：

$$
X[k] = X(e^{j\omega}) \big|_{\omega = \frac{2\pi k}{N}}
$$

#### DFT性质

1. **线性性：** $ax_1[n] + bx_2[n] \leftrightarrow aX_1[k] + bX_2[k]$
2. **循环移位：** $x[(n-m)_N] \leftrightarrow e^{-j\frac{2\pi}{N}km}X[k]$
3. **循环卷积：** $x[n] \circledast_N h[n] \leftrightarrow X[k]H[k]$
4. **对称性：** 对于实序列 $x[n]$，$X[k] = X^*[N-k]$


## 5、快速傅里叶变换（FFT）算法与实现

### 5.1 FFT算法的数学基础

#### DFT计算复杂度分析

直接计算N点DFT需要：
- 复数乘法：$N^2$ 次
- 复数加法：$N(N-1)$ 次

#### 旋转因子性质

定义旋转因子 $W_N = e^{-j\frac{2\pi}{N}}$，具有以下性质：

$$
\begin{align*}
W_N^{kn} &= e^{-j\frac{2\pi}{N}kn} \\
W_N^{k(n+N)} &= W_N^{kn} \\
W_N^{(k+N)n} &= W_N^{kn} \\
W_N^{N/2} &= -1 \\
W_N^{k+N/2} &= -W_N^k
\end{align*}
$$

### 5.2 基2-FFT算法推导

#### 时域抽取法（DIT-FFT）

将N点序列按奇偶分解：

$$
\begin{align*}
X[k] &= \sum_{n=0}^{N-1} x[n]W_N^{kn} \\
&= \sum_{r=0}^{N/2-1} x[2r]W_N^{2rk} + \sum_{r=0}^{N/2-1} x[2r+1]W_N^{(2r+1)k} \\
&= \sum_{r=0}^{N/2-1} x[2r]W_{N/2}^{rk} + W_N^k \sum_{r=0}^{N/2-1} x[2r+1]W_{N/2}^{rk}
\end{align*}
$$

定义：

$$
\begin{align*}
G[k] &= \sum_{r=0}^{N/2-1} x[2r]W_{N/2}^{rk} \quad \text{(偶数点DFT)} \\
H[k] &= \sum_{r=0}^{N/2-1} x[2r+1]W_{N/2}^{rk} \quad \text{(奇数点DFT)}
\end{align*}
$$

则：

$$
X[k] = G[k] + W_N^k H[k], \quad k=0,1,\dots,N-1
$$

由于 $G[k]$ 和 $H[k]$ 都是 $N/2$ 点周期序列：

$$
\begin{align*}
X[k] &= G[k] + W_N^k H[k], \quad k=0,1,\dots,N/2-1 \\
X[k+N/2] &= G[k] - W_N^k H[k], \quad k=0,1,\dots,N/2-1
\end{align*}
$$

#### 频域抽取法（DIF-FFT）

将频域输出按前后分解：

$$
\begin{align*}
X[2r] &= \sum_{n=0}^{N-1} x[n]W_N^{2rn} = \sum_{n=0}^{N/2-1} [x[n] + x[n+N/2]]W_{N/2}^{rn} \\
X[2r+1] &= \sum_{n=0}^{N-1} x[n]W_N^{(2r+1)n} = \sum_{n=0}^{N/2-1} [x[n] - x[n+N/2]]W_N^n W_{N/2}^{rn}
\end{align*}
$$

### 5.3 FFT算法的Python实现

```python
import numpy as np

def fft_recursive(x):
    """递归实现FFT"""
    N = len(x)
    if N <= 1:
        return x
    
    # 分治：偶数和奇数索引
    even = fft_recursive(x[0::2])
    odd = fft_recursive(x[1::2])
    
    # 旋转因子
    T = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N//2)]
    
    # 合并结果
    return [even[k] + T[k] for k in range(N//2)] + \
           [even[k] - T[k] for k in range(N//2)]

def fft_iterative(x):
    """迭代（位逆序）FFT"""
    N = len(x)
    
    # 位逆序置换
    j = 0
    for i in range(1, N):
        bit = N >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            x[i], x[j] = x[j], x[i]
    
    # 蝴蝶运算
    length = 2
    while length <= N:
        half_len = length // 2
        factor = np.exp(-2j * np.pi / length)
        for i in range(0, N, length):
            w = 1 + 0j
            for j in range(i, i + half_len):
                u = x[j]
                v = x[j + half_len] * w
                x[j] = u + v
                x[j + half_len] = u - v
                w *= factor
        length <<= 1
    
    return x
```

### 5.4 FFT的Verilog硬件实现

```verilog
module FFT #(
    parameter N = 1024,
    parameter DATA_WIDTH = 16
)(
    input wire clk,
    input wire rst_n,
    input wire start,
    input wire [DATA_WIDTH-1:0] data_in_real,
    input wire [DATA_WIDTH-1:0] data_in_imag,
    output reg [DATA_WIDTH-1:0] data_out_real,
    output reg [DATA_WIDTH-1:0] data_out_imag,
    output reg done
);

// 1. 双端口RAM存储输入数据
reg [DATA_WIDTH-1:0] mem_real [0:N-1];
reg [DATA_WIDTH-1:0] mem_imag [0:N-1];

// 2. 位逆序寻址
function [10:0] bit_reverse;
    input [10:0] address;
    begin
        bit_reverse = {address[0], address[1], address[2], 
                       address[3], address[4], address[5],
                       address[6], address[7], address[8],
                       address[9], address[10]};
    end
endfunction

// 3. CORDIC算法生成旋转因子
reg [15:0] cos_table [0:N/2-1];
reg [15:0] sin_table [0:N/2-1];

// 4. 蝴蝶运算单元
always @(posedge clk) begin
    if (!rst_n) begin
        // 复位
    end else if (start) begin
        // FFT计算流程
        // 阶段1：位逆序重排
        // 阶段2-10（对1024点）：log2(N)个阶段
        // 每个阶段：N/2个蝴蝶运算
    end
end

// 蝴蝶运算核心
task butterfly;
    input [DATA_WIDTH-1:0] a_real, a_imag;
    input [DATA_WIDTH-1:0] b_real, b_imag;
    input [DATA_WIDTH-1:0] twiddle_real, twiddle_imag;
    output [DATA_WIDTH-1:0] y0_real, y0_imag;
    output [DATA_WIDTH-1:0] y1_real, y1_imag;
    
    reg [DATA_WIDTH*2-1:0] temp_real, temp_imag;
    begin
        // 计算旋转乘法：b * W
        temp_real = b_real * twiddle_real - b_imag * twiddle_imag;
        temp_imag = b_real * twiddle_imag + b_imag * twiddle_real;
        
        // 蝴蝶加法和减法
        y0_real = a_real + temp_real[DATA_WIDTH+15:DATA_WIDTH];
        y0_imag = a_imag + temp_imag[DATA_WIDTH+15:DATA_WIDTH];
        
        y1_real = a_real - temp_real[DATA_WIDTH+15:DATA_WIDTH];
        y1_imag = a_imag - temp_imag[DATA_WIDTH+15:DATA_WIDTH];
    end
endtask

endmodule
```

## 6、采样定理与频域效应

### 6.1 采样定理的数学推导

#### 冲激串采样模型

连续信号 $x(t)$ 的冲激串采样表示为：

$$
x_s(t) = x(t) \cdot p(t) = \sum_{n=-\infty}^{\infty} x(t) \delta(t-nT_s)
$$

其中 $p(t) = \sum_{n=-\infty}^{\infty} \delta(t-nT_s)$ 为周期冲激串。

#### 频域分析

$p(t)$ 的傅里叶级数展开为：

$$
p(t) = \frac{1}{T_s} \sum_{k=-\infty}^{\infty} e^{j\frac{2\pi k}{T_s}t}
$$

因此采样信号：

$$
\begin{align*}
x_s(t) &= x(t) \cdot \frac{1}{T_s} \sum_{k=-\infty}^{\infty} e^{j\frac{2\pi k}{T_s}t} \\
&= \frac{1}{T_s} \sum_{k=-\infty}^{\infty} x(t) e^{j\frac{2\pi k}{T_s}t}
\end{align*}
$$

取傅里叶变换：

$$
\begin{align*}
X_s(\omega) &= \frac{1}{T_s} \sum_{k=-\infty}^{\infty} \mathcal{F}\{x(t)e^{j\frac{2\pi k}{T_s}t}\} \\
&= \frac{1}{T_s} \sum_{k=-\infty}^{\infty} X\left(\omega - \frac{2\pi k}{T_s}\right)
\end{align*}
$$

即：

$$
X_s(\omega) = \frac{1}{T_s} \sum_{k=-\infty}^{\infty} X(\omega - k\omega_s), \quad \omega_s = \frac{2\pi}{T_s}
$$

### 6.2 混叠现象的严格分析

#### 混叠的产生条件

当信号带宽 $B$ 大于 $\omega_s/2$ 时，频谱周期延拓会发生重叠：

$$
\text{混叠条件：} \omega_m \gt \frac{\omega_s}{2} \quad \text{或} \quad f_m \gt\frac{f_s}{2}
$$

#### 混叠频率计算

实际频率为 $f_a$ 的信号，在采样频率 $f_s$ 下，观测到的频率为：

$$
f_{\text{alias}} = |f_a - k f_s|, \quad k = \left\lfloor \frac{f_a}{f_s/2} \right\rfloor
$$

其中 $\lfloor \cdot \rfloor$ 表示向下取整。

#### 混叠的数学证明

设原信号 $x(t) = \cos(2\pi f_a t + \phi)$，采样后：

$$
\begin{align*}
x[n] &= \cos(2\pi f_a nT_s + \phi) \\
&= \cos(2\pi f_a \frac{n}{f_s} + \phi)
\end{align*}
$$

如果 $f_a = f_s + f_{\text{alias}}$，则：

$$
\begin{align*}
x[n] &= \cos(2\pi (f_s + f_{\text{alias}}) \frac{n}{f_s} + \phi) \\
&= \cos(2\pi n + 2\pi f_{\text{alias}} \frac{n}{f_s} + \phi) \\
&= \cos(2\pi f_{\text{alias}} \frac{n}{f_s} + \phi)
\end{align*}
$$

这正是频率为 $f_{\text{alias}}$ 的离散信号。

### 6.3 栅栏效应详细分析

#### 栅栏效应的数学描述

DFT只能观测到离散频率点：

$$
X[k] = X(e^{j\omega}) \big|_{\omega = \frac{2\pi k}{N}}, \quad k=0,1,\dots,N-1
$$

如同通过栅栏观察连续频谱，只能看到特定位置的样值。

#### 频谱泄露与栅栏效应的相互作用

实际中，有限长采样相当于加矩形窗：

$$
x_w[n] = x[n] \cdot w[n], \quad w[n] = 
\begin{cases}
1, & 0 \leq n \leq N-1 \\
0, & \text{其他}
\end{cases}
$$

频域上相当于频谱卷积：

$$
X_w(e^{j\omega}) = \frac{1}{2\pi} X(e^{j\omega}) * W(e^{j\omega})
$$

其中 $W(e^{j\omega}) = e^{-j\omega(N-1)/2} \frac{\sin(\omega N/2)}{\sin(\omega/2)}$ 是矩形窗的频谱。

#### 栅栏效应的影响量化

设真实频谱峰值为 $\omega_0$，DFT观测到的最近频率点为 $\omega_k = 2\pi k/N$，则观测误差：

$$
\Delta \omega = \omega_0 - \omega_k
$$

观测到的幅度误差：

$$
\Delta |X| = |X(e^{j\omega_0})| - |X(e^{j\omega_k})| \approx |X'(e^{j\omega_0})| \cdot \Delta \omega
$$

### 6.4 抗混叠滤波器设计

#### 理想抗混叠滤波器

理想抗混叠滤波器频率响应：

$$
H_{\text{aa}}(\omega) = 
\begin{cases}
1, & |\omega| \leq \omega_c \\
0, & |\omega| &gt; \omega_c
\end{cases}
$$

其中 $\omega_c = \pi f_s$（数字域）或 $\omega_c = 2\pi f_s/2$（模拟域）。

#### 实际滤波器设计

常用巴特沃斯滤波器，其幅度平方函数：

$$
|H(j\omega)|^2 = \frac{1}{1 + \left(\frac{\omega}{\omega_c}\right)^{2n}}
$$

$n$ 阶巴特沃斯滤波器的传递函数：

$$
H(s) = \frac{\omega_c^n}{\prod_{k=1}^{n} (s - s_k)}, \quad s_k = \omega_c e^{j\frac{\pi}{2n}(2k+n-1)}
$$

#### 滤波器参数选择

设计指标：
- 通带截止频率：$f_p = f_{\text{max}}$（信号最高频率）
- 阻带起始频率：$f_{\text{stop}} = f_s - f_{\text{max}}$
- 通带衰减：$\alpha_p$ dB
- 阻带衰减：$\alpha_s$ dB

所需滤波器阶数：

$$
n \geq \frac{\log\left[\left(10^{\alpha_s/10}-1\right)/\left(10^{\alpha_p/10}-1\right)\right]}{2\log(\Omega_s/\Omega_p)}
$$

其中 $\Omega_p = \omega_p/\omega_c$，$\Omega_s = \omega_s/\omega_c$。

### 6.5 信号重建理论

#### 理想重建滤波器

理想重建滤波器是理想低通滤波器：

$$
h_r(t) = \text{sinc}\left(\frac{\pi t}{T_s}\right) = \frac{\sin(\pi t/T_s)}{\pi t/T_s}
$$

频率响应：

$$
H_r(\omega) = 
\begin{cases}
T_s, & |\omega| \leq \pi/T_s \\
0, & |\omega| &gt; \pi/T_s
\end{cases}
$$

#### 实际DAC的零阶保持

零阶保持的时域响应：

$$
h_{\text{ZOH}}(t) = \text{rect}\left(\frac{t - T_s/2}{T_s}\right)
$$

频率响应：

$$
H_{\text{ZOH}}(\omega) = T_s \cdot \text{sinc}\left(\frac{\omega T_s}{2}\right) e^{-j\omega T_s/2}
$$

需要在DAC后接补偿滤波器：

$$
H_c(\omega) = \frac{1}{H_{\text{ZOH}}(\omega)} = \frac{e^{j\omega T_s/2}}{\text{sinc}(\omega T_s/2)}, \quad |\omega| \leq \pi/T_s
$$

### 6.6 过采样与欠采样技术

#### 过采样（Oversampling）

过采样率定义为：

$$
OSR = \frac{f_s}{2f_{\text{max}}}
$$

过采样的优势：
1. 降低抗混叠滤波器要求
2. 提高信噪比（SNR）
3. 减少量化噪声

信噪比改善：

$$
\text{SNR}_{\text{improvement}} = 10\log_{10}(OSR) \quad \text{dB}
$$

#### 欠采样（Undersampling）或带通采样

对于带通信号，带宽 $B$，中心频率 $f_c$，采样频率需满足：

$$
\frac{2f_c + B}{m+1} \leq f_s \leq \frac{2f_c - B}{m}
$$

其中 $m$ 为满足条件的最大整数。

### 6.7 量化效应分析

#### 量化误差模型

设量化步长为 $\Delta$，则量化误差 $e[n]$ 可建模为均匀分布的白噪声：

$$
p(e) = 
\begin{cases}
\frac{1}{\Delta}, & |e| \leq \Delta/2 \\
0, & \text{其他}
\end{cases}
$$

均值：$E[e] = 0$

方差：$\sigma_e^2 = \frac{\Delta^2}{12}$

#### 量化信噪比

对于满幅度正弦信号，幅度 $A = 2^{b-1}\Delta$，功率 $P_s = A^2/2$，量化噪声功率 $P_n = \Delta^2/12$，信噪比：

$$
\text{SNR} = 10\log_{10}\left(\frac{P_s}{P_n}\right) = 6.02b + 1.76 \quad \text{dB}
$$

其中 $b$ 为量化位数。

#### 过采样对量化噪声的改善

过采样将量化噪声功率分散到更宽的频带 $[-\pi,\pi]$，经过数字滤波后，噪声功率降低：

$$
\text{SNR}_{\text{OS}} = 6.02b + 1.76 + 10\log_{10}(OSR) \quad \text{dB}
$$

