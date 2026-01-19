<div align="center"><h1>Dual-OutputLDO</h1></div>

LM27762 是一款低噪声正负输出集成式电荷泵与 LDO 芯片，能够从单路输入（2.7V‑5.5V）同时生成可调节的正电压（1.5V‑5V）和负电压（‑1.5V‑‑5V），输出电流可达 ±250mA。其特点包括采用反相电荷泵后接负 LDO 的结构，开关频率为 2MHz，输出噪声极低（典型值 22μVrms），并具有独立的使能控制和电源正常（PGOOD）指示功能。重要参数包括静态电流仅 390μA（典型值）、关断电流 0.5μA，正/负 LDO 在 100mA 负载下的压降分别为 45mV 和 30mV，适用于音频放大器、运放偏置、数据转换器等需要低噪声正负电源的场景。

MP2236 是一款 18V、6A 高效率同步降压转换器，采用恒定导通时间（COT）控制，提供快速瞬态响应和简易的环路补偿。其输入电压范围宽达 3V‑18V，支持最大 6A 连续输出电流，内部集成低导通电阻的功率 MOSFET（25mΩ/12mΩ）。该器件默认参考电压为 600mV，开关频率为 600kHz，并具备打嗝式过流保护（OCP）和热关断功能。重要参数包括轻载时静态电流 150μA（典型值）、关断电流低于 1μA，以及内部软启动时间约 1ms，主要应用于平板电视、数字电视电源、分布式电源系统等中高功率降压转换场合。

### 硬件设计

<img src="../../Bitmap/Dual_OutputLDO-MP2236模块.png" alt="TPS7A47模块" style="zoom:50%;" />

<div align="center">图1 MP2236模块</div>

MP2236是一款同步降压（Step-Down）转换器，其核心任务是将较高的输入电压（如12V）高效、稳定地转换为一个更低的、可精确设定的中间电压（VCC）。这个电压的设定完全由一个连接在输出端与反馈（FB）引脚之间的外部电阻分压网络决定。计算遵循公式 **Vout = 0.6V × (1 + R1/R2)**，其中0.6V是芯片内部的精密基准电压。通过改变R1与R2的阻值比例，即可在0.6V至输入电压的范围内线性调节输出电压。MP2236采用恒定导通时间（COT）控制模式，能根据输入、输出电压实时调整开关频率，在宽输入范围内保持效率与快速瞬态响应。其输出的VCC电压的精度和稳定性，直接决定了后续电路供电平台的质量。

<img src="../../Bitmap/Dual_OutputLDO-LM27762模块.png" alt="TPS7A47模块" style="zoom:50%;" />

<div align="center">图2 LM27762模块</div>

LM27762则是一个集成了电荷泵和低压差线性稳压器（LDO）的独特芯片，它能从一个单路正输入（即MP2236提供的VCC）同时产生一组相互独立、低噪声的正负输出电压（如+3.3V和-3.3V）。其每路输出都拥有独立的反馈控制环路：正输出由基准电压1.2V和电阻R1、R2设定（公式：**Vout+ = 1.2V × (R1+R2)/R2**），负输出则由基准电压-1.22V和电阻R3、R4设定（公式：**Vout- = -1.22V × (R3+R4)/R4**）。一个关键的设计约束是，为了保障LDO环路的稳定，连接到地的反馈电阻R2和R4必须不小于50kΩ。这种设计允许工程师灵活配置不对称的双电源（如+5V/-3V），但为了获得最佳性能，正负输出的电阻需分别计算以确保精度。



<div style="display: flex; justify-content: space-between; margin: 20px 0;">
  <img src="../../Bitmap/Dual_OutputLDO_PCB顶层.png" alt="QuietLDO_PCB顶层" style="width: 48%; border: 1px solid #ddd; border-radius: 5px;">
  <img src="../../Bitmap/Dual_OutputLDO_PCB底层.png" alt="QuietLDO_PCBd底层" style="width: 48%; border: 1px solid #ddd; border-radius: 5px;">
</div>
<div align="center">图3 Dual-OutputLDO PCB设计</div>

<div style="background-color:#f8f9fa;padding:40px;text-align:center;margin-top:30px;border-radius:10px;"><div style="color:#666;margin-bottom:20px;font-size:18px;">PCB尺寸示意图</div><div style="position:relative;display:inline-block;padding:80px 120px;"><div style="width:300px;height:180px;background-color:#e8f0fe;border:3px solid #2c5aa0;clip-path:path('M15,0L285,0L300,15L300,165L285,180L15,180L0,165L0,15L15,0Z M0,15A15,15 0 0 0 15,0L0,15Z M300,15L285,0A15,15 0 0 0 300,15Z M285,180L300,165A15,15 0 0 0 285,180Z M0,165L15,180A15,15 0 0 0 0,165Z')"><div style="color:#2c5aa0;font-weight:bold;font-size:32px;position:absolute;top:50%;left:50%;transform:translate(5%,100%);">25 × 45 mm</div></div></div><div style="color:#666;margin-top:20px;font-size:16px;">长×宽 (单位: mm)，四角2mm半径内凹缺角</div></div>

  <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">
    <div style="flex: 1; min-width: 200px;">
      <div style="color: #666; margin-bottom: 5px;">安装孔半径</div>
      <div style="font-size: 18px; font-weight: bold; color: #333;">2 mm</div>
    </div>
    <div style="flex: 1; min-width: 200px;">
      <div style="color: #666; margin-bottom: 5px;">安装孔数量</div>
      <div style="font-size: 18px; font-weight: bold; color: #333;">4个</div>
    </div>
    <div style="flex: 1; min-width: 200px;">
      <div style="color: #666; margin-bottom: 5px;">板厚</div>
      <div style="font-size: 18px; font-weight: bold; color: #333;">1.6 mm</div>
    </div>
    <div style="flex: 1; min-width: 200px;">
      <div style="color: #666; margin-bottom: 5px;">安装孔位置</div>
      <div style="font-size: 18px; font-weight: bold; color: #333;">四角对称</div>
    </div>
</div>


### 使用注意

- 在焊接过程中需注意反馈电阻的选择,原理图上为标注电阻大小的作为反馈电阻,具体取值参考附录
- 在使用前尽可能先估算电压电流大小,该电路板不适合通过大电流
- 用户需要采用4个铜柱+螺母将PCB固定
- 由于可以同时输出正负电压,所以在使用过程中注意散热

### 附录:建议匹配电阻

| 目标输出 (LM27762) | 推荐VCC (MP2236) | MP2236 电阻配置 (产生VCC)         | LM27762 正输出电阻配置            | LM27762 负输出电阻配置            | 计算实际电压                                 |
| :----------------- | :--------------- | :-------------------------------- | :-------------------------------- | :-------------------------------- | :------------------------------------------- |
| **±3.3V**          | **4.0V**         | **R1**: 267kΩ </br>**R2**: 47.5kΩ | **R1**: 174kΩ </br>**R2**: 100kΩ  | **R3**: 169kΩ </br>**R4**: 100kΩ  | VCC≈3.99V </br>VOUT+≈3.30V </br>VOUT-≈-3.29V |
| **±1.8V**          | **2.5V**         | **R1**: 158kΩ </br>**R2**: 49.9kΩ | **R1**: 51.1kΩ </br>**R2**: 100kΩ | **R3**: 47.5kΩ </br>**R4**: 100kΩ | VCC≈2.50V </br>VOUT+≈1.81V </br>VOUT-≈-1.80V |
| **±2.5V**          | **3.3V**         | **R1**: 287kΩ </br>**R2**: 63.4kΩ | **R1**: 127kΩ </br>**R2**: 100kΩ  | **R3**: 124kΩ </br>**R4**: 100kΩ  | VCC≈3.30V </br>VOUT+≈2.51V </br>VOUT-≈-2.50V |
