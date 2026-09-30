# Video-Summarization 相关 Benchmark 调研

```
ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of default=noprint_wrappers=1:nokey=1 ".\main_video.mkv"
```



| 编号 | benchmark                 | 接收时间                        | 摘要任务                                 | 视频信息                                                     | 输入输出                                             |
| ---- | ------------------------- | ------------------------------- | ---------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| A1   | WikiHow Summaries         | ECCV 2022                       | 教学步骤视频摘要                         | 评测集平均约 73.4 秒                                         | V -- > 二值摘要                                      |
| A2   | BLiSS                     | CVPR 2023                       | 关键帧与文本联合摘要                     | 每个评测片段 5 分钟；源直播通常数小时                        | V + T -- >关键帧 + 关键句 / 文本摘要                 |
| A3   | Mr. HiSum                 | NeurIPS 2023                    | 重要性预测、提取式摘要与高光             | 121–300 秒，平均 201.9 秒                                    | V -- > 重要性分数 + 二值视频摘要                     |
| A4   | VideoXum                  | TMM，2023-11-12 接收；2024 卷期 | 视频、文本及视频—文本联合摘要            | 10–755 秒，平均 124.2 秒                                     | V -- > 视频摘要 + 文本摘要；视频摘要为采样帧二值选择 |
| A5   | MMSum                     | CVPR 2024                       | 文本摘要、关键帧与缩略图                 | 1.0–115.4 分钟，平均 14.5 分钟                               | V + T -- >分段关键帧 + 分段文本摘要                  |
| A6   | VISTA                     | ACL 2025                        | 科研报告视频的生成式文本摘要             | 18,599 条，平均 6.76 分钟                                    | V / A / T / OCR -- >文本摘要                         |
| A7   | Instruct-V2Xum            | AAAI 2025                       | 指令驱动的视频、文本及联合摘要           | 40–940 秒，平均 183 秒                                       | V + Instruction -- >视频帧摘要 + 文本摘要            |
| A8   | MLVU                      | CVPR 2025                       | 长视频文本摘要                           | 全 benchmark 约 3 分钟–2 小时；VS 子集统计 NR                | V + Instruction -- >自由文本摘要                     |
| A9   | S-VideoXum && S-NewsVSum  | ACM Multimedia 2025             | Script 指定内容的提取式视频摘要          | S-VideoXum：11,908 条，最长约 12.5 分钟；S-NewsVSum：45 条，时长未报告 | V + Script -- >二值视频摘要 / 帧选择                 |
| A10  | SM-VideoXum && SM-MrHiSum | arXiv 首版 2025-10-07（未接收） | Video + script + transcript 的提取式摘要 | 分别 11,908／29,917 条；源库最长约 12.5／5 分钟              | V + Script + Transcript -- >二值视频摘要 / 片段选择  |
| A11  | MoSu                      | ICLR 2026                       | 三模态重要性预测与提取式摘要             | 主集平均 272.3 秒；附加 50 条平均 70.4 分钟                  | V + A + T -- >重要性分数 + 二值视频摘要              |
| A12  | LVSum                     | arXiv 首版 2026-04-11（未接收） | 长视频的时间戳、片段描述与相关性评分     | 72 条，10–55 分钟，平均 16 分钟                              | V + T -- >摘要时间片段 + 描述 + 相关性分数           |





## A1. WikiHow Summaries

**论文：**[TL;DW? Summarizing Instructional Videos with Task Relevance & Cross-Modal Saliency](https://arxiv.org/abs/2208.06773)

**代码：**[Instructional-Video-Summarization](https://github.com/medhini/Instructional-Video-Summarization)

**接收时间：**ECCV 2022

![image-20260917101524642](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917101524642.png)

**数据集内容：**

- **2,106 条教学视频、20 个类别**。公开资源包括主视频、网页步骤文字及图片/短视频。

**输入：**

- 教学视频

**输出：**

- 逐帧二值摘要标签（每帧  0 1）
- 0 = 该帧不属于 Ground-Truth Summary 
- 1 = 该帧属于 Ground-Truth Summary

**标注方式和内容：**

- 标注方式：抓取主视频及网页上的步骤图片/GIF，用 ResNet50 特征将其定位回主视频；静态图片取匹配帧前后各 2.5 秒，GIF 按其持续时间确定区间。拼接这些片段形成参考摘要，再人工修正过短/过长的结果，并核验参考摘要至少占原视频 30%。
- 标注内容：逐帧二值标签（0/1）；由标签为 1 的帧构成的 Ground-Truth Summary；片段级重要性分数（0–1，由段内帧标签均值计算）、各 visual step 在视频中的帧级定位；

**视频长度和帧率：**

- 总时长 42.94 小时，按 2,106 条计算，平均约 73.4 秒（1.22 分钟）；
- 帧率：24fps，30fps

---



## **A2. BLiSS**

**论文：** [Align and Attend: Multimodal Summarization with Dual Contrastive Losses](https://ieeexplore.ieee.org/abstract/document/10204014)

**代码：** [A2Summ](https://github.com/boheumd/A2Summ)

**接收时间：** CVPR 2023

![image-20260917102013129](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917102013129.png)

**数据集内容：** 

- 从 Behance 收集 **674 场艺术创作直播**，切分为 **13,303 个视频—文本样本**，包含视频、对应英文 transcript 和摘要标注，**视频总时长约 1,109 小时**。

- 官方提供[预处理数据的 Google Drive 链接](https://drive.google.com/drive/folders/1rqXEIelRzq4mb7NaBk3GXxh7jlfP_Snm?usp=share_link)，仓库说明包含 `annotation` 与 `feature`。
- 原始视频的公开 URL 需按仓库说明邮件联系 `bohe@umd.edu` 获取。

**输入：** 

- 视频画面和带句子时间戳的英文 transcript；官方模型读取 CLIP 帧特征与 RoBERTa 句子特征。

**输出：** 

- **关键帧与关键句的二值选择标签**：0 = 未选中，1 = 属于参考视觉/抽取式文本摘要。
- 选中的关键帧集合、抽取式文本摘要；另提供人工改写的概括性文本摘要，供生成式摘要任务使用。

**标注方式和内容：**

- **标注方式：** 每个视频被划分为5分钟长的片段用于人工标注。标注者观看片段并阅读 transcript，选出约 5～10 个关键词；包含关键词的句子作为关键句，并撰写整段摘要。对于每个视频，从网站上获取其缩略图动画，并从每个剪辑中选择与缩略图最相似的帧作为真值关键帧。
- **标注内容：** 关键帧/关键句标签、关键词、人工改写摘要和句子—帧时间对应信息。视觉参考来自缩略动画匹配，并非人工逐帧连续重要性评分。

**视频长度和帧率：**

- 原始直播通常数小时；**每个 benchmark 样本为约 5 分钟，总时长约 1,109 小时**。
- 原视频统一 FPS、特征提取固定采样 FPS：**未明确报告**。

---



## **A3. Mr. HiSum**

论文：[Mr. HiSum: A Large-scale Dataset for Video Highlight Detection and Summarization](https://proceedings.neurips.cc/paper_files/paper/2023/file/7f880e3a325b06e3601af1384a653038-Paper-Datasets_and_Benchmarks.pdf)

代码：[MR.HiSum](https://github.com/MRHiSum/MR.HiSum)

接收时间：NeurIPS 2023

![image-20260917102142097](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917102142097.png)

数据集内容：

- 来自 YouTube-8M 的 **31,892 条视频，覆盖 3,509 个实体类别标签**；一条视频可有多个类别。
- 视频筛选要求至少 50,000 次观看。
- 发布回放热度标注及元数据，配合 YouTube-8M 视觉特征使用。

输入：

- 视频视觉信息；原始方案使用按秒采样的 Inception-v3/PCA 特征。

输出：

- **重要性分数，范围 0～1**，数值越大表示该视频内相对回放热度越高。
- 根据分数和摘要预算选择的视频片段；二值摘要

标注方式和内容：

- **标注方式：** 自动获取 YouTube Most Replayed 曲线，将每条视频的 **100 个等比例时间分箱分数**映射到逐秒视觉特征。
- **标注内容：** 视频元数据。摘要实验以 KTS 划分镜头，再在时长预算下选择片段；**回放热度自动生成summary**。

视频长度和帧率：

- 长度：**121～300 秒，平均 201.9 秒**。
- 帧率：未报告；
- 视觉特征采样为 **1 FPS**。

change_points

gt_summary

gtscore

![image-20260916000206757](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260916000206757.png)

---



## **A4. VideoXum**

论文：[VideoXum: Cross-modal Visual and Textural Summarization of Videos](https://arxiv.org/abs/2303.12060)

代码：[VideoXum](https://github.com/jylins/videoxum)

接收时间：**IEEE TMM，2023-11-12 接收；发表于 2024 年第 26 卷**。

![image-20260917102529897](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917102529897.png)

数据集内容：

- 给了 YouTube 视频 id
- 基于 ActivityNet Captions 的 **14,001 条视频**，训练/验证/测试划分为 **8,000/2,001/4,000**。
- 每条视频有 10 份视觉摘要参考（每条视频有 10 个标注者进行标注），共 **140,010 组视频—文本摘要配对**；文本参考由对应事件描述组成。

输入：

- 视频

输出：

- **10 份采样帧级二值摘要标签 `vsum_onehot`**：0 = 未被该参考摘要选中，1 = 被选中。
- 缩短后的摘要时间区间 `vsum`、文本摘要 `tsum`；联合任务同时输出视觉与文本摘要。

标注方式和内容：

- **标注方式：** 在原有 ActivityNet 事件描述和时间范围上，由人工缩短视频片段；每条视频由 10 位标注者分别给出视觉摘要。文本摘要由原事件描述拼接形成。标注目标约为原时长的 15%，并过滤摘要比例超过 20% 的结果。
- **标注内容：** 视频时长、原事件时间区间、文本参考、10 份缩短后的视觉摘要区间，以及在采样时间轴上展开的二值标签。10 份视觉参考不等于 10 篇独立改写的文本摘要。

视频长度和帧率：

- **10～755 秒，平均 124.2 秒，中位数 121.6 秒**。
- 原视频统一 FPS：未报告；
- 官方发布的 `sampled_frames` 按 **1 FPS** 均匀采样。

```json
{
    'video_id': 'v_QOlSCBRmfWY',
    'duration': 82.73,
    'sampled_frames': 83
    'timestamps': [[0.83, 19.86], [17.37, 60.81], [56.26, 79.42]],
    'tsum': ['A young woman is seen standing in a room and leads into her dancing.',
             'The girl dances around the room while the camera captures her movements.',
             'She continues dancing around the room and ends by laying on the floor.'],
    'vsum': [[[ 7.01, 12.37], ...],
             [[41.05, 45.04], ...],
             [[65.74, 69.28], ...]] (3 x 10 dim)
    'vsum_onehot': [[[0,0,0,...,1,1,...], ...],
                    [[0,0,0,...,1,1,...], ...],
                    [[0,0,0,...,1,1,...], ...],] (10 x 83 dim)
}
```

---



## **A5. MMSum**

论文：[MMSum: A Dataset for Multimodal Summarization and Thumbnail Generation of Videos](https://openaccess.thecvf.com/content/CVPR2024/papers/Qiu_MMSum_A_Dataset_for_Multimodal_Summarization_and_Thumbnail_Generation_of_CVPR_2024_paper.pdf)

代码：[MMSum_model](https://github.com/Jason-Qiu/MMSum_model)；数据集下载链接 404

接收时间：CVPR 2024。

数据集内容：

- **5,100 条 YouTube 视频，17 个大类、170 个子类**，包含 transcript、视频分段、关键帧、文本摘要和视频元数据。
- 同时支持多模态摘要和缩略图生成任务；资源入口见。

输入：

- 视频画面及对应 transcript。

输出：

- **每个视频分段的代表性关键帧及文本摘要**。
- 缩略图任务进一步生成视频封面；摘要任务的主要视觉目标是关键帧选择。

标注方式和内容：

- **标注方式：** 收集创作者提供的分段结构、视觉摘要与文本摘要，再由 5 名专家观看视频，核验分段边界、关键帧和摘要质量，将 6,800 条候选筛选为 5,100 条。
- **标注内容：** 分段时间边界、分段关键帧、分段文本摘要及元数据。5 名审核者不代表每条视频拥有 5 份独立参考摘要，也不应将关键帧标注写成逐帧连续重要性评分。

视频长度和帧率：

- **1.0～115.4 分钟，平均 14.5 分钟，总时长 1,229.9 小时**。
- 原视频统一 FPS：未报告；未核实到适用于全量数据的固定采样 FPS。

来自 README

```json
{
  "info": {
    "video_id": "ANIAMP0000",
    "youtube_id": "XI8GPsf6TAc",
    "url": "https://youtube.com/watch?v=XI8GPsf6TAc",
    "author": "Happy Learning English",
    "title": "Amphibians | Educational Video for Kids",
    "num_of_segments": 3,
    "duration": "00:04:30",
    "category": "animals",
    "sub_category": "amphibians"
  },
  "summary": [
    {
      "segment": 0,
      "start_time": "00:00:24",
      "summary": "THE ANPHIBIANS",
      "end_time": "00:01:25",
      "length": "00:01:01"
    },
    {
      "segment": 1,
      "start_time": "00:01:26",
      "summary": "OVIPAROUS",
      "end_time": "00:02:47",
      "length": "00:01:21"
    },
    {
      "segment": 2,
      "start_time": "00:02:48",
      "summary": "CARNIVORES",
      "end_time": "03:00:00",
      "length": "00:01:42"
    }
  ],
  "transcript": [
    {
      "index": 0,
      "start_time": "00:00:06",
      "end_time": "00:00:12",
      "length": "00:00:06",
      "summary": "Hello everybody! Today we\u2019re going to look\nat a truly amazing group of vertebrates..."
    },
```

---



## **A6. VISTA**

论文：[What Is That Talk About? A Video-to-Text Summarization Dataset for Scientific Presentations](https://aclanthology.org/2025.acl-long.310/)

代码：[VISTA](https://github.com/dongqi-me/VISTA)

接收时间：**ACL 2025 主会长文**

![image-20260917110316920](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917110316920.png)

数据集内容：

- **18,599 组 AI 会议报告视频—论文摘要配对**，来自 ACL 系列、ICML、NeurIPS 等会议。
- 训练／验证／测试为 **14,881／1,859／1,859**。

输入：

- 学术报告视频，包含幻灯片画面及演讲音频；
- 论文也测试音频、ASR transcript、OCR 文本等输入设定。

输出：

- 类似科研论文 abstract 的自然语言摘要；不是逐帧评分或片段选择。

标注方式和内容：

- **标注方式：** 配对报告视频与论文作者撰写的 abstract，经过质量检查；不是为每个视频重新人工写一篇摘要。
- **标注内容：** 视频—abstract 对应关系及论文元数据。

视频长度和帧率：

- 长度：平均 **6.76 分钟**，每视频平均 **16.36 个镜头**；
- 帧率：未报告。
- 论文附录 E 将视频模型设置记为 **0.1 FPS、提取 32 帧**；

```json
hugging face 申请访问未通过
```

---



## **A7. Instruct-V2Xum**

论文：[V2Xum-LLM: Cross-Modal Video Summarization with Temporal Prompt Instruction Tuning](https://ojs.aaai.org/index.php/AAAI/article/view/32374)

代码：[V2Xum-LLM](https://github.com/hanghuacs/V2Xum-LLM)

![image-20260917110338900](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917110338900.png)

接收时间：AAAI 2025。

数据集内容：

- 从 InternVid 视频列表中筛选的 **30,000 条 YouTube 视频**，划分为 **25,000/1,000/4,000** 条训练/验证/测试样本。
- 提供视频摘要、文本摘要及相关任务指令，发布于[官方 Hugging Face 数据集](https://huggingface.co/datasets/hhua2/Instruct-V2Xum)。

输入：

- 视频帧、帧位置/时间提示和任务指令。

输出：

- **被选中的视频帧索引/时间位置**，可在相同采样时间轴上转换为二值摘要选择：0 = 未选中，1 = 选中。
- 对应文本摘要；根据指令完成视频摘要、文本摘要或视频—文本联合摘要。

标注方式和内容：

- **标注方式：** 以 1 FPS 抽帧，用 LLaVA 生成逐帧描述，再经 GPT-4V 选择、BERTScore 去重、GPT-4 压缩改写，最后人工筛选。
- **标注内容：** 参考帧选择、文本摘要及任务指令。测试参考也来自模型生成后人工筛选，不能写成全部由人工从零标注。

视频长度和帧率：

- **40～940 秒，平均 183 秒**；参考视频摘要平均约 30 帧，平均压缩比例约 16.39%。
- 原视频统一 FPS：未报告；**标注抽帧为 1 FPS**。论文训练将视频下采样/归一化为 **100 个帧位置**，属于模型输入预算。

```json
{
  "id": "MqTdJwMDZhY",

  "meta": {
    "duration": 63.0,
    "sampled_frames": 63,

    "token": {
      "<f0>": 0.0,
      "<f1>": 5.0,
      "<f2>": 11.0,
      "<f3>": 15.0,
      "<f4>": 20.0,
      "<f5>": 26.0,
      "<f6>": 34.0,
      "<f7>": 37.0,
      "<f8>": 41.0,
      "<f9>": 44.0,
      "<f10>": 49.0,
      "<f11>": 53.0,
      "<f12>": 57.0,
      "<f13>": 59.0
    }
  },

  "conversations": [
    {
      "from": "human",
      "value": "<video>
Please generate BOTH video and text summarization for this video."
    },
    {
      "from": "gpt",
      "value": "
[<f0>]A white and black checkered cube rests on a wooden table.
[<f1>]In the foreground, a hand holds a small, patterned white box, suggesting a gift or item, with the box slightly blurred in the background.
[<f2>]A small white box with a blue button is cradled in a hand.
[<f3>]Another hand grips a small white box, likely a puzzle or toy, set against a wooden table backdrop, a cup nearby.
[<f4>]A person's hand presents a small white box, accompanied by a blue object on the table.
[<f5>]A white cup adorned with dots is securely held.
[<f6>]A dome-shaped object or small ball, white in color, is displayed in a hand above a table.
[<f7>]A Rubik's Cube is expertly held, indicating a moment of challenge or leisure.
[<f8>]A small white box, with a black cord trailing, is positioned on a table, held in view.
[<f9>]A hand showcases a small white cube, possibly another Rubik's cube, hinting at a theme of puzzles.
[<f10>]A small white box featuring a black and white design is carefully held.
[<f11>]The familiar shape of a Rubik's cube appears again in a person's grasp.
[<f12>]A simple scene: a hand and a small white box on a wooden table.
[<f13>]A white cube, marked with black dots, sits alone on the wooden surface, completing the collection of objects and moments captured.
"
    }
  ],

  "vsum_onehot": [
    1, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
    1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 0, 1,
    0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
    0, 0, 0
  ]
}
```

---



## **A8. MLVU**

论文：[MLVU: Benchmarking Multi-task Long Video Understanding](https://openaccess.thecvf.com/content/CVPR2025/papers/Zhou_MLVU_Benchmarking_Multi-task_Long_Video_Understanding_CVPR_2025_paper.pdf)

代码：[MLVU](https://github.com/JUNJIE99/MLVU)

![image-20260917110436840](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917110436840.png)

接收时间：CVPR 2025。

数据集内容：

- 正式论文的完整 MLVU 包含 **1,730 条视频、3,102 个问题**；
- 其中 **VS 子任务使用 257 条叙事丰富的视频**，来源包括电影、电视剧、纪录片、生活记录等。

输入：

- 视频和摘要指令。

输出：

- **自由文本形式的视频摘要**，概括主要内容和关键事件。
- Ground Truth 为人工参考文本，不是逐帧重要性或二值摘要选择标签。

标注方式和内容：

- **标注方式：** 选择叙事丰富的视频，由人工编写覆盖关键内容的摘要。
- **标注内容：** 视频对应的摘要任务指令和参考摘要；官方使用参考答案辅助的模型评审评价摘要。

视频长度和帧率：

- **全 MLVU** 的视频约 **3 分钟～2 小时**，论文整体平均约 **930 秒（15.5 分钟）**。
- 原视频统一 FPS：24fps，25fps；不同评测模型采用不同帧数或采样率，例如 16/32 帧或 GPT-4o 的 0.5 FPS，不存在统一的 benchmark 输入 FPS。

```json
    {
        "video": "217.mp4",
        "duration": 480.0,
        "question": "Please summarize this video, including its main content.",
        "answer": "The video starts with waves lapping against the rocks, creating a spray. Then, a boat appears with two men on board, one with a hat and the other without. The man without a hat holds a camera, seemingly focusing on two whales. The hatless man changes into a diving suit and dives underwater for a closer shot of the whales. The video then uses animation techniques to help us understand more about the whales. The video switches between the characters and the whales, but primarily describes the human activity of filming the whales.",
        "question_type": "summary"
    },
```

---



## **A9. S-VideoXum && S-NewsVSum**

论文：[SD-VSum: A Method and Dataset for Script-Driven Video Summarization](https://arxiv.org/abs/2505.03319)

代码：[SD-VSum](https://github.com/IDT-ITI/SD-VSum)

![image-20260917110541815](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917110541815.png)

接收时间：**ACM Multimedia 2025**。两套数据来自同一篇论文；SD-VSum 是方法名。

**数据集内容：**

- **S-VideoXum：** 从原 VideoXum 中仍可获取的视频构建，包含 **11,908 条视频**。每条保留 **10 份人工视觉摘要参考**，并为每份参考生成一个对应的自然语言 script，共 **119,080 组视频—参考视觉摘要（人工选取的摘要帧/片段）—script 配对**；
- **S-NewsVSum：** 包含 **45 条新闻播报视频**，每条配套 **1 份专业编辑制作的视觉摘要**及人工撰写的 script。原始视频和 script 原文属于媒体公司的专有素材，公开发布的是预提取特征、参考选择标签与划分文件。

![image-20260916162936568](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260916162936568.png)

**输入：**

- 与视觉摘要对应的文本摘要（script），这里是先人工选取视觉摘要，再用 LLaVA 生成文本摘要 script。
- 再输入整个视频 + script ，给摘要模型，让它预测与该参考文本摘要对应的帧选择。

**输出：**

- 与输入 script 相符的帧／片段选择，组成**提取式视频摘要**；模型先预测帧重要性，再执行长度约束下的选择。
- S-VideoXum 的参考 `gtsummaries` 按官方格式为 **`[10, n_frames]`**：每行对应一个 script 的视觉参考，0 = 不选中，1 = 选中。
- S-NewsVSum 每条视频只有一份参考。本轮实读发布的 H5，`gtsummaries` 实际为 **`[n_frames]` 的布尔数组**，`False/True` 分别表示不选／选入摘要；**README 写成 `[1, n_frames]`，与当前文件不一致**。
- 论文在 S-VideoXum 上选择得分最高的 **15% 采样帧**，将每个 script 生成的摘要与对应参考计算 F-score，再对同一视频的 10 个 script 及测试视频取平均。

**标注方式和内容：**

- **S-VideoXum：** 视觉选择标签沿用 VideoXum 的人工摘要；以 **1 FPS** 读取每份参考摘要，用 **LLaVA-NeXT-Video-7B** 生成自然语言 script。

**视频长度和帧率：**

- **S-VideoXum：** 论文报告最长约 **12.5 分钟**。特征抽帧为 **1 FPS**。
- **S-NewsVSum：** 论文未明确报告原视频时长分布及统一 FPS；

S-VideoXum：

![image-20260916155250582](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260916155250582.png)

Text Annotations：Dense Captions + Scripts

![image-20260916161900619](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260916161900619.png)



---



## **A10. SM-VideoXum && **SM-MrHiSum

论文：[SD-MVSum: Script-Driven Multimodal Video Summarization Method and Datasets](https://arxiv.org/abs/2510.05652)

代码与数据说明：[SD-MVSum](https://github.com/IDT-ITI/SD-MVSum)

接收时间：**尚未核实正式接收**。arXiv 首版为 **2025-10-07**，v2 修订于 **2026-05-07**；截至本次核实，论文页和仓库仍标为 **under review**。

![image-20260917111626683](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917111626683.png)

**数据集内容：**

SD-MVSum 是方法名称，配套发布 **SM-VideoXum** 和 **SM-MrHiSum** 两个扩展数据集，分别统计与评测。

- **SM-VideoXum：** 在 VideoXum／此前 S-VideoXum 基础上扩展，包含 **11,908 条视频**。每条视频保留 **10 份人工视觉摘要参考**，并为每份参考生成一个 script，共 **10 份 script**；对有语音的视频，另提供全片的带时间戳 transcript。
- **SM-MrHiSum：** 在 MrHiSum 基础上扩展，包含 **29,917 条视频**。每条视频提供 **1 份视觉摘要参考和 1 份 script**；对有语音的视频，另提供带时间戳 transcript。视觉参考由 **Most Replayed 重播热度分数结合时间分段和 Knapsack 算法**构造。

实际读取两份官方划分文件，训练／验证／测试分别为：

| 数据集      |   训练 |  验证 |  测试 |
| :---------- | -----: | ----: | ----: |
| SM-VideoXum |  6,782 | 1,707 | 3,419 |
| SM-MrHiSum  | 26,178 | 1,875 | 1,864 |

**输入：**

- 视频、**指定期望摘要内容的 script**、带时间戳的 transcript；实现使用对应的 CLIP 特征。
- script 描述“摘要想保留什么”，transcript 转录“视频中说了什么”。数据集中的 script 由模型根据已有参考摘要生成；有语音时，同一视频的不同 script 共用该视频的 transcript。

**输出：**

- 与输入 script 对应的帧／片段选择，组成**提取式视频摘要**。
- 官方评测中，**SM-VideoXum** 选择得分最高的 **15% 帧**；**SM-MrHiSum** 结合时间分段与 Knapsack 算法选择片段，总时长不超过原视频的 **15%**。

**标注方式和内容：**

- **视觉参考：** SM-VideoXum 沿用每视频 **10 组人工二值帧选择**；SM-MrHiSum 沿用重播热度重要性分数，并据此构造每视频 **1 组二值摘要选择**。两者的参考来源不同。
- **script：** 当前版本使用 **Qwen3-VL-8B-Instruct** 描述每份参考摘要的视觉内容，生成对应脚本。
- **transcript：** 使用 **Silero VAD** 检测语音区间、**Whisper Turbo** 生成带时间戳转录；非英语转录使用 **NLLB-200** 翻译为英语。
- **无语音情况：** SM-VideoXum 有 **3,893 条（32.7%）**无语音视频；SM-MrHiSum 有 **5,638 条（18.8%）**。这些视频使用零值转录特征，不能写成全部视频均有有效 transcript。
- **公开标注与特征：** 包括视觉选择标签、对应 script、转录及其时间区间，以及视觉、脚本和转录特征。

**视频长度和帧率：**

- **SM-VideoXum：** 沿用 VideoXum 系列视频。论文对 VideoXum 源库报告最长约 **12.5 分钟**、平均约 **2 分钟**；扩展子集的实际时长分布尚未重新统计。
- **SM-MrHiSum：** 沿用 MrHiSum 视频。论文对 MrHiSum 源库报告最长约 **5 分钟**、平均约 **3.3 分钟**；扩展子集的实际时长分布尚未重新统计。
- **原始视频统一 FPS：** 未报告。
- **视觉特征采样：** 两个数据集均使用 **1 FPS**，即每秒采一帧并提取 CLIP 特征。

**SM-MrHiSum**

![image-20260915233144876](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260915233144876.png)

**SM-VideoXum**

![image-20260915233228834](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260915233228834.png)

![image-20260915233249723](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260915233249723.png)

---



## **A11. MoSu**

论文：[TripleSumm: Adaptive Triple-Modality Fusion for Video Summarization](https://arxiv.org/abs/2603.01169)

代码：[TripleSumm](https://github.com/smkim37/TripleSumm)

接收时间：[ICLR 2026](https://iclr.cc/virtual/2026/poster/10006671)。

![image-20260917111652047](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917111652047.png)

数据集内容：

- **52,678 条视频，约 4,000 小时**，从 YouTube-8M 筛选，涵盖游戏、乐器、烹饪、动物等内容。
- 官方数据卡列训练／验证／测试为 **42,152／5,263／5,263**。

输入：

- 视频画面、音频和带时间戳的 transcript
- 官方方法使用时间对齐的 CLIP、AST 和 RoBERTa 特征。

输出：

- **范围 0～1 的连续重要性分数**
- Ground Truth 包含 `gt_score` 与二值选择 `gt_summary`

标注方式和内容：

- **标注方式：** 收集至少 50,000 次观看的视频，用 YouTube “Most Replayed” 重播热度作为重要性分数；不是人工逐帧打分。原始热度按 100 个均匀区间提供，预处理将前 5 秒的分数置零。
- **标注内容：** 重要性、二值摘要、镜头边界、主题类别。

视频长度和帧率：

- 长度：**120–501 秒，平均 272.25 秒（约 4.54 分钟）**
- 帧率：未报告。视觉抽帧为 **1 FPS**。

![image-20260917112120132](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917112120132.png)

![image-20260917112228850](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917112228850.png)

![image-20260917112526048](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917112526048.png)

---



## **A12. LVSum**

论文：[LVSum: A Benchmark for Timestamp-Aware Long Video Summarization](https://arxiv.org/abs/2604.10024)

代码：[LVSum](https://github.com/apple-aiml-research/ml-lvsum-video-summarization)

接收时间：**2026 年预印本，尚未核实正式会议／期刊接收**。arXiv 首版 **2026-04-11**，所核对修订版为 **2026-07-17**。

![image-20260917112548043](C:\Users\31708\AppData\Roaming\Typora\typora-user-images\image-20260917112548043.png)

数据集内容：

- **72 条长视频、13 类内容**，包括讲座、纪录片、新闻、vlog、播客等；多人工标注，每视频最多 10 份人工参考。

输入：

- 长视频与带时间戳 transcript；论文实验采用均匀抽帧，转录由 Gemini-2.5-Pro 生成，仓库提供生成脚本。

输出：

- 摘要片段的开始／结束时间、片段描述及相关性分数；可据时间区间剪出视频摘要。

标注方式和内容：

- **标注方式：** 人工完整观看并回看视频，选取关键区间，撰写简短描述，打 **1–3 分**，将选中区间总长控制在原视频的 **15%** 内；之后进行质量过滤。
- **标注内容：** 视频与标注者 ID、摘要片段区间、文字描述、片段score。

视频长度和帧率：

- 论文报告 **10–55 分钟，平均 16 分钟**。
- 帧率：25fps，30fps不等
- 论文推理使用 **96 个均匀采样帧**；相关性评测使用 **1 秒粒度**，不是原视频帧率。

```json
    {
        "video_path": "https://ndtvod.pc.cdn.bitgravity.com/23372/ndtv/02102016_i_TopJagannathPackage_442154_241510_320.mp4",
        "video_id": "single_asset_data_00f277a5-f5e2-471d-a8b4-6d051bc0ddc7",
        "annotator_id": "0535d104-44ee-4848-b2f5-900bd755d82f",
        "summary_timestamps": [
            {
                "start_time": 145419,
                "end_time": 154086,
                "start_timestamp": "00:02:25",
                "end_timestamp": "00:02:34",
                "score": 3.0,
                "description": "Environmental issues in Puri - sewage, draining issues leading to health issues to those living in area 3km from holy shrine"
            },
            {
                "start_time": 187348,
                "end_time": 197182,
                "start_timestamp": "00:03:07",
                "end_timestamp": "00:03:17",
                "score": 2.0,
                "description": "Praying places important to keep clean - but same applies to living space as it's as much a temple"
            },
            {
                "start_time": 285692,
                "end_time": 293180,
                "start_timestamp": "00:04:45",
                "end_timestamp": "00:04:53",
                "score": 3.0,
                "description": "Puri environmental issues contain waste management"
            },
            {
                "start_time": 424331,
                "end_time": 432044,
                "start_timestamp": "00:07:04",
                "end_timestamp": "00:07:12",
                "score": 2.0,
                "description": "To be able to honor structures in city, need to keep city clean"
            },
            {
                "start_time": 570829,
                "end_time": 582790,
                "start_timestamp": "00:09:30",
                "end_timestamp": "00:09:42",
                "score": 3.0,
                "description": "Process is in place to improve household and commercial establishments waste management connectivity and enforcement of law"
            }
        ]
    },
```

