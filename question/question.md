# 问题汇总

#### 1. kts代码分割出来的片段有2000多个，但是官方给出的只有71个

![image-20260907103706025](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260907103706025.png)



#### 2. 如何处理输入视频？

~~目前对原视频进行kts分割需要几十分钟。~~




#### 3. MLLM的输入是什么？

~~KTS片段，先对每个片段生成caption并打分~~



#### 4. 怎么画架构图

> v1.0
>
> 不足：不是对每帧生成 caption，而是当当前帧的特征和历史特征存在显著差异时，才输出当前帧的 caption 作为一个片段的 caption？？

![image-20260923112244058](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260923112244058.png)



**想法：**对每一帧，提取当前特征，然后与前面一部分历史特征比较。

- 如果相似则跳过；
- 如果有显著差异，则输出当前帧与历史特征的差异对应的 caption，并将历史特征清空，把当前帧的特征作为后续的历史特征，按照这样依次顺序处理后续采样帧  

有点像 change points，按片段分割。多了一个只用差异生成 caption

> v1.1
>
> ChatGPT 生成

![framework](C:\Users\31708\Desktop\framework.png)



> streamo 生成 caption

![image-20260923170656313](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260923170656313.png)
