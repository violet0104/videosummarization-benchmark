# 2021–2026 Video Summarization 相关 Benchmark 调研

检索截止：**2026-09-11**。范围：**ICLR、NeurIPS、ICCV、ECCV、CVPR、ICML、AAAI、IEEE Transactions on Multimedia（TMM）**。

本轮核实并整理了 **21 项已接收工作**：12 项直接提供摘要数据集或摘要评测子任务，8 项属于高光、预告片、视频再剪辑或摘要理解等邻近任务，另有 1 项自建叙事摘要评测语料。一个论文同时提出训练集与测试集时合并介绍；旧数据集的新增标注与原数据集首次发表分开处理。一般 video QA 不逐项展开，邻近问答资源优先纳入明确设置 Summarization 子任务的工作。

## 阅读口径

- **接收时间**：只有论文或作者明确披露时才写具体接收日期；其余写已核实的接收会议及届次。会议年份、论文集出版时间、arXiv 上传时间不是同一个概念。作者发布“已接收”的日期也不必然等于正式通知日。
- **视频长度**：优先报告该 benchmark 实际输入单元的长度；原始长视频、切分后的样本、输出摘要长度分别标注。混合任务 benchmark 的总体统计不能直接当作摘要子集统计。
- **帧率**：原视频 FPS、模型采样 FPS、固定输入帧数、标注时间粒度分别记录。例如“每 2 秒一个标签”不能推导出视频是 0.5 FPS。
- **NR**：在本次核查的论文、附录或官方说明中未找到明确报告；不表示视频没有帧率或数据不存在。不用常见的 25/30 FPS 补空，也不把某个后续模型的采样配置当成数据集规定。
- **标注**：区分人工创作、创作者已有内容、模型合成后人工审核、自动匹配，以及观看行为代理标签。后两类不能直接称作“多个人工摘要”。
- 本文以原始论文、正式论文集、作者项目页和官方仓库为证据。没有下载完整视频库或逐文件用 ffprobe 测量，原始 FPS 缺失项仍需后续实测。

## 一、直接摘要数据集与摘要评测子任务：12 项

| 编号 | 数据集 / 子任务 | 已核实接收 | 实际摘要任务 | 视频长度概览 |
|---|---|---|---|---|
| A1 | WikiHow Summaries | ECCV 2022 | 教学步骤视频摘要 | 评测集平均约 73.4 秒，按总时长计算 |
| A2 | BLiSS | CVPR 2023 | 关键帧与文本联合摘要 | 每个评测片段 5 分钟；源直播通常数小时 |
| A3 | VideoXum | TMM，2023-11-12 接收；2024 卷期 | 视频、文本及视频—文本联合摘要 | 10–755 秒，平均 124.2 秒 |
| A4 | Mr. HiSum | NeurIPS 2023 Datasets and Benchmarks | 重要性预测、提取式摘要与高光 | 121–300 秒，平均 201.9 秒 |
| A5 | LfVS-P / LfVS-T | CVPR 2024 | 长视频提取式摘要 | 测试集 8–33 分钟，平均 12.2 分钟 |
| A6 | MMSum | CVPR 2024 | 文本摘要、关键帧与缩略图 | 1.0–115.4 分钟，平均 14.5 分钟 |
| A7 | PlotSnap | CVPR 2024 | 剧集镜头与对白摘要 | 平均约 44 分钟 |
| A8 | Instruct-V2Xum | AAAI 2025 | 指令驱动的视频、文本及联合摘要 | 40–940 秒，平均 183 秒 |
| A9 | Shot2Story | ICLR 2025 | 多镜头视频的连贯文本摘要 | 10–40 秒，平均 17.1 秒 |
| A10 | MLVU–Video Summarization | CVPR 2025 | 长视频文本摘要 | 全 benchmark 约 3 分钟–2 小时；VS 子集统计 NR |
| A11 | MoSu；论文附加长视频测试集 | ICLR 2026 | 三模态重要性预测与提取式摘要 | 主集平均 272.3 秒；附加 50 条平均 70.4 分钟 |
| A12 | MedVidBench–Video Summarization | CVPR 2026 | 医疗视频文本摘要 | 全 benchmark 20–1,800 秒；VS 子集统计 NR |

### A1. WikiHow Summaries / Pseudo Summaries

论文：*TL;DW? Summarizing Instructional Videos with Task Relevance & Cross-Modal Saliency*。

- **输入与输出**：输入教学视频；论文方法还使用 ASR transcript 及任务相关信息。输出保留关键教学步骤的视频片段、对应帧/片段重要性。WikiHow 文章及步骤图是构建参考答案的来源，不能默认把这些参考内容提供给测试模型。
- **接收时间**：ECCV 2022；具体接收通知日未核实。
- **规模与标注**：WikiHow Summaries 报告 2,106 条视频、20 类。将文章中的步骤图片或 GIF 自动匹配回原视频，静态图取匹配位置附近的 5 秒窗口，GIF 按其持续时间生成区间，再合并并人工检查，获得二值时间选择与重要性标签。另有 12,160 条 COIN/CrossTask 来源的 **Pseudo Summaries 训练数据**，由 ASR、任务相关性和跨模态显著性自动生成，不能混称为 12,160 条人工测试摘要。
- **视频长度**：WikiHow 评测集总计 42.94 小时，按 2,106 条计算平均约 **73.4 秒**；精确最短/最长值 NR。Pseudo Summaries 平均 **3.09 分钟**。摘要构造要求至少保留 30%；论文推理设置采用 55% 输出比例，不是普遍适用的 15% 协议。
- **帧率**：原始 FPS 未统一报告。训练/伪标签流程使用 **8 FPS**；论文说明推理保留原视频帧率，不能将 8 FPS 写成整个数据集的固定 FPS。
- **一致性提示**：论文写出的验证/测试数量为 768/1,339，相加 2,107，与总数 2,106 差 1；复现实验应以实际发布的样本 ID 清单为准，不能擅自修正其中一个数字。

依据：论文数据构建、实验设置及附录。[ECCV 2022 论文](https://arxiv.org/abs/2208.06773)；[Google Research 接收信息](https://research.google/pubs/tldw-summarizing-instructional-videos-with-task-relevance-cross-modal-saliency/)；[官方代码与数据说明](https://github.com/medhini/Instructional-Video-Summarization)。

### A2. BLiSS（Behance LiveStream Summarization）

论文：*Align and Attend: Multimodal Summarization With Dual Contrastive Losses*。

- **输入与输出**：输入设计/绘画直播视频和带句子时间戳的 transcript，另保留音频与元数据。输出关键帧和关键句；数据还提供人工撰写的概括性文本摘要，支持抽取式与生成式文本摘要评测。
- **接收时间**：CVPR 2023，正式论文集为 2023 年 6 月；具体接收通知日未核实。
- **规模与标注**：674 场直播切成 **13,303 个样本**，总计约 1,109 小时。人工为每个片段选择 transcript 关键句、编写摘要与关键词。视觉参考帧由直播的 thumbnail animation 与片段内帧自动相似度匹配得到，**不是标注者逐帧人工选择的完整视频摘要**。
- **视频长度**：源直播通常数小时；模型评测单元是 **5 分钟片段**。不能把 13,303 个样本都描述成数小时长视频。
- **帧率**：原视频 FPS 为 NR；本次查阅正文、补充材料及官方说明未找到统一固定采样 FPS。论文明确使用 CLIP 帧特征和 RoBERTa 句子特征，特征名称本身不能推导采样率。

依据：正文 §4.2 及补充材料数据标注部分。[CVPR 2023 论文](https://openaccess.thecvf.com/content/CVPR2023/html/He_Align_and_Attend_Multimodal_Summarization_With_Dual_Contrastive_Losses_CVPR_2023_paper.html)；[官方项目](https://boheumd.github.io/A2Summ/)；[官方仓库](https://github.com/boheumd/A2Summ)。

### A3. VideoXum

论文：*VideoXum: Cross-modal Visual and Textural Summarization of Videos*。

- **输入与输出**：输入原视频/采样帧，输出视频关键片段、文本摘要或两者联合输出，分别对应 V2V、V2T、V2VT。ActivityNet Captions 的文字用于参考答案构建，不能因此认定标准输入必须包含 transcript。
- **接收时间**：论文首页明确写 **2023-11-12 accepted**；正式卷期为 **TMM Vol. 26，2024**。不是把 2023 年 arXiv 版本计为 CVPR 论文。
- **规模与标注**：ActivityNet Captions 来源 **14,001 条视频**，训练/验证/测试为 8,000/2,001/4,000。40 名工作人员参与；对视频已有事件描述对应的时间范围进行缩短，每条视频形成 **10 份视频选择标注，共 140,010 份**。文字摘要基于原事件 caption 合并，不能理解成每条视频有 10 篇独立人工重写的文本摘要。标注目标约 15% 视频长度，并过滤超过 20% 的样本。
- **视频长度**：**10–755 秒，平均 124.2 秒，中位数 121.6 秒**；99.9% 少于 300 秒。论文报告平均视频压缩比例 13.6%。
- **帧率**：原始 FPS 为 NR；官方 `sampled_frames` 按 **1 FPS** 均匀采样。这是发布预处理帧的采样率，不是原视频编码帧率。

依据：论文首页、数据构建与统计，README 的 sampled_frames 说明。[TMM 论文](https://arxiv.org/abs/2303.12060)；[官方项目](https://videoxum.github.io/)；[官方仓库](https://github.com/jylins/videoxum)。

### A4. Mr. HiSum

论文：*Mr. HiSum: A Large-scale Dataset for Video Highlight Detection and Summarization*。

- **输入与输出**：原始发布以视频视觉特征为主要输入；输出时间重要性分数、高光片段或提取式视频摘要。摘要实验与高光实验的输出/指标应分别使用。
- **接收时间**：**NeurIPS 2023 Datasets and Benchmarks**；具体接收通知日未核实。
- **规模与标注**：**31,892 条 YouTube-8M 视频，3,509 个实体标签**。用 YouTube **Most Replayed** 曲线的 100 个归一化时间点作为重要性代理，再映射到逐秒视觉特征。视频要求至少 50,000 次观看；这不是“50,000 名摘要标注者”，也不意味着有人工摘要文本。
- **视频长度**：**121–300 秒，平均 201.9 秒**。筛选不超过 300 秒与可用 YouTube-8M 特征长度有关；不能把源平台可播放长度等同于模型实际可用特征范围。
- **帧率**：原始 FPS 为 NR；视觉特征来自 **1 FPS** 的 Inception-v3 表征并做 PCA。100 个回放分数是等比例时间分箱，不能写成 100 FPS 或固定 100 秒。
- **评测含义**：论文提供摘要与高光评测流程，包括重要性排序及摘要选择；但回放热度衡量的偏好与“保留全部重要事件”不是同一个目标。MoSu 作者后续提供的三模态 Mr. HiSum 扩展也不等于本论文最初发布条件。

依据：论文数据构建、特征和评测协议。[NeurIPS 2023 正式论文](https://proceedings.neurips.cc/paper_files/paper/2023/file/7f880e3a325b06e3601af1384a653038-Paper-Datasets_and_Benchmarks.pdf)；[官方仓库](https://github.com/MRHiSum/MR.HiSum)。

### A5. LfVS-P / LfVS-T

论文：*Scaling Up Video Summarization Pretraining with Large Language Models*。

- **输入与输出**：输入长视频以及可获得的 transcript；无语音时论文使用视觉 caption 作为文字信息。输出按时间组织的提取式视频摘要。其核心 gold 是视频摘要，不应直接当作独立标注的视频—文本联合摘要 benchmark。
- **接收时间**：CVPR 2024，正式论文集为 2024 年 6 月；具体接收通知日未核实。
- **规模与标注**：**LfVS-P：250,000 条训练视频**，HowTo100M 来源，Whisper 转录、视觉—语言筛选、LLM 抽取句子及时间区间、再进行视觉定位修正，属于伪摘要预训练数据。**LfVS-T：1,200 条、392 类**，含有解说和无解说视频，参考视频摘要由专业人员人工制作。
- **视频长度**：LfVS-P 筛选至少 8 分钟，平均 **13.3 分钟**；LfVS-T 为 **8–33 分钟，平均 12.2 分钟**。这两组统计不能互换。
- **帧率**：原始 FPS 为 NR；论文视觉处理采用 **1 FPS** 采样。视频摘要与源视频帧匹配用于构造评测重要性，不等于逐秒人工评分。
- **可用性边界**：论文与协议已核实；本次未核实到可直接取得完整 LfVS-T 数据及逐视频多参考人数的发布清单，正式采用前需要继续确认。

依据：正文数据构建、LfVS-T 描述及实验设置。[CVPR 2024 正式论文](https://openaccess.thecvf.com/content/CVPR2024/html/Argaw_Scaling_Up_Video_Summarization_Pretraining_with_Large_Language_Models_CVPR_2024_paper.html)。

### A6. MMSum

论文：*MMSum: A Dataset for Multimodal Summarization and Thumbnail Generation of Videos*。早期名称 **MultiSum** 与本项有关，不重复计为两套新 benchmark。

- **输入与输出**：输入视频及对应 transcript，附有视频/片段元数据。输出片段级文本摘要和代表性关键帧，也覆盖视频缩略图生成任务；关键帧序列不能直接等同于连续可播放的定长视频摘要。
- **接收时间**：CVPR 2024，正式论文集为 2024 年 6 月；具体接收通知日未核实。
- **规模与标注**：**5,100 条视频，17 大类、170 子类，共 1,229.9 小时**。收集已有创作者提供的文本摘要、结构性分段及视觉信息；5 名人工专家观看并核验分段边界、关键帧与文本摘要，将 6,800 条候选筛成 5,100 条。不能把 5 名审核者解释成每条视频有 5 篇独立参考摘要。
- **视频长度**：正式论文 Table 2 报告 **1.0–115.4 分钟，平均 14.5 分钟**。收集条件中出现的 1–120 分钟不是最终实测范围。
- **帧率**：原始 FPS 为 NR；本次核查未找到一个对全部数据统一适用的固定采样 FPS。论文按帧/句子序列定义输入，不能据此自行填 1 FPS。

依据：正文 §3–4、Table 2。[CVPR 2024 正式论文](https://openaccess.thecvf.com/content/CVPR2024/html/Qiu_MMSum_A_Dataset_for_Multimodal_Summarization_and_Thumbnail_Generation_of_CVPR_2024_paper.html)；[官方项目与数据工具](https://mmsum-dataset.github.io/)。

### A7. PlotSnap

论文：*“Previously on …” From Recaps to Story Summarization*。

- **输入与输出**：输入整集电视剧视频和带时间戳的对白字幕；输出重要镜头及对白选择，形成故事摘要。论文的文本侧主要是对白抽取，不应称作全新撰写的剧情摘要段落。
- **接收时间**：CVPR 2024，正式论文集为 2024 年 6 月；具体接收通知日未核实。
- **规模与标注**：**205 集**，其中《24》172 集、《Prison Break》33 集。利用下一集开头专业制作的 recap：人工分离 recap，再自动匹配回上一集中的镜头与对白，剔除不属于对应上一集的内容，产生重要性标签。另取 17 集做额外人工/剧情资料参考验证；不能把这项验证扩大成全部 205 集均有独立多人摘要。
- **视频长度**：《24》平均 **2,635±72 秒**，《Prison Break》平均 **2,615±39 秒**，约 43.9/43.6 分钟。参考 recap 分别平均 104±28 秒和 62±20 秒。源剧集长度与 recap 长度必须分开。
- **帧率**：原始 FPS 为 NR；附录特征提取使用 **8 FPS**。字幕按自身时间戳与镜头对齐，不是每帧一条文字。
- **标注偏好**：recap 服务于后续剧情理解，可能突出即将再次出现的线索；它与对本集全部重要事件的无偏覆盖存在任务差异。

依据：数据集统计、recap 匹配流程及附录特征提取。[CVPR 2024 正式论文](https://openaccess.thecvf.com/content/CVPR2024/html/Singh_Previously_on_..._From_Recaps_to_Story_Summarization_CVPR_2024_paper.html)；[含附录的作者版本](https://arxiv.org/abs/2405.11487)；[官方仓库](https://github.com/katha-ai/RecapStorySumm-CVPR2024)。

### A8. Instruct-V2Xum

论文：*V2Xum-LLM: Cross-Modal Video Summarization with Temporal Prompt Instruction Tuning*。

- **输入与输出**：输入视频帧、时间提示和任务指令；输出选中帧的索引/时间提示、文本摘要或两者联合输出。ASR 并非这个数据构建流程的必需输入。
- **接收时间**：AAAI 2025；官方文章页 2025-04-11 的出版日期不作为接收通知日。
- **规模与标注**：InternVid 提供的视频列表中筛出 **30,000 条**，划分 **25,000/1,000/4,000**。LLaVA 生成逐帧 caption，GPT-4V 做抽取，BERTScore 去重，GPT-4 压缩改写，再经人工筛选。它有独立测试集，但测试参考仍是“模型生成＋人工过滤”，不是全部人工从零编写。
- **视频长度**：**40–940 秒，平均 183 秒**；参考视频摘要平均 30 帧、文本平均 239 tokens，平均视频压缩比例 16.39%。
- **帧率**：原始 FPS 为 NR；**标注过程 1 FPS**。论文训练实现将视频下采样/归一化到 **100 个帧位置**；因此“标注 1 FPS”不能直接写成“模型始终看到全部 1 FPS 帧”。

依据：数据章节、测试集表格和 Implementation Details；详细统计参照作者后续完整版本。[AAAI 2025 正式文章](https://ojs.aaai.org/index.php/AAAI/article/view/32374)；[作者论文版本](https://arxiv.org/abs/2404.12353)；[官方项目](https://hanghuacs.github.io/v2xum/)。

### A9. Shot2Story

论文：*Shot2Story: A New Benchmark for Comprehensive Understanding of Multi-shot Videos*。

- **输入与输出**：输入含多个镜头的视频，可加入 ASR；摘要任务输出跨镜头连贯的文本段落。该数据还支持单镜头 caption 和问答，不应把这些任务数全部算成摘要数。
- **接收时间**：ICLR 2025；早期预印本和仓库中可见 Shot2Story20K，但正式论文对应规模已变化。
- **规模与标注**：正式论文为 **42,958 条**，训练/验证/测试为 **36,951/1,982/4,025**。视觉 caption 先由模型生成后人工纠正；叙述/语音 caption 由人工书写；GPT-4 将多镜头信息整合成摘要，再经人工修改，强调实体一致与事件衔接。另有 90K 自动扩展训练摘要，不能与人工审核主集混计。
- **视频长度**：HD-VILA-100M 来源片段，**10–40 秒，平均 17.1 秒**；每条 2–8 个镜头，平均 4.4 个。长篇文字摘要不意味着输入是长视频。
- **帧率**：原始 FPS 为 NR。论文 holistic baseline **整条均匀取 16 帧**；shot baseline **每个镜头取 4 帧**。二者是帧数预算而非固定 FPS，帧数随镜头数变化时需要单独计成本。

依据：ICLR 正式论文数据统计和 §3.3。[ICLR 2025 论文](https://proceedings.iclr.cc/paper_files/paper/2025/hash/672d794a6052b6beab0e2e002204d974-Abstract-Conference.html)；[官方仓库](https://github.com/bytedance/Shot2Story)。

### A10. MLVU–Video Summarization（VS）

论文：*MLVU: Benchmarking Multi-task Long Video Understanding*。

- **输入与输出**：视频与摘要指令作为输入，输出自由文本概括。VS 是综合长视频理解 benchmark 中的生成式子任务；不能用选择题的 M-Avg 直接代表摘要质量。
- **接收时间**：**CVPR 2025**；官方仓库于 **2025-02-27 公告已接收**。2024 年预印本/数据发布不能写成“NeurIPS 2024 正式接收”。
- **规模与标注**：正式论文全 benchmark 为 **1,730 条视频、3,102 个问题**；VS 对 **257 条叙事丰富的视频**人工编写关键事件摘要，来源包括电影、电视剧、纪录片、生活视频等。采用参考答案辅助的模型评审；总问题数不等于摘要参考数。
- **视频长度**：官方整体介绍为约 **3 分钟–2 小时**；正式论文整体平均约 **930 秒（15.5 分钟）**。VS 子集单独的最短、最长、均值为 NR，不能将整体统计标为“257 条摘要视频均值”。
- **帧率**：原始 FPS 未统一报告；评测按模型使用不同输入预算，例如 16 帧、32 帧或 GPT-4o 的 **0.5 FPS**。这不是一个统一固定帧输入的比较协议。若要证明自适应观察机制有效，需要重新对齐预算。

依据：正式论文任务定义和统计，官方仓库 News 与输入列。[CVPR 2025 正式论文](https://openaccess.thecvf.com/content/CVPR2025/html/Zhou_MLVU_Benchmarking_Multi-task_Long_Video_Understanding_CVPR_2025_paper.html)；[官方数据与评价代码](https://github.com/JUNJIE99/MLVU)。

### A11. MoSu；同论文附加 50 条长视频测试集

论文：*TripleSumm: Adaptive Triple-Modality Fusion for Video Summarization*。

- **输入与输出**：输入视觉、音频与时间对齐的 transcript；输出重要性分数和提取式视频摘要。数据虽然有 transcript，仍不等于有人工生成式文本摘要 gold。
- **接收时间**：**ICLR 2026**；官方会议页面可核实，作者仓库在 2026 年 1 月公告接收。2026 年 3 月 arXiv 上传日期不能反推接收时间。
- **规模与标注**：主集 **52,678 条视频、3,406 类、3,983.7 小时**，按 8:1:1 划分。采用 Most Replayed 的 100 个时间分箱，筛选至少 50,000 次观看；为减轻开头回放偏差，将前 5 秒标签置零。英文转录直接使用，其他语言可经 YouTube 自动翻译。标签仍是回放行为代理，不是专业人工内容覆盖标注。
- **视频长度**：主集 **120–501 秒，平均约 272.3 秒**。附录 B.6 另建 **50 条跨领域长视频**测试集，范围 **2,413–7,207 秒（约 40.2–120.1 分钟）**，平均 **4,224 秒（70.4 分钟）**；同样采用 Most Replayed 标签。不能把 70.4 分钟平均长度赋给 52,678 条主集视频。
- **帧率**：主集视觉 **1 FPS**，视觉/音频/文本按秒对齐，采用 CLIP/RoBERTa/AST 特征；原始 FPS 为 NR。B.6 未单独明确附加长视频集的完整采样参数，不能仅凭主集设置声称附加集原始 FPS 也是 1。

依据：主文数据部分、附录 B 与 Table IV。[ICLR 2026 官方接收页面](https://iclr.cc/virtual/2026/poster/10006671)；[含附录论文](https://arxiv.org/abs/2603.01169)；[官方数据与代码](https://github.com/smkim37/TripleSumm)。

### A12. MedVidBench–Video Summarization（VS）

论文：*MedGRPO: Multi-Task Reinforcement Learning for Heterogeneous Medical Video Understanding*。

- **输入与输出**：输入手术/医疗视频及任务指令；VS 输出操作过程或关键内容的文本摘要。其他任务中的定位框、动作时间段或细粒度 caption 不等于摘要输出。
- **接收时间**：**CVPR 2026**，已在 CVF 正式论文集中核实；具体接收通知日未核实。
- **规模与标注**：从 **8 个医疗数据集、626 条源视频**构建 8 类任务。利用已有专家动作/空间/过程标注，必要时 WhisperX 转录，再用 GPT-4.1、Gemini-2.5-Flash 生成并交叉校验任务数据。全量约 **531,850 条指令对**，不是 531,850 条独立摘要；VS 单独样本数及每视频参考数 NR。按视频划分训练/测试，比例约 85:15。
- **视频长度**：总体处理范围 **20–1,800 秒**；VS 独立范围和均值 NR。
- **帧率**：源数据异构，原始 FPS 未统一报告；论文处理使用自适应 **0.1–3 FPS**、每视频约 50–180 帧，GRPO 阶段报告 **1 FPS**。这些是方法/任务相关配置，不能合并为数据集单一固定 FPS。
- **适用边界**：属于医疗领域的综合理解与摘要评测，生成参考和 LLM judge 不能直接作为人工校准的事实性评估。

依据：数据构建、实验设置及项目说明。[CVPR 2026 正式论文](https://openaccess.thecvf.com/content/CVPR2026/html/Su_MedGRPO_Multi-Task_Reinforcement_Learning_for_Heterogeneous_Medical_Video_Understanding_CVPR_2026_paper.html)；[官方项目](https://uii-america.github.io/MedGRPO/)。

## 二、与摘要紧密相关，但输出目标不同：8 项

| 编号 | 数据集 / 资源 | 已核实接收 | 与完整摘要的区别 |
|---|---|---|---|
| B1 | QVHighlights | NeurIPS 2021 | 查询相关时刻定位与高光评分 |
| B2 | MovieLights | CVPR 2023 | 电影高光，不要求生成完整故事摘要 |
| B3 | TGT 电影—预告片数据及 MAD/MovieNet 扩展 | CVPR 2024 | 可重排镜头的预告片生成 |
| B4 | DocumentaryNet | ICLR 2025 | 吸引观众的纪录片 teaser 生成 |
| B5 | Repurpose-10K | AAAI 2025 | 从长视频中提取多条独立可传播短视频 |
| B6 | VideoAds–Visual Summary | ICCV 2025 | 选择正确概括的选择题，非自由摘要生成 |
| B7 | CineBench | ECCV 2026 | 按指令跨电影/镜头编排视频 |
| B8 | HourVideo–Summarization | NeurIPS 2024 Datasets and Benchmarks | 第一视角长视频的概括类选择题 |

### B1. QVHighlights

论文：*Detecting Moments and Highlights in Videos via Natural Language Queries*，通常称 QVHighlights。

- **输入与输出**：输入视频和自然语言 query；输出一个或多个相关时间区间及 clip saliency 分数。它适合 query-focused 的定位/选择机制，但不原生评价无 query 的完整摘要。
- **接收时间**：NeurIPS 2021；具体通知日未核实。
- **规模与标注**：**10,148 个视频片段、10,310 条查询、18,367 个相关 moments**。众包人员写自由查询并标出相关 2 秒片段；相关片段再由 **3 人做 5 级显著性评分**。不能说所有无关片段也经过同样 5 级人工评分。
- **视频长度**：标准输入为 **150 秒片段**；不是源 YouTube 视频的全部长度。
- **帧率**：源 FPS 为 NR；**2 秒是标签/clip 特征的时间分辨率**，不能写成源视频 0.5 FPS。官方基线组合 SlowFast 与 CLIP 等特征，视觉编码器内部采样需与 clip 时间间隔分开。

依据：[NeurIPS 2021 正式论文](https://proceedings.neurips.cc/paper/2021/hash/62e0973455fd26eb03e91d5741a4a3bb-Abstract.html)；[官方仓库](https://github.com/jayleicn/moment_detr)。

### B2. MovieLights

论文：*Collaborative Noisy Label Cleaner: Learning Scene-Aware Trailers for Multi-Modal Highlight Detection in Movies*。

- **输入与输出**：电影视频与音频特征输入，输出镜头/时段高光标签或分数。预告片用于监督构建，不是标准测试时必须额外输入的答案。
- **接收时间**：CVPR 2023；具体通知日未核实。
- **规模与标注**：**174 部完整电影，训练 144、测试 30**，约 325K 镜头、36K 场景。训练阶段把官方 trailer 匹配到电影镜头，再扩展到场景，自动生成带噪标签。测试阶段 **2 名独立标注者**参照 trailer 相关内容标出高光，取两者交集作为 gold。人工标注受 trailer 内容约束，并非完全自由选择。
- **视频长度**：多数电影 **90–150 分钟**；训练/测试电影平均分别 **2.19/2.14 小时**。高光区间长度为几十秒到数分钟。
- **帧率**：原始 FPS 为 NR；视觉特征取 **每个镜头的中间 1 帧**，没有固定 FPS。音频 16 kHz 是音频采样率，不能写入视频 FPS 栏。

依据：§3、Table 1 和实验特征设置。[CVPR 2023 正式论文](https://openaccess.thecvf.com/content/CVPR2023/papers/Gan_Collaborative_Noisy_Label_Cleaner_Learning_Scene-Aware_Trailers_for_Multi-Modal_Highlight_CVPR_2023_paper.pdf)。

### B3. TGT 电影—预告片训练资源及 MAD/MovieNet 预告片扩展

论文：*Towards Automated Movie Trailer Generation*。

- **输入与输出**：输入完整电影，输出可选取和重排的镜头序列组成 trailer。输出无需保留原片时间顺序，目标也不要求完整覆盖剧情。
- **接收时间**：CVPR 2024；具体通知日未核实。
- **规模与标注**：收集 **23,304 个训练电影—trailer 对及 300 个验证对**。测试使用 **602 部 MAD 电影和 989 部 MovieNet 电影**补充 IMDb trailer；这是旧电影数据的新预告片扩展，不能将 MAD/MovieNet 的原始发表都计为本文新 benchmark。参考来自专业发布的 trailer，以镜头表征匹配形成监督，不是新采集多人内容覆盖摘要。
- **视频长度**：完整电影级输入；本论文对应这些确切子集的最短/最长/平均时长 **NR**。不能拿原 MAD/MovieNet 全集均值代填经过筛选的 602/989 部子集。
- **帧率**：原始 FPS 和统一采样 FPS 均为 NR；明确使用镜头切分及 CLIP 视觉特征。本次未核实完整训练数据的直接下载可用性。

依据：论文数据收集和评测设置。[CVPR 2024 正式论文](https://openaccess.thecvf.com/content/CVPR2024/html/Argaw_Towards_Automated_Movie_Trailer_Generation_CVPR_2024_paper.html)；[作者论文版本](https://arxiv.org/abs/2404.03477)。

### B4. DocumentaryNet

论文：*TeaserGen: Generating Teasers for Long Documentaries*。

- **输入与输出**：输入纪录片主体视频、解说/音频等，输出 teaser 视频与解说。目标是激发观看兴趣，不能直接当作完整事实覆盖型摘要。
- **接收时间**：ICLR 2025；具体通知日未核实。
- **规模与标注**：**1,269 条纪录片**，来源包括 DW、PBS、National Geographic。人工找出纪录片开头专业制作 teaser 的边界，将其与主体分离形成参考；对语音、音乐和音效做分离，并转录解说等。参考 teaser 本身是已有创作，不是系统生成后作为 gold；论文测试集为 49 条。
- **视频长度**：主体平均 **31.3 分钟**，参考 teaser 平均 **79 秒（约 1.3 分钟）**；全体最短/最长 NR。
- **帧率**：原始 FPS 为 NR；论文模型视觉输入使用 **1 FPS**。时间边界、配音分段与视觉采样是不同粒度。

依据：数据构建与统计、实验实现。[ICLR 2025 正式论文](https://proceedings.iclr.cc/paper_files/paper/2025/file/bc667ac84ef58f2b5022da97a465cbab-Paper-Conference.pdf)。

### B5. Repurpose-10K

论文：*Video Repurposing from User Generated Content: A Large-scale Dataset and Benchmark*。

- **输入与输出**：输入长 UGC 视频、音频及字幕/ASR 信息；输出多条自包含短视频的起止时间区间。多条短视频各自独立传播，不要求拼成一个全局摘要。
- **接收时间**：AAAI 2025；作者仓库于 **2024-12-10 公告已接收**，该公告日不等同于已核实的通知日。
- **规模与标注**：先收集 **8,398 条原视频**；超过 30 分钟的原视频经过切分，形成 **11,210 个输入样本**，共 **120,925 个剪辑时间区间**。Opus Clip/OpusAI 先产生主题粗剪，用户通过喜欢/发布选择，并人工编辑起止边界；最终保留经过用户边界修改且认可的片段。属于真实用户偏好与编辑行为标注。
- **视频长度**：8,398 条原视频总长 **4,539.94 小时，平均 0.54 小时（约 32.4 分钟）**。这不是切分后 11,210 个样本的均值；后者均值和精确范围未单独报告。人评抽样的 462 个输出片段平均 58.66 秒，也不能写成全体 120,925 个片段的均值。
- **帧率**：原始 FPS 与统一视觉采样 FPS 为 NR；不能由短视频输出时长或 transcript 句子时间戳推算 FPS。

依据：Data Collection、Data Analysis 和 Human Evaluation。[AAAI 2025 正式文章](https://ojs.aaai.org/index.php/AAAI/article/view/32916)；[作者论文](https://arxiv.org/abs/2412.08879)；[官方仓库](https://github.com/yongliang-wu/Repurpose)。

### B6. VideoAds–Visual Summary

论文：*VideoAds for Fast-Paced Video Understanding*。

- **输入与输出**：输入广告视频和四选一问题，输出正确选项；Visual Summary 要识别正确的整体概括，**不要求模型生成摘要文本或视频片段**。
- **接收时间**：ICCV 2025；具体通知日未核实。
- **规模与标注**：全 benchmark **200 条广告、1,100 道选择题**，其中 **312 道 Visual Summary**，另有信息查找和推理。人工设计题目/答案，结合模型辅助干扰项及格式整理，再由专家过滤；312 是题目数，不是 312 条独立视频。
- **视频长度**：总体平均 **79.60 秒**；与 Summary 题关联的视频平均 **78.45 秒**。本次未核实精确最短/最长值。
- **帧率**：原始 FPS 为 NR；模型使用不同固定帧预算或各自采样方式，并非全 benchmark 固定一个 FPS。

依据：任务定义、数据统计和评测设置。[ICCV 2025 正式论文](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_VideoAds_for_Fast-Paced_Video_Understanding_ICCV_2025_paper.html)；[官方项目](https://videoadsbenchmark.netlify.app/)。

### B7. CineBench

论文：*A Benchmark and Multi-Agent System for Instruction-driven Cinematic Video Compilation*。

- **输入与输出**：输入一部或多部电影/剧集及编辑指令，输出筛选、重排、拼接的视频 compilation，可配合旁白等元素。它可支持摘要式指令，但整体任务比常规 summarization 更宽。
- **接收时间**：**ECCV 2026**。已在会议官方 Accepted Papers 列表定位到完整论文标题；列表注明仍待出版社检查。不是仅凭 2026 年 4 月 arXiv 上传认定接收。
- **规模与标注**：来自 **70 余部电影/剧集、500 余组指令—参考编排**，由 **5 名专业编辑**构建，含英文与中文素材；约 30% 指令为无法完成的负例，用于检验可行性判断。负例不应作为有正常参考摘要的正例计数。
- **视频长度**：长电影/剧集级或多视频输入；对应数据的最短/最长/平均时长 **NR**。不能用某个案例指令要求的“5 分钟输出”代替源视频长度。
- **帧率**：源 FPS 及统一输入采样 FPS 为 NR；实际观察预算随编辑系统工具流程变化，需要单独记录。

依据：论文 benchmark 构建与标注，会议接收目录。[论文](https://arxiv.org/abs/2604.10456)；[ECCV 2026 官方接收列表](https://eccv.ecva.net/Conferences/2026/AcceptedPapers)；[作者发表记录](https://shuchenweng.github.io/)。

### B8. HourVideo–Summarization

论文：*HourVideo: 1-Hour Video-Language Understanding*。

- **输入与输出**：输入第一视角视频及五选一问题，输出正确选项。Summarization 包括关键事件/物体、活动时间顺序、跨情境比较三类；它检验选择正确概括的能力，不要求生成一段自由文本摘要。
- **接收时间**：**NeurIPS 2024 Datasets and Benchmarks**；论文首页和作者项目页均明确列出会期，具体接收通知日未核实。
- **规模与标注**：从 Ego4D 选出 **500 条视频、77 种日常情境、12,976 道选择题**，其中 Summarization 为 **714 道题**。利用 Ego4D 的人工视觉 narrations 生成结构化内容，LLM 辅助出题，再经过人工反馈修正、无视频作答过滤和专家复核。Narrations 是标注者对画面的描述，不是自动等同于视频自身 ASR；所有题目总数也不是摘要子任务规模。
- **视频长度**：整体 **20–120 分钟，平均 45.7 分钟**，其中 113 条超过一小时；Summarization 子集单独长度分布 NR。
- **帧率**：原始 FPS 为 NR；其 caption-memory baseline 按一分钟分块、**0.5 FPS** 采样，其他原生多模态模型走各自输入接口，未统一为单一采样率。分块长度不等于 benchmark 把原视频切成独立一分钟测试题。

依据：论文数据构建、Figure 3、baseline 实现。[NeurIPS 2024 论文](https://arxiv.org/abs/2411.04998)；[官方项目与评价入口](https://hourvideo.stanford.edu/)。

## 三、已接收但不宜算作标准摘要 gold benchmark：1 项

### C1. M-D 电影—纪录片语料

论文：*Multimodal-Based and Aesthetic-Guided Narrative Video Summarization*。

- **输入与输出**：输入视频、音频与字幕，可结合用户文字描述；输出具有叙事性的视频镜头摘要。
- **接收时间**：**TMM**；作者机构的出版记录日期为 **2022-06-15**。具体接收通知日 NR，出版记录日期不冒充接收日。
- **规模与标注**：作者收集 **72 部纪录片、21,643 条带时间位置的情节描述**，与 94 部 MPII 电影组成 **166 部 M-D 语料**，用于文字—视频定位及叙事摘要实验。这些情节描述不是逐帧重要性或人工视频摘要 gold；摘要部分依赖用户研究。
- **视频长度**：完整电影/纪录片级输入；对应集合最短、最长和平均时长 NR。个别长片案例不能代表整个语料分布。
- **帧率**：原始 FPS 与统一视觉采样 FPS 为 NR；论文中时间定位的均匀分段数属于处理配置，不等于 FPS。

依据：[作者机构正式记录](https://ir.cwi.nl/pub/31736)；[作者公开论文全文](https://ir.cwi.nl/pub/31736/31736.pdf)；[补充材料](https://ir.cwi.nl/pub/31736/Supplementary%20material)。

## 四、容易误纳入的工作与版本

**LVSum 单独保留为待确认接收的候选，不计入上面的 21 项。**

*LVSum: A Benchmark for Timestamp-Aware Long Video Summarization* 与长视频、时间证据和多参考摘要的研究设定很接近，但截至本次检索，arXiv、Apple Research 页面及官方仓库未提供足够证据确认它已被题目指定 venues 接收；ECCV 2026 官方列表中也未检索到该标题。不能据此断言它被拒，也不能把项目页上线时间当作接收时间。

- **输入/输出**：视频帧及 timestamped transcript 输入，输出带起止时间、内容描述的重要片段摘要。
- **规模/标注**：72 条、13 类，每条最多 10 份人工参考，包含片段时间区间、描述与重要性。
- **长度**：10–55 分钟，平均约 16 分钟。
- **帧率**：原始 FPS 为 NR；论文模型输入是 **96 个均匀采样帧＋transcript**，评价重要性时使用 **1 FPS 时间网格**。这两者是不同步骤，不能写成模型以 1 FPS 看完整长视频。
- **时间状态**：2026 年预印本，具体指定 venue 接收状态待确认。

依据：[论文](https://arxiv.org/abs/2604.10024)；[Apple Research](https://machinelearning.apple.com/research/lvsum-video-summarization)；[官方仓库](https://github.com/apple/ml-lvsum-video-summarization)。

其他边界条目：

| 工作 | 本轮处理 | 依据 |
|---|---|---|
| VISTA / *What Is That Talk About?* | ACL 2025，不在指定 venues；输入视频是 ICML/NeurIPS 学术报告，不代表 benchmark 论文被这些会议接收 | [ACL Anthology](https://aclanthology.org/2025.acl-long.310/) |
| MM-AVS | NAACL 2021，不在指定 venues | [正式论文](https://aclanthology.org/2021.naacl-main.473/) |
| MLASK | Findings of EACL 2023，不在指定 venues | [正式论文](https://aclanthology.org/2023.findings-eacl.67/) |
| SD-VSum / S-VideoXum | ACM Multimedia 2025，不在指定 venues | [官方仓库](https://github.com/IDT-ITI/SD-VSum) |
| 360-VSumm | ACM IMX 2024 相关 workshop，不在指定 venues | [官方仓库](https://github.com/IDT-ITI/360-VSumm) |
| VISIOCITY | 有 2021 arXiv 和项目资料，本轮未确认题目指定 venues 的接收记录，不因 arXiv 年份纳入 | [官方项目](https://visiocity.github.io/) |
| SumMe / TVSum / QFVS | 原始 benchmark 分别来自 2014 / 2015 / 2017，超出 2021–2026；后续方法继续使用不会改变它们的首次发表时间 | [SumMe 原始论文](https://doi.org/10.1007/978-3-319-10584-0_33)；[TVSum 原始论文](https://openaccess.thecvf.com/content_cvpr_2015/html/Song_TVSum_Summarizing_Web_2015_CVPR_paper.html)；[QFVS 原始论文](https://openaccess.thecvf.com/content_cvpr_2017/html/Sharghi_Query-Focused_Video_Summarization_CVPR_2017_paper.html) |

“在旧 benchmark 上提出新方法”的论文不自动算作新 benchmark。本文未为填满每个 venue 强行添加条目；目前没有核实到满足上述纳入口径的 **ICML 新摘要 benchmark**，这不等于证明 ICML 没有相关方法论文。2026 年仅统计截止日已能核实接收的工作。

## 五、对 Video Summarization 研究选型的直接含义

1. **若主任务是视频—文本联合摘要**：优先检查 VideoXum、Instruct-V2Xum、MMSum、BLiSS；它们在视频片段、关键帧、文本生成/抽取及标注来源上差异很大，不能仅因都有“video＋text”就共用一个评价结论。
2. **若主任务是长视频的重要内容选择**：LfVS-T、MMSum、PlotSnap 和 MoSu 附加 50 条长视频集更贴近长输入，但人工编辑、recap 与回放热度对应不同目标。Shot2Story 的多镜头复杂性不能替代长时序覆盖验证。
3. **若要验证 claim–segment grounding**，即每条文字主张是否被最终选中的视频片段支持，上述多数资源没有独立逐主张支持/不支持标签。联合输出或时间戳标注本身不能证明事实性；应补充人工对齐评估，并同时测重要事件覆盖，防止通过删掉难验证内容提高表面准确率。
4. **若要验证 agentic 的收益**：固定证据集与允许重读视频的设置应分开。对齐总观察帧数、分辨率、transcript、工具调用与输出时长；原始视频很长而模型仅看 96/100 帧时，主要考验的是稀疏信息选择，不能直接声称解决了超长上下文推理。

**优先补齐的信息**：正式实验前下载目标 benchmark 的 manifest 与评价代码，核对输入单元、划分、字幕可用性和输出预算；对原始 FPS 为 NR 的条目使用 ffprobe 逐文件测量并区分可变帧率；对混合任务数据单独统计 VS 子集。报告中的 NR 保留了这些实际证据缺口，避免把未核实项写成确定数字。
