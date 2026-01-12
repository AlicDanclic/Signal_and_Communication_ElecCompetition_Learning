<div align=center><h1>滤波器设计手册</h1></div>

> 

[TOC]

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

# 滤波器系统理论与设计方法

## 1.滤波器的基本分类与数学描述

### 1.1 滤波器的频率响应特性

滤波器根据其频率响应幅度的特性可分为四类基本形式。设滤波器的频率响应函数为$H(\omega)$，其中$\omega=2\pi f$为角频率。

**低通滤波器**的幅度响应满足：

$$
|H(\omega)| \approx 
\begin{cases}
1, & \text{当 } \omega < \omega_c \\
0, & \text{当 } \omega > \omega_c
\end{cases}
$$

其中$\omega_c$为截止角频率。

**高通滤波器**的幅度响应满足：

$$
|H(\omega)| \approx 
\begin{cases}
0, & \text{当 } \omega < \omega_c \\
1, & \text{当 } \omega > \omega_c
\end{cases}
$$

**带通滤波器**的幅度响应在频带$[\omega_1, \omega_2]$内近似为1，在此频带外近似为0，其中$\omega_1$为下截止频率，$\omega_2$为上截止频率，中心频率$\omega_0 = \sqrt{\omega_1\omega_2}$，带宽$BW = \omega_2 - \omega_1$。

**带阻滤波器**的幅度响应在频带$[\omega_1, \omega_2]$内近似为0，在此频带外近似为1。

### 1.2 滤波器的性能参数

**通带**定义为幅度响应满足$|H(\omega)| \geq 1/\sqrt{2} \approx 0.707$的频率范围，对应衰减不超过3 dB。**阻带**定义为幅度响应低于规定衰减值$A_{\min}$的频率范围，通常$A_{\min}$取20 dB、40 dB或更高。

**截止频率**$\omega_c$通常指幅度响应下降至通带最大值$1/\sqrt{2}$时的频率，即-3 dB点。对于具有纹波的滤波器，截止频率可定义为纹波带宽的边缘频率。

**纹波参数**$\delta_p$和$\delta_s$分别表示通带和阻带内幅度响应的最大偏差。通带纹波通常表示为：

$$
1 - \delta_p \leq |H(\omega)| \leq 1 + \delta_p, \quad \omega \in \text{通带}
$$

或以分贝表示：$R_p = -20\log_{10}(1 - \delta_p)$ dB

阻带衰减表示为：

$$
|H(\omega)| \leq \delta_s, \quad \omega \in \text{阻带}
$$

或以分贝表示：$A_s = -20\log_{10}(\delta_s)$ dB

**过渡带**为通带边缘频率$\omega_p$与阻带起始频率$\omega_s$之间的区域，即$\omega_p < \omega < \omega_s$。过渡带宽度$\Delta\omega = \omega_s - \omega_p$。

**滤波器阶数**n决定了幅度响应在过渡带的陡峭程度。对于无传输零点的滤波器，阻带衰减渐近线斜率为$-20n$ dB/十倍频程。

## 2.经典滤波器逼近函数 

### 2.1 巴特沃斯逼近

巴特沃斯滤波器在$\omega=0$处具有最大平坦幅度特性，其幅度平方函数为：

$$
|H(j\omega)|^2 = \frac{1}{1 + (\omega/\omega_c)^{2n}}
$$

其中$n$为滤波器阶数。

在$s$复平面，巴特沃斯滤波器的传递函数极点位于半径为$\omega_c$的圆上，角度间隔为$\pi/n$，且全部位于左半平面。第$k$个极点位置为：

$$
s_k = \omega_c \exp\left[j\left(\frac{\pi}{2} + \frac{(2k-1)\pi}{2n}\right)\right], \quad k=1,2,\ldots,n
$$

归一化($\omega_c=1$ rad/s)巴特沃斯多项式的系数可通过递推公式计算或查表获得。

### 2.2 切比雪夫逼近

切比雪夫I型滤波器在通带具有等波纹特性，阻带单调衰减。其幅度平方函数为：

$$
|H(j\omega)|^2 = \frac{1}{1 + \varepsilon^2 C_n^2(\omega/\omega_p)}
$$

其中$C_n(x)$为第一类切比雪夫多项式：$C_n(x)=\cos(n \arccos(x)), |x|\leq 1$；$C_n(x)=\cosh(n \operatorname{arccosh}(x)), |x|>1$。$\varepsilon$为纹波系数，与通带纹波$R_p$的关系为：$\varepsilon = \sqrt{10^{R_p/10} - 1}$。

切比雪夫II型滤波器在通带单调，阻带具有等波纹特性，其幅度平方函数为：

$$
|H(j\omega)|^2 = \frac{1}{1 + \varepsilon^2 / C_n^2(\omega_s/\omega)}
$$

切比雪夫滤波器的极点位于椭圆上，椭圆方程由纹波参数决定。

### 2.3 椭圆逼近

椭圆滤波器在通带和阻带均具有等波纹特性，提供了给定阶数下的最陡过渡带。其幅度平方函数为：

$$
|H(j\omega)|^2 = \frac{1}{1 + \varepsilon^2 R_n^2(\omega, L)}
$$

其中$R_n$为雅可比椭圆函数，$L$为选择性因子，定义为阻带起始频率与通带截止频率之比。

椭圆滤波器的传递函数包含传输零点，位于阻带内$j\omega$轴上，这使其在过渡带边缘具有极高的斜率。

### 2.4 贝塞尔逼近

贝塞尔滤波器具有最大平坦群延迟特性，其传递函数由反向贝塞尔多项式构成：

$$
B_n(s) = \sum_{k=0}^{n} a_k s^k, \quad \text{其中 } a_k = \frac{(2n-k)!}{2^{n-k} k! (n-k)!}
$$

贝塞尔滤波器的相位响应近似线性，群延迟在通带内接近常数，但幅度响应选择性较差。

## 3.滤波器设计方法

### 3.1 归一化低通原型

滤波器设计通常从归一化低通原型开始，其截止频率$\omega_c'=1$ rad/s，参考阻抗$R'=1\Omega$。原型滤波器的传递函数$H_p(s')$确定后，通过频率变换和阻抗缩放得到实际滤波器。

对于无源LC滤波器，常用梯形结构实现。元件值可通过网络综合法或查表获得。例如，$n$阶巴特沃斯低通原型的元件值($g$值)为：

$$
g_k = 2 \sin\left[\frac{(2k-1)\pi}{2n}\right], \quad k=1,2,\ldots,n
$$

### 3.2 频率变换

**低通到低通变换**：将原型频率$s'$映射为实际频率$s$，变换关系为$s' = s/\omega_c$。原型电感$L'$变换为实际电感$L = (R/\omega_c)L'$，原型电容$C'$变换为实际电容$C = C'/(R\omega_c)$。

**低通到高通变换**：变换关系为$s' = \omega_c/s$。原型电感$L'$变换为实际电容$C = 1/(R\omega_cL')$，原型电容$C'$变换为实际电感$L = R/(\omega_cC')$。

**低通到带通变换**：变换关系为$s' = \dfrac{s^2 + \omega_0^2}{BW \cdot s}$，其中$\omega_0=\sqrt{\omega_1\omega_2}$为中心频率，$BW=\omega_2-\omega_1$为带宽。原型电感$L'$变换为串联LC谐振电路：$L_s = \dfrac{R \cdot BW \cdot L'}{\omega_0^2}$，$C_s = \dfrac{1}{\omega_0^2 L_s}$。原型电容$C'$变换为并联LC谐振电路：$C_p = \dfrac{BW \cdot C'}{R\omega_0^2}$，$L_p = \dfrac{1}{\omega_0^2 C_p}$。

**低通到带阻变换**：变换关系为$s' = \dfrac{BW \cdot s}{s^2 + \omega_0^2}$。这是带通变换的逆变换。

### 3.3 滤波器阶数确定

给定通带截止频率$\omega_p$、阻带起始频率$\omega_s$、通带最大衰减$A_p$(dB)、阻带最小衰减$A_s$(dB)，可计算所需滤波器阶数。

对于巴特沃斯滤波器：

$$
n \geq \frac{\log\left[(10^{A_s/10}-1)/(10^{A_p/10}-1)\right]}{2 \log(\omega_s/\omega_p)}
$$

对于切比雪夫I型滤波器：

$$
n \geq \frac{\operatorname{arccosh}\left[\sqrt{(10^{A_s/10}-1)/(10^{A_p/10}-1)}\right]}{\operatorname{arccosh}(\omega_s/\omega_p)}
$$

## 4.无源滤波器实现

### 4.1 LC梯形网络

无源滤波器通常采用梯形网络结构，有T型和π型两种基本形式。综合方法包括影像参数法和插入损耗法。

对于双端接载的LC梯形网络（源电阻$R_s$，负载电阻$R_L$），其传递函数可通过达林顿综合法获得。该方法将给定的传递函数$H(s)$实现为无损LC网络，两端接电阻。

具体步骤：

- 由$|H(j\omega)|^2$确定反射系数$\rho(s)\rho(-s) = 1 - H(s)H(-s)$
- 选择左半平面零点构成$\rho(s)$
- 计算输入阻抗$Z_{in}(s) = R_s[1+\rho(s)]/[1-\rho(s)]$
- 通过连分式展开实现LC梯形网络

### 4.2 元件灵敏度

灵敏度$S_x^y = (\partial y/\partial x)(x/y)$表示参数$y$对元件$x$变化的敏感程度。对于滤波器，重要的灵敏度包括：

- 极点频率灵敏度：$S_{L,C}^{\omega_0} = -1/2$
- 品质因数Q灵敏度：$S_{L,C}^{Q} = \pm 1/2$（取决于电路拓扑）

无源LC滤波器的灵敏度较低，巴特沃斯逼近的灵敏度最低，椭圆逼近的灵敏度最高。

### 4.3 实际元件非理想性

实际电感包含串联电阻$R_L$，导致品质因数$Q_L = \omega L/R_L$有限。电容存在等效串联电阻ESR和寄生电感。这些非理想性影响滤波器的插入损耗和频率响应。

设计时需考虑元件值容差、温度系数和长期稳定性。通常需要容差分析，使用蒙特卡洛方法评估性能变化范围。

## 5.有源滤波器

### 5.1 有源滤波器基本结构

有源滤波器使用运算放大器、电阻和电容实现滤波功能，无需电感。基本二阶节结构包括：

**Sallen-Key结构**：电压控制电压源(VCVS)型，传递函数为：

$$
H(s) = \frac{K}{s^2RC_1C_2 + s(RC_1+RC_2-C_1R(1-K)) + 1}
$$

其中$K$为同相放大器增益（通常$K=1$为单位增益）。

**多重反馈(MFB)结构**：电流反馈型，传递函数为：

$$
H(s) = -\frac{R_2/R_1}{s^2R_2R_3C_1C_2 + sC_1(R_2+R_3+R_2R_3/R_1) + 1}
$$

**状态变量滤波器**：由积分器和加法器组成，可同时实现低通、高通和带通输出。传递函数为：

$$
H_{LP}(s) = -\frac{R_6/R_5}{s^2(R_1R_3C_1C_2)/(R_2R_4) + s(R_1C_1)/(R_2) + 1}
$$

### 5.2 运算放大器限制

有源滤波器的性能受运放参数限制：
- 增益带宽积GBW：滤波器截止频率$f_c$应满足$f_c < GBW/(10Q_{\max})$，其中$Q_{\max}$为最高品质因数
- 压摆率SR：处理大信号时，SR应满足$SR > 2\pi f_{\max} V_p$，其中$f_{\max}$为最高信号频率，$V_p$为峰值电压
- 输入阻抗和偏置电流：影响低频精度
- 噪声：决定滤波器的最小可检测信号

### 5.3 高阶有源滤波器实现

高阶滤波器通过二阶节和一阶节级联实现。$n$阶滤波器需要$\lfloor n/2 \rfloor$个二阶节，若$n$为奇数则再加一个一阶节。

级联设计步骤：
- 将高阶传递函数分解为二阶因式乘积
- 为每个二阶节分配极点和零点
- 设计各二阶节电路，通常从高Q节开始
- 确定各级增益分配以满足动态范围要求
- 级联时考虑节间阻抗匹配

## 6.滤波器设计流程

### 6.1 设计规范

给定以下滤波器规格：
- 类型：带通滤波器
- 通带：900-1100 Hz通带纹波：$\leq 0.5$ dB
- 阻带：$\leq 800$ Hz 和 $\geq 1200$ Hz
- 阻带衰减：$\geq 40$ dB
- 阻抗：600 $\Omega$

通带边缘频率：$\omega_{p1}=2\pi\times 900$，$\omega_{p2}=2\pi\times 1100$

阻带边缘频率：$\omega_{s1}=2\pi\times 800$，$\omega_{s2}=2\pi\times 1200$

中心频率：$\omega_0 = \sqrt{\omega_{p1}\omega_{p2}} \approx 2\pi\times 995$

带宽：$BW = \omega_{p2} - \omega_{p1} = 2\pi\times 200$

选择性：$\omega_{s2}/\omega_{p2} = 1200/1100 \approx 1.091$，$\omega_{p1}/\omega_{s1} = 900/800 = 1.125$

计算低通原型要求：$\Omega_s = \min(\omega_{s2}/\omega_{p2}, \omega_{p1}/\omega_{s1}) = 1.091$

对于切比雪夫I型（通带纹波0.5 dB）：

$$
n \geq \frac{\operatorname{arccosh}\left[\sqrt{(10^{40/10}-1)/(10^{0.5/10}-1)}\right]}{\operatorname{arccosh}(1.091)} \approx 7.2
$$

故选择$n=8$。

查表得8阶0.5 dB纹波切比雪夫低通原型元件值（对于π型结构）：

$$
\begin{aligned}
&g_1=1.6703, \quad g_2=1.1926, \quad g_3=2.3661, \quad g_4=0.8419, \\
&g_5=2.2404, \quad g_6=0.6555, \quad g_7=1.9841, \quad g_8=0.8140
\end{aligned}
$$


将低通原型变换为带通滤波器：
对于原型电感$L_k'$，变换为串联LC电路：

$$
\begin{aligned}
L_{sk} &= \frac{R \cdot BW \cdot L_k'}{\omega_0^2} \\
C_{sk} &= \frac{1}{\omega_0^2 L_{sk}}
\end{aligned}
$$

对于原型电容$C_k'$，变换为并联LC电路：

$$
\begin{aligned}
C_{pk} &= \frac{BW \cdot C_k'}{R\omega_0^2} \\
L_{pk} &= \frac{1}{\omega_0^2 C_{pk}}
\end{aligned}
$$

代入数值计算实际元件值：

$$
\begin{aligned}
\omega_0 &= 2\pi\times 995 \approx 6251.3 \text{ rad/s} \\
BW &= 2\pi\times 200 \approx 1256.6 \text{ rad/s} \\
R &= 600 \Omega
\end{aligned}
$$

例如，对于$g_1=1.6703$（串联电感）：

$$
\begin{aligned}
L_{s1} &= \frac{600\times 1256.6\times 1.6703}{6251.3^2} \approx 0.0322 \text{ H} = 32.2 \text{ mH} \\
C_{s1} &= \frac{1}{6251.3^2\times 0.0322} \approx 7.94\times 10^{-7} \text{ F} = 0.794 \mu\text{F}
\end{aligned}
$$

重复计算所有元件值。

作为替代方案，可采用有源滤波器实现。将8阶滤波器分解为4个二阶节级联。每个二阶节的传递函数为：

$$
H_i(s) = \frac{K_i \omega_{0i}^2}{s^2 + (\omega_{0i}/Q_i)s + \omega_{0i}^2}
$$

使用状态变量结构实现各二阶节，可独立调整中心频率和Q值。节间使用缓冲器隔离。

计算各元件对中心频率和带宽的灵敏度。对于LC谐振电路：

$$
\begin{aligned}
S_L^{\omega_0} &= S_C^{\omega_0} = -\frac{1}{2} \\
S_L^{Q} &= S_C^{Q} = \frac{1}{2}
\end{aligned}
$$

这表明元件值变化1\%会导致中心频率变化0.5\%，Q值变化0.5\%。

通过容差分析，确定元件精度要求。若要求中心频率变化小于1\%，则电感和电容容差应小于2\%。使用温度补偿电容（如NPO陶瓷）可改善温度稳定性。

### 6.2 滤波器实现中的实际问题

在较高频率下（$>10$ MHz），寄生参数影响显著：
- 电感自谐振频率：由分布电容引起，限制最大工作频率
- 电容串联电感：由引线电感引起，影响高频特性
- 印刷电路板走线电感：约1 nH/mm，在GHz范围不可忽略

滤波器的动态范围定义为最大不失真输出与等效输入噪声之比。对于有源滤波器，噪声主要来自：
- 电阻热噪声：$e_n = \sqrt{4kTRB}$，其中$k$为玻尔兹曼常数，$T$为绝对温度，$B$为带宽
- 运放电压噪声和电流噪声
- 电源噪声耦合

最小化噪声措施包括：使用低噪声运放;优化电阻值（降低热噪声但增加电流噪声）;良好的电源去耦;屏蔽和接地技术

### 6.3 现代滤波器技术

**开关电容滤波器**使用开关和电容模拟电阻，其等效电阻$R_{eq} = 1/(f_{clk} C)$，其中$f_{clk}$为时钟频率。截止频率与时钟频率成比例，易于精确控制。传递函数由电容比值决定，与绝对电容值无关，适合集成电路实现。限制包括：时钟馈通和电荷注入;有限开关速度限制最高工作频率;混叠效应需要抗混叠滤波器

**自适应滤波器**系数可实时调整，以最小化误差信号$e(n)$。最常用算法为最小均方(LMS)算法：

$$
w(n+1) = w(n) + \mu e(n) x(n)
$$

其中$w(n)$为系数向量，$\mu$为步长参数，$x(n)$为输入向量。

# 数字滤波器

## 1.数字频率与模拟频率的根本关系

要理解数字频率，必须从连续时间信号的离散化过程开始。一个模拟信号 $x_a(t)$ 经过理想采样后，得到数字序列 $x[n] = x_a(nT)$，其中 $T$ 为采样周期，其倒数 $f_s = 1/T$ 称为采样频率。

一个模拟复指数信号 $e^{j\Omega t}$ 的角频率为 $\Omega$（单位：弧度/秒）。采样后，该信号变为 $e^{j\Omega nT} = e^{j(\Omega T)n}$。我们定义 **数字频率** $\omega = \Omega T$，其单位为 **弧度/样本**。因此，数字序列可表示为 $e^{j\omega n}$。

这个关系 $\omega = \Omega T = 2\pi f / f_s$ 是连接模拟与数字领域的桥梁。它指出，数字频率 $\omega$ 本质上是模拟频率 $\Omega$ 相对于采样频率 $f_s$ 的归一化值。

由于离散时间傅里叶变换（DTFT）的周期性，数字频率 $\omega$ 通常只考虑一个 $2\pi$ 周期，例如 $[-\pi, \pi]$ 或 $[0, 2\pi]$。根据奈奎斯特-香农采样定理，为了避免混叠，模拟信号的最高频率分量必须小于 $f_s/2$。对应地，在数字频率域，有意义的最高频率为 $\omega = \pi$（对应 $\Omega = \pi f_s$）。当模拟频率超过 $f_s/2$（即 $\omega$ 超过 $\pi$）时，会产生混叠，即高频分量会被错误地映射到 $[- \pi, \pi]$ 区间内的某个低频上。

## 2.无限脉冲响应（IIR）滤波器

### 2.1 概念与数学模型

IIR滤波器的系统函数是一个有理分式：

$$
H(z) = \frac{\sum_{k=0}^{M} b_k z^{-k}}{1 - \sum_{k=1}^{N} a_k z^{-k}} = \frac{B(z)}{A(z)}
$$

其对应的差分方程为：

$$
y[n] = \sum_{k=0}^{M} b_k x[n-k] + \sum_{k=1}^{N} a_k y[n-k]
$$

该方程的特点是，当前输出 $y[n]$ 不仅依赖于当前和过去的输入 $x[n-k]$，还依赖于过去的输出 $y[n-k]$，这称为 **反馈**。正是由于反馈的存在，其单位脉冲响应 $h[n]$（即系统函数 $H(z)$ 的逆Z变换）在理论上是无限长的，故得名"无限脉冲响应"。

IIR滤波器的主要优势在于，它能够利用反馈以较低的阶数（即较少的系数）实现非常陡峭的频率选择性，计算效率较高。其主要缺点是，由于存在反馈，滤波器可能不稳定（所有极点必须在单位圆内），且通常不具有线性相位特性（除全通网络外）。

### 2.2 从模拟滤波器转换

IIR滤波器通常基于成熟的模拟滤波器原型（如巴特沃斯、切比雪夫、椭圆滤波器）进行设计，通过某种映射将模拟系统函数 $H_a(s)$ 转换为数字系统函数 $H(z)$。

#### 2.2.1 冲激响应不变法

该方法的核心是保持模拟滤波器单位冲激响应的形状，即令数字滤波器的单位脉冲响应等于模拟冲激响应的等间隔采样：$h[n] = T \cdot h_a(nT)$。这里因子 $T$ 用于补偿采样带来的幅度缩放。

设模拟滤波器的系统函数为部分分式形式：$H_a(s) = \sum_{i=1}^{N} \frac{A_i}{s - p_i}$。则其冲激响应为 $h_a(t) = \sum_{i=1}^{N} A_i e^{p_i t} u(t)$。采样后得到数字脉冲响应 $h[n] = T \sum_{i=1}^{N} A_i e^{p_i nT} u[n]$。对其取Z变换，得到数字系统函数：

$$
H(z) = T \sum_{i=1}^{N} \frac{A_i}{1 - e^{p_i T} z^{-1}}
$$

由此可见，模拟极点 $s = p_i$ 被映射为数字极点 $z = e^{p_i T}$。这种方法保持了时域响应的形态，但s平面到z平面的映射关系为 $z = e^{sT}$，它将s平面虚轴（$s=j\Omega$）映射到z平面的单位圆上（$z=e^{j\Omega T}$），频率是线性对应的 $\omega = \Omega T$。然而，由于 $e^{j(\Omega + 2\pi k/T)T} = e^{j\Omega T}$，任何模拟频率 $\Omega + 2\pi k/T$ 都会映射到同一个数字频率 $\omega$，这导致了 **频率混叠**。因此，冲激响应不变法仅适用于带限的模拟滤波器（通常是低通和带通）。

#### 2.2.2 双线性变换法

为了完全消除混叠，双线性变换采用了一种非线性的频率压缩映射。其变换公式为：

$$
s = \frac{2}{T} \cdot \frac{1 - z^{-1}}{1 + z^{-1}} \quad \text{或等价地} \quad z = \frac{1 + (T/2)s}{1 - (T/2)s}
$$

将 $s = j\Omega$ 和 $z = e^{j\omega}$ 代入上式，可以得到模拟频率 $\Omega$ 与数字频率 $\omega$ 之间的关系：

$$
j\Omega = \frac{2}{T} \cdot \frac{1 - e^{-j\omega}}{1 + e^{-j\omega}} = j \frac{2}{T} \tan\left(\frac{\omega}{2}\right)
$$

即：

$$
\Omega = \frac{2}{T} \tan\left(\frac{\omega}{2}\right) \quad \text{或} \quad \omega = 2 \arctan\left(\frac{\Omega T}{2}\right)
$$

这个正切关系表明，整个模拟频率轴 $-\infty < \Omega < \infty$ 被一一对应地、非线性地压缩到了数字频率的主值区间 $-\pi < \omega < \pi$ 内。这种非线性压缩被称为 **频率畸变**。在低频处（$\omega \ll 1$），$\tan(\omega/2) \approx \omega/2$，近似有线性关系 $\Omega \approx \omega / T$；但在高频处，畸变严重。

#### 2.2.3 预畸变

为了补偿双线性变换带来的频率畸变，需要在设计模拟原型滤波器之前，对数字频率指标进行 **预畸变**。具体步骤是：给定数字滤波器的期望截止频率 $\omega_d$，首先通过下式计算出对应的模拟原型滤波器的截止频率 $\Omega_a$：

$$
\Omega_a = \frac{2}{T} \tan\left(\frac{\omega_d}{2}\right)
$$

然后，以 $\Omega_a$ 作为技术指标去设计模拟滤波器 $H_a(s)$。最后，对此 $H_a(s)$ 应用双线性变换 $s = \frac{2}{T} \cdot \frac{1 - z^{-1}}{1 + z^{-1}}$，得到数字滤波器 $H(z)$。此时，$H(e^{j\omega})$ 在 $\omega_d$ 处将精确满足预设的衰减要求。

### 2.3 实现结构

一个给定的系统函数 $H(z)$ 可以通过不同的计算结构来实现。

#### 2.3.1 直接型

直接根据差分方程 $y[n] = \sum_{k=0}^{M} b_k x[n-k] + \sum_{k=1}^{N} a_k y[n-k]$ 实现的结构称为直接I型。通过交换分子分母的次序并共用延迟单元，可以得到所需延迟单元最少（$\max(M, N)$个）的 **直接II型（典范型）** 结构。直接型结构简单直观，但对系数量化误差非常敏感，容易导致极点位置发生较大偏移，影响稳定性。

#### 2.3.2 级联型

将系统函数 $H(z)$ 的分子和分母多项式进行因式分解，通常分解为一阶或二阶实系数因子的乘积：

$$
H(z) = K \prod_{i=1}^{L} \frac{1 + \beta_{1i}z^{-1} + \beta_{2i}z^{-2}}{1 - \alpha_{1i}z^{-1} - \alpha_{2i}z^{-2}}
$$

每个二阶节 $H_i(z) = \frac{1 + \beta_{1i}z^{-1} + \beta_{2i}z^{-2}}{1 - \alpha_{1i}z^{-1} - \alpha_{2i}z^{-2}}$ 可以用一个直接II型子滤波器实现，然后将这些子滤波器级联。级联型的优点是每一节的零极点对是独立的，便于控制滤波器的特性，并且对系数量化的敏感度低于直接型。

#### 2.3.3 并联型

将系统函数 $H(z)$ 展开成部分分式之和：

$$
H(z) = C + \sum_{i=1}^{L} \frac{\gamma_{0i} + \gamma_{1i}z^{-1}}{1 - \alpha_{1i}z^{-1} - \alpha_{2i}z^{-2}}
$$

每个二阶节（或一阶节）并行运算，最后将各支路输出相加。并联型的优点是各支路误差独立，不会相互影响，运算速度较快，且对系数量化误差的敏感度也较低。

## 3.有限脉冲响应（FIR）滤波器

### 3.1 概念与数学模型

FIR滤波器的系统函数仅包含零点（除原点处的极点外）：

$$
H(z) = \sum_{n=0}^{N-1} h[n] z^{-n}
$$

其差分方程为：

$$
y[n] = \sum_{k=0}^{N-1} h[k] x[n-k]
$$

这是一个输入信号 $x[n]$ 与有限长单位脉冲响应 $h[n]$ 的卷积和。由于没有反馈项，FIR滤波器总是稳定的。其设计焦点在于如何求取这N个系数 $h[n]$，以满足频率响应要求。FIR滤波器的主要优点是能够实现严格的线性相位，缺点是对于相同的频率选择性，其所需阶数通常远高于IIR滤波器。

### 3.2 线性相位条件

线性相位意味着滤波器的频率响应可以表示为 $H(e^{j\omega}) = A(\omega)e^{-j(\alpha\omega + \beta)}$，其中 $A(\omega)$ 是实值幅度函数，相位是频率的线性函数 $-\alpha\omega - \beta$。可以证明，当且仅当单位脉冲响应 $h[n]$ 满足某种对称性时，FIR滤波器才具有线性相位。具体分为四种类型：

**类型I**：$h[n]$ 偶对称，长度 $N$ 为奇数。即 $h[n] = h[N-1-n]$， $n=0,1,...,N-1$。其相位响应为 $\theta(\omega) = -\omega (N-1)/2$，群延迟为常数 $(N-1)/2$。它能设计所有类型的滤波器（低通、高通、带通、带阻）。

**类型II**：$h[n]$ 偶对称，长度 $N$ 为偶数。相位响应与类型I相同，但幅度响应在 $\omega=\pi$ 处必为零（$H(e^{j\pi})=0$），因此不能用于设计高通或带阻滤波器。

**类型III**：$h[n]$ 奇对称，长度 $N$ 为奇数。即 $h[n] = -h[N-1-n]$。其相位响应为 $\theta(\omega) = -\omega (N-1)/2 + \pi/2$，在零频和Nyquist频率 ($\omega=\pi$) 处幅度响应为零。适用于设计希尔伯特变换器和微分器。

**类型IV**：$h[n]$ 奇对称，长度 $N$ 为偶数。相位响应与类型III相同，在零频处幅度响应为零。适用于设计高通滤波器、希尔伯特变换器和微分器。

### 3.3 设计方法

#### 3.3.1 窗函数法

窗函数法是一种时域设计方法。首先给定一个理想的频率响应 $H_d(e^{j\omega})$，其对应的理想无限长脉冲响应为 $h_d[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} H_d(e^{j\omega}) e^{j\omega n} d\omega$。为了得到一个长度为 $N$ 的因果FIR滤波器，需要用一有限长的窗序列 $w[n]$ 来截断 $h_d[n]$：$h[n] = h_d[n] w[n]， n=0,1,...,N-1$。不同的窗函数在频域具有不同的特性，主要是主瓣宽度和旁瓣衰减的权衡。常见窗函数包括：

**矩形窗**：主瓣最窄，但旁瓣最高，阻带最小衰减约21dB。

**汉宁窗**：$w[n] = 0.5 - 0.5\cos(2\pi n/(N-1))$

**汉明窗**：$w[n] = 0.54 - 0.46\cos(2\pi n/(N-1))$，旁瓣较低且等波纹。

**布莱克曼窗**：$w[n] = 0.42 - 0.5\cos(2\pi n/(N-1)) + 0.08\cos(4\pi n/(N-1))$，旁瓣最低，但主瓣最宽。

#### 3.3.2 频率采样法

频率采样法的核心思想是在频域对期望的频率响应进行均匀采样，然后通过离散傅里叶逆变换（IDFT）得到有限长的单位脉冲响应。这一方法建立在离散傅里叶变换（DFT）理论的基础上，其数学依据是频域采样定理。

设期望的频率响应为 $H_d(e^{j\omega})$，我们希望在单位圆上均匀分布的 $N$ 个频率点 $\omega_k = \frac{2\pi}{N}k$（$k=0,1,\dots,N-1$）上，使设计的滤波器频率响应精确等于采样值：

$$
H_d[k] = H_d(e^{j\frac{2\pi}{N}k})
$$

通过 $N$ 点IDFT得到单位脉冲响应：

$$
h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H_d[k] e^{j\frac{2\pi}{N}kn}, \quad n=0,1,\dots,N-1
$$

得到的系统函数为：

$$
H(z) = \sum_{n=0}^{N-1} h[n] z^{-n}
$$

根据频域采样定理，实际滤波器的频率响应是采样值的频域内插：

$$
H(e^{j\omega}) = \sum_{k=0}^{N-1} H_d[k] \Phi\left(\omega - \frac{2\pi}{N}k\right)
$$

其中内插函数为：

$$
\Phi(\omega) = \frac{1}{N} \frac{\sin(N\omega/2)}{\sin(\omega/2)} e^{-j\omega(N-1)/2}
$$


为保证设计的FIR滤波器具有线性相位，频率采样值 $H_d[k]$ 必须满足特定的对称条件。对于四种线性相位FIR滤波器类型：

**类型I（N为奇数，偶对称）**：

幅度响应满足 $A(\omega) = A(2\pi-\omega)$，对应的频域采样值为：
$$
H_d[k] = A\left(\frac{2\pi}{N}k\right) e^{-j\frac{2\pi}{N}k\frac{N-1}{2}}
$$

且满足 $H_d[k] = H_d[N-k]^*$（共轭对称），$k=1,2,\dots,N-1$。

**类型II（N为偶数，偶对称）**：

幅度响应在 $\omega=\pi$ 处为零，采样值满足：
$$
H_d[k] = -H_d[N-k]^*
$$

且 $H_d[N/2] = 0$。

**类型III（N为奇数，奇对称）**：

幅度响应在 $\omega=0$ 和 $\omega=\pi$ 处为零，采样值满足：
$$
H_d[k] = -H_d[N-k]^*
$$

且 $H_d[0] = 0$。

**类型IV（N为偶数，奇对称）**：

幅度响应在 $\omega=0$ 处为零，采样值满足：
$$
H_d[k] = -H_d[N-k]^*
$$

且 $H_d[0] = 0$。


在理想滤波器的设计中，通带到阻带是突变的，即截止频率处 $H_d(e^{j\omega})$ 从1跳变到0。这种突变会导致实际滤波器在阻带内产生较大的旁瓣，阻带衰减不足。为改善这一状况，可以在过渡带（通常为1到3个采样点）设置非0非1的采样值，这些采样值作为可调参数进行优化。

设过渡带包含 $M$ 个采样点，其位置为 $k_1, k_2, \dots, k_M$，对应的采样值为 $T_1, T_2, \dots, T_M$。优化目标通常是最小化阻带最大旁瓣电平：

$$
\min_{T_1,\dots,T_M} \max_{\omega \in \text{阻带}} |H(e^{j\omega})|
$$

或最小化最大相对误差：

$$
\min_{T_1,\dots,T_M} \max_{\omega} \left| \frac{H(e^{j\omega}) - H_d(e^{j\omega})}{H_d(e^{j\omega})} \right|
$$

优化方法可采用梯度下降法、线性规划或直接搜索等方法。通过优化过渡带采样值，通常可将阻带衰减提高10-30dB。

设计步骤可以总结如下:

1. **确定滤波器规格**：包括通带截止频率 $\omega_p$、阻带起始频率 $\omega_s$、通带最大衰减 $\alpha_p$、阻带最小衰减 $\alpha_s$。

2. **选择滤波器长度 $N$**：根据过渡带宽度 $\Delta\omega = \omega_s - \omega_p$ 初步估计 $N \approx \frac{2\pi}{\Delta\omega}$，并确定线性相位类型。

3. **设置频域采样值**：
   - 通带内：$H_d[k] = e^{-j\frac{2\pi}{N}k\frac{N-1}{2}}$
   - 阻带内：$H_d[k] = 0$
   - 过渡带：设置1-3个优化变量 $T_i$

4. **应用对称性约束**：根据所选类型，对 $H_d[k]$ 施加相应的对称条件。

5. **优化过渡带采样值**：使用优化算法调整 $T_i$，使阻带衰减最大化或误差最小化。

6. **计算单位脉冲响应**：对优化后的 $H_d[k]$ 进行IDFT得到 $h[n]$。

7. **验证设计结果**：计算实际频率响应，检查是否满足指标要求。

频率采样法的优势在于可以直接在频域进行设计，特别适合于需要精确控制特定频率点响应的应用，如频率采样滤波器组、信道化滤波器等。其缺点是需要优化过渡带采样值才能获得良好的阻带性能，且对滤波器长度的选择较为敏感。

#### 3.3.3 最优等波纹设计（Parks-McClellan算法）

Parks-McClellan算法是基于切比雪夫逼近理论的最优化FIR滤波器设计方法，由Thomas Parks和James McClellan于1972年提出。该算法利用雷米兹（Remez）交换算法迭代求解，得到在切比雪夫意义下最优的滤波器，即在通带和阻带内具有等波纹特性。

设需要设计一个线性相位FIR滤波器，其单位脉冲响应 $h[n]$ 长度为 $N$，具有对称性。频率响应可表示为：

$$
H(e^{j\omega}) = A(\omega) e^{-j\omega(N-1)/2}
$$

其中 $A(\omega)$ 为实值幅度响应。对于不同类型的线性相位滤波器，$A(\omega)$ 有不同的表达形式：

**类型I（N为奇数，偶对称）**：

$$
A(\omega) = \sum_{k=0}^{(N-1)/2} a[k] \cos(k\omega)
$$

其中 $a[0] = h[(N-1)/2]$，$a[k] = 2h[(N-1)/2 - k]$，$k=1,2,\dots,(N-1)/2$。

**类型II（N为偶数，偶对称）**：

$$
A(\omega) = \sum_{k=1}^{N/2} b[k] \cos\left[(k-\frac{1}{2})\omega\right]
$$

其中 $b[k] = 2h[N/2 - k]$，$k=1,2,\dots,N/2$。

其余类型也有类似表达式。

定义期望的幅度响应 $D(\omega)$，对于低通滤波器：

$$
D(\omega) = 
\begin{cases}
1, & 0 \leq \omega \leq \omega_p \quad (\text{通带}) \\
0, & \omega_s \leq \omega \leq \pi \quad (\text{阻带})
\end{cases}
$$

定义加权函数 $W(\omega)$，用于控制不同频带的误差权重：

$$
W(\omega) = 
\begin{cases}
\frac{1}{\delta_p}, & 0 \leq \omega \leq \omega_p \\
\frac{1}{\delta_s}, & \omega_s \leq \omega \leq \pi
\end{cases}
$$

其中 $\delta_p$ 和 $\delta_s$ 分别为通带和阻带允许的最大纹波（波纹幅度）。

加权误差函数定义为：

$$
E(\omega) = W(\omega)[A(\omega) - D(\omega)]
$$

设计目标是寻找一组系数 $a[k]$ 或 $b[k]$，使得最大加权误差最小化：

$$
\min \max_{\omega \in \Omega} |E(\omega)|
$$

其中 $\Omega$ 为感兴趣的频带集合，包括通带和阻带。


交替定理是Parks-McClellan算法的理论基础，它给出了最优切比雪夫逼近的充要条件。

**定理**：设 $P(\omega)$ 是 $r$ 个余弦函数的线性组合（对应于类型I的 $A(\omega)$），$D(\omega)$ 是 $[0,\pi]$ 上的分段常数函数，$W(\omega)$ 是正的分段常数加权函数，$\Omega$ 是 $[0,\pi]$ 的闭子集。则 $P(\omega)$ 是 $D(\omega)$ 的唯一最优加权切比雪夫逼近的充要条件是，误差函数 $E(\omega) = W(\omega)[P(\omega) - D(\omega)]$ 在 $\Omega$ 上至少有 $r+1$ 个极值频率点 $\omega_0 < \omega_1 < \cdots < \omega_r$，使得：

$$
E(\omega_i) = -E(\omega_{i+1}), \quad i=0,1,\dots,r-1
$$

且

$$
|E(\omega_i)| = \max_{\omega \in \Omega} |E(\omega)|, \quad i=0,1,\dots,r
$$

对于类型I滤波器，$r = (N-1)/2$；类型II，$r = N/2$；类型III，$r = (N-1)/2$；类型IV，$r = N/2$。


Parks-McClellan算法实现交替定理的具体步骤如下：

1. **初始化极值频率点集**：选择 $r+1$ 个初始极值频率点 $\omega_0, \omega_1, \dots, \omega_r$，通常均匀分布在通带和阻带上，并包括边界频率 $\omega_p$ 和 $\omega_s$。

2. **求解线性方程组**：在极值点处，误差满足：
   
$$
   W(\omega_i)[P(\omega_i) - D(\omega_i)] = (-1)^i \delta, \quad i=0,1,\dots,r
$$

其中 $\delta$ 是极值点处的误差绝对值。这构成 $r+1$ 个线性方程，包含 $r+1$ 个未知数：$r$ 个滤波器系数和 $\delta$。

   对于类型I，方程可写为：

$$
   \sum_{k=0}^{r-1} a[k] \cos(k\omega_i) - \frac{(-1)^i \delta}{W(\omega_i)} = D(\omega_i), \quad i=0,1,\dots,r
$$

   其中 $r = (N-1)/2$。

3. **求解系数和 $\delta$**：通过求解上述线性方程组得到滤波器系数 $a[k]$ 和纹波值 $\delta$。可使用高效算法（如高斯消元法）求解。

4. **计算误差函数**：利用求得的系数计算整个频带上的误差函数 $E(\omega)$：
   
$$
   E(\omega) = W(\omega)\left[\sum_{k=0}^{r-1} a[k] \cos(k\omega) - D(\omega)\right]
$$

5. **寻找新的极值点**：在频带 $\Omega$ 上寻找 $E(\omega)$ 的所有局部极值点（包括边界），选择其中使 $|E(\omega)|$ 最大的 $r+1$ 个点作为新的极值频率点集。

6. **检查收敛**：如果新的极值点集与旧的相同，或者纹波值 $\delta$ 的变化小于预设容差，则算法收敛；否则返回步骤2。

7. **计算单位脉冲响应**：从最优系数 $a[k]$ 或 $b[k]$ 反推得到单位脉冲响应 $h[n]$。


在开始设计前，需要估计满足指标所需的最小滤波器阶数 $N$。Kaiser给出了一个经验公式：

$$
N \approx \frac{-10\log_{10}(\delta_p \delta_s) - 13}{2.324 \Delta\omega} + 1
$$

其中 $\Delta\omega = \omega_s - \omega_p$ 是过渡带宽度。实际应用中可能需要微调 $N$ 以满足指标。

### 3.4 实现结构

**3.4.1 直接型（横截型）**：直接实现卷积和 $y[n] = \sum_{k=0}^{N-1} h[k] x[n-k]$，需要 $N$ 个乘法器和 $N-1$ 个加法器。

**3.4.2 线性相位型**：利用 $h[n]$ 的对称性（如 $h[n] = h[N-1-n]$），可以将卷积和改写为 $y[n] = \sum_{k=0}^{(N/2)-1} h[k] (x[n-k] + x[n-N+1+k])$（当 $N$ 为偶数时）。这种结构大约只需要原来一半数量的乘法器，显著提高了计算效率。

## 4.滤波器性能分析

### 4.1 系数量化效应

在实际的数字系统中，滤波器系数必须以有限字长（如16位定点数）存储。系数量化会改变零点 $z_q$ 和极点 $p_q$ 的位置。

对于IIR滤波器，极点的位置对反馈系数 $a_k$ 的量化非常敏感，尤其是当极点靠近单位圆或滤波器阶数较高时。极点的微小移动可能导致其跑到单位圆外，从而造成系统不稳定。此外，量化也会改变滤波器的频率响应特性。

对于FIR滤波器，由于没有极点，系数量化不会导致不稳定，但会使幅度响应和相位响应偏离设计值，可能破坏严格的线性相位条件（如果系数不再精确对称）。

### 4.2 舍入噪声分析

在定点运算中，乘法结果必须舍入或截断到指定位宽，这引入了非线性误差。为了分析，通常将每次舍入操作建模为一个加性白噪声源 $e[n]$，其均值为0，方差为 $\sigma_e^2 = \Delta^2/12$，其中 $\Delta = 2^{-B}$ 是量化步长，$B$ 是小数部分的位数。每个噪声源通过其后的滤波器部分传播到输出端。输出噪声的总方差等于所有独立噪声源方差乘以各自噪声传递函数 $G_i(z)$ 的平方 $l_2$ 范数（$\frac{1}{2\pi} \int_{-\pi}^{\pi} |G_i(e^{j\omega})|^2 d\omega$）后的和。

为了防止信号在级联的滤波器节点处因累加而溢出，需要在关键节点处引入缩放因子 $s_i$。常用的缩放准则有：

$L_1$ 范数缩放：$s_i = 1 / \sum_{n} |g_i[n]|$，保证节点信号绝对值有界。

$L_2$ 范数缩放：$s_i = 1 / \sqrt{\sum_{n} |g_i[n]|^2}$。

$L_\infty$ 范数缩放：$s_i = 1 / \max_{\omega} |G_i(e^{j\omega})|$。

### 4.3 IIR滤波器稳定性判断

理论上的稳定性判据是：因果IIR滤波器的所有极点必须位于Z平面的单位圆内，即 $|p_k| < 1$。在系数量化后，必须检验量化后的极点是否仍然满足此条件。

除了直接计算多项式 $A(z) = 1 - \sum_{k=1}^{N} a_k z^{-k}$ 的根之外，还可以使用 **朱里（Jury）稳定性判据** 或 **舒尔-科恩（Schur-Cohn）判据**。朱里判据通过构造一个系数表格，检查表格首列元素是否全为正，从而判断所有根是否在单位圆内，而无需显式求根。

在实践中，使用 **二阶节（Biquad）的级联或并联型** 是实现高阶IIR滤波器的稳健选择，因为每个二阶节的极点对系数量化的敏感度远低于直接型的高阶多项式。此外，需要警惕由有限字长效应引起的 **极限环振荡**，即输入为零或为常数时，输出仍存在小幅振荡，这包括由舍入非线性引起的 **粒度极限环** 和由溢出非线性引起的 **溢出极限环**。

# 滤波器软件设计

## 1.Matlab



## 2.FilterPro