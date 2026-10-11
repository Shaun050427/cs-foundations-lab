# CS Foundations Lab · 计算机科学实验室

**把算法、底层原理与工程实践连接起来，用可运行代码和可复现证据验收学习。**

- 学习应用：https://shaun050427.github.io/cs-foundations-lab/
- 总体目标与日程：https://shaun050427.github.io/personal-growth-app/#cs
- 新用户先打开「学习总览」，进入第一课「同一字节，两个解释」。

## 第一版可用功能

- 五阶段、20课：表示与推理 → 算法与结构 → 执行与内存 → 系统与存储 → 工程与迁移。
- 每课包含先修关系、算法与系统连接、具体练习、思考题、参考解释和证据验收。
- 可点击的知识连接图；学习验收为本人确认，不能当作标准化能力测评。
- 插入/归并排序：单步、回放、暂停、精确比较与主数组写入计数。
- 直接映射缓存：相同64元素的行式、列式、固定种子随机访问；改变缓存行数和块大小。
- BFS/DFS：工作队列或栈、已发现节点和访问顺序。
- 字节：无符号与8位补码解释。
- 学习记录的新增、编辑、搜索、删除；实验观察转为记录草稿。
- 完整JSON备份、带预览的恢复、指定日期范围的AI复盘Markdown。
- 成长系统导入：同一ID幂等更新，记录进入成果资产与每周复盘，项目保存阶段/下一里程碑/每周投入摘要。

**数据边界：** 网页公开代码与课程；个人学习状态仅保存在浏览器localStorage，不上传服务器。换设备、清除网站数据或无痕窗口前请导出JSON。两个网站的本机存储相互独立，不宣称自动双向同步。成长系统的现有GitHub私人数据同步按原有配置运行。完整备份和详细进度由实验室维护，成长系统只导入成果和目标摘要。V1生成可交给AI分析的文件，没有模型API或自动AI评分。

## 运行与验证

网页是无构建、无第三方依赖的静态应用。开发时可从仓库根目录运行：

```bash
python -m http.server 8000
```

然后打开 `http://localhost:8000`。代码有分文件脚本；不建议用file://协议作为主要运行方式。

```bash
npm run check
npm test
python -m unittest discover -s tests -p 'test_*.py'
python experiments/benchmark.py --size 1000 --repeats 7
python experiments/sqlite_index.py
cc -O2 -std=c11 -Wall -Wextra -pedantic experiments/locality.c -o locality
./locality 1048576 7
```

Windows用户可直接使用在线学习应用。Python实验可在本机Python运行；C实验可使用WSL或合适的C编译器。C11程序使用TIME_UTC墙钟，时钟调整或小规模计时可能失真，建议扩大n、重复、保留原始数据。

## 学习节奏与迁移

建议每周约4小时：两次45–60分钟学习，一次60–90分钟实验，再用30分钟整理证据与复盘。根据课程基础与实际时间调整，不承诺固定周数学完。每个主题遵循：**独立预测 → 写实现/证明 → 运行对照 → 记录反例 → 保存验收证据**。

三个最终作品方向：Kaggle预处理性能与一致性、成长系统幂等导入与同步恢复、行情工具的窗口统计与数据缺失处理。先选一个实际瓶颈，不同时铺开。优化不自动意味着竞赛成绩或投资收益提升。

## 仓库结构

```text
index.html                  学习工作台
css/style.css               响应式界面
js/curriculum.js            五阶段20课与资源
js/lab.js                   纯函数实验模型
js/app.js                   界面、备份、记录和复盘
js/transfer.js              与成长系统共享的导入协议
experiments/algorithms.py   排序、二分、BFS参考实现
experiments/benchmark.py    实际排序计时与环境记录
experiments/locality.c      同工作量布局对照
experiments/sqlite_index.py 查询计划与索引实验
 tests/                     正确性与幂等性检查
 docs/                      实验方法、验证记录与维护指南
```

## 维护原则

- 修改算法时先给出规格、基线和反例，保持参考判定器独立。
- 不把模拟计数写成CPU实测，不把环境内的一次结果写成普遍保证。
- 不在公开仓库提交个人备份、令牌、竞赛私有数据或付费材料。
- 每次源代码提交自动运行GitHub Actions验证。
- 发布由GitHub Pages的main分支根目录提供；不要把整个仓库发布成含个人数据的镜像。
- 成长系统共享 `cs-transfer.js` 与 `cs-curriculum.js`，变更协议时同步两端并运行幂等性检查。

资源选用MIT 6.006、CMU 15-213、Python文档和SQLite官方文档。仅链接原始资源，不复制教材正文。参考[实验方法](docs/EXPERIMENTS.md)、[验证记录](docs/VERIFICATION.md)、[下一步维护](docs/ROADMAP.md)。
