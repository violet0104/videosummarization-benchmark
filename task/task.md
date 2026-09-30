# 进度汇总

## 2026

### 9 月

------

#### 9.17

**Todo**

- 找 movie + 简述 / 视频 + 简述
- 长视频怎么抽帧，找摘要
- 找视频任务

------

#### 9.23

**Todo**

- 看 streamo 论文
- 用现有的数据集跑 streamo 方法
- 看电影，评估解说视频质量
- 开题报告：
    - 课题意义，现有研究（视频摘要 Video Summarization、流式视频 Video Streaming），国内外研究，不足之处
    - 调研 benchmark，方法（架构图）
    - 复现结果（体现自己做的工作），实验结果对比，参考文献

**Notes**

- 电影、美剧、动漫等解说视频

    - [Movies in Minutes](https://www.youtube.com/@MoviesinMinutes)

    - [Man of Recaps](https://www.youtube.com/@ManofRecaps)

- streamo 论文（流式视频） [Streaming Video Instruction Tuning](https://openaccess.thecvf.com/content/CVPR2026/papers/Xia_Streaming_Video_Instruction_Tuning_CVPR_2026_paper.pdf)

![image-20260924150222216](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260924150222216.png)

streamo 方法

- Slience：表示当前帧和用户提问无关，模型保持沉默，持续处理后续帧
- Standby：表示模型检测到相关视频画面，但信息尚不完整，继续收集视觉信息，等待完整事件信息
- Response：表示已经获取了足够的信息，模型输出回答



将上述方法用于生成 caption（决定什么时候输出 caption）

- Slience：表示当前输入没有产生值得描述的新语义信息，暂时不输出caption，继续读取后续帧
- Standby：已检测到一个新的事件/动作/场景变化，但事件仍在发展，信息不足以形成完整 caption，继续积累上下文
- Response：当前事件或语义变化已经足够完整，生成对应 caption

例子：比如一个视频：

​	**t₁：** 一个人站在泳池边
 		--> `<Silence>`，没有新的事件。

​	**t₂：** 他开始弯腰准备跳水
​		 --> `<Standby>`，已经检测到新动作，但还不知道最后做什么。

​	**t₃：** 他跳入水中
 		--> `<Response> A man jumps into the swimming pool.`



生成 caption：利用 LLM ，输入特定的 prompt，使模型输出增量的 caption，而不是全量的（代替之前说的使用 attention）

- prompt 示例：根据当前视频画面和历史描述，只生成相对于历史描述新增的视觉信息，不要重复历史中已经描述且当前仍然保持不变的内容。
    - 需要描述：
        1. 新出现的人物、物体或场景；
        2. 已有人物或物体的新动作；
        3. 状态发生的变化；
        4. 新产生的交互关系或事件。
    - 不需要描述：
        1. 历史中已经出现且没有发生变化的信息；
        2. 同一动作或状态的持续；
        3. 仅仅因为当前画面仍能看到某个物体而重复描述它。



------

