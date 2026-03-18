from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from level2_c_bug_trap_pack import build_level2_c_bug_trap_pack
from level2_c_comprehensive_programming_pack import build_level2_c_comprehensive_programming_pack
from level2_c_file_linkedlist_pack import build_level2_c_file_linkedlist_pack
from level2_c_high_frequency_pack import build_level2_c_high_frequency_pack
from level2_c_pointer_algorithm_advanced_pack import build_level2_c_pointer_algorithm_advanced_pack
from level2_c_problem_solving_pack import build_level2_c_problem_solving_pack
from level2_c_recursion_matrix_pack import build_level2_c_recursion_matrix_pack
from level2_c_sort_search_pack import build_level2_c_sort_search_pack
from level2_c_string_file_advanced_pack import build_level2_c_string_file_advanced_pack
from level2_c_file_structure_case_pack import build_level2_c_file_structure_case_pack
from level2_c_structure_memory_project_pack import build_level2_c_structure_memory_project_pack


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
QUESTION_BANK_DIR = DATA_DIR / "question_banks"


def single_choice(question_id, stem, options, answer, analysis, tags, difficulty="medium", score=2):
    return {
        "id": question_id,
        "type": "single_choice",
        "stem": stem,
        "options": options,
        "answer": answer,
        "analysis": analysis,
        "tags": tags,
        "difficulty": difficulty,
        "score": score,
    }


def fill_blank(question_id, stem, answers, analysis, tags, difficulty="medium", score=5):
    return {
        "id": question_id,
        "type": "fill_blank",
        "stem": stem,
        "answer": answers,
        "analysis": analysis,
        "tags": tags,
        "difficulty": difficulty,
        "score": score,
    }


def code_completion(question_id, stem, answers, analysis, tags, difficulty="medium", score=5):
    return {
        "id": question_id,
        "type": "code_completion",
        "stem": stem,
        "answer": answers,
        "analysis": analysis,
        "tags": tags,
        "difficulty": difficulty,
        "score": score,
    }


def rubric_item(description, keywords, points):
    return {"description": description, "keywords": keywords, "points": points}


def subjective(question_id, qtype, stem, analysis, rubric, tags, difficulty="medium", score=10):
    return {
        "id": question_id,
        "type": qtype,
        "stem": stem,
        "analysis": analysis,
        "rubric": rubric,
        "tags": tags,
        "difficulty": difficulty,
        "score": score,
    }


def infer_standard_topic(question):
    text = " ".join(
        [question.get("stem", "")]
        + list(question.get("tags", []))
    )
    rules = [
        ("C基础", ["C基础", "标识符", "类型", "表达式", "复合赋值", "逻辑运算", "运算"]),
        ("动态内存", ["malloc", "free", "动态内存", "内存", "悬空", "泄漏"]),
        ("结构体", ["结构体", "链表", "成员", "结点", "联合", "struct"]),
        ("文件", ["文件", "fopen", "fclose", "fprintf", "fscanf", "feof", "FILE"]),
        ("指针", ["指针", "地址", "解引用", "空指针"]),
        ("数组", ["数组", "下标", "二维数组", "顺序表"]),
        ("字符串", ["字符串", "字符", "strlen", "strcpy", "strcmp", "strcat", "\\0"]),
        ("函数", ["函数", "形参", "实参", "递归", "return", "原型", "参数"]),
        ("输入输出", ["printf", "scanf", "输入输出"]),
        ("预处理", ["预处理", "宏", "#define", "头文件", "条件编译"]),
        ("控制结构", ["switch", "while", "for", "break", "continue", "控制结构", "条件"]),
        ("算法与数据结构", ["算法", "排序", "查找", "队列", "栈", "树", "二叉树"]),
        ("公共基础", ["公共基础", "软件工程", "数据库"]),
        ("程序设计", ["程序设计", "编程", "设计思路"]),
    ]
    for topic, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return topic
    return question["type"]


def annotate_bank_questions(questions, high_frequency_ids=None):
    high_frequency_ids = set(high_frequency_ids or [])
    for question in questions:
        question.setdefault("source", "curated")
        question.setdefault("topic", infer_standard_topic(question))
        question.setdefault("frequency", "high" if question["id"] in high_frequency_ids else "medium")
    return questions


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_level1_office_bank():
    questions = [
        single_choice("L1OFF-001", "在 Word 中，要快速复制格式，最适合使用的工具是：", ["A. 页面布局", "B. 格式刷", "C. 拼写检查", "D. 分栏"], "B", "格式刷用于复制并批量应用已有格式。", ["Word", "排版"], "easy"),
        single_choice("L1OFF-002", "Excel 中函数 `SUM(A1:A5)` 的作用是：", ["A. 计算平均值", "B. 统计个数", "C. 求和", "D. 查找最大值"], "C", "SUM 用于求一组单元格的和。", ["Excel", "函数"], "easy"),
        single_choice("L1OFF-003", "PowerPoint 中要让对象依次出现，应设置：", ["A. 页面方向", "B. 动画顺序", "C. 页眉页脚", "D. 主题字体"], "B", "动画顺序控制对象在播放中的先后。", ["PowerPoint", "动画"], "easy"),
        single_choice("L1OFF-004", "在 Windows 中，`Ctrl + C` 的常见功能是：", ["A. 保存", "B. 复制", "C. 粘贴", "D. 撤销"], "B", "Ctrl + C 是复制快捷键。", ["Windows", "基础"], "easy"),
        fill_blank("L1OFF-005", "Excel 中用于返回最大值的函数是 ______。", ["MAX"], "MAX 函数返回指定区域中的最大值。", ["Excel", "函数"], "easy"),
        fill_blank("L1OFF-006", "PowerPoint 演示文稿的默认扩展名通常为 ______。", ["pptx", ".pptx"], "Office 新版演示文稿默认保存为 pptx。", ["PowerPoint", "文件"], "easy"),
        single_choice("L1OFF-007", "数据库中用于唯一标识记录的字段通常称为：", ["A. 主键", "B. 索引", "C. 备注", "D. 标题"], "A", "主键用于唯一标识一条记录。", ["数据库", "基础"], "medium"),
        single_choice("L1OFF-008", "邮件中抄送的英文缩写通常是：", ["A. FTP", "B. PDF", "C. CC", "D. SQL"], "C", "CC 表示 Carbon Copy。", ["网络应用", "办公"], "easy"),
        code_completion("L1OFF-009", "在 Word 表格中，按 `Tab` 键位于最后一个单元格时会自动 ______ 新的一行。", ["创建", "插入"], "Word 会在最后一个单元格按 Tab 时自动新增行。", ["Word", "表格"], "medium"),
        single_choice("L1OFF-010", "WPS 或 Office 文档中，保护文档常见的方式是：", ["A. 设置密码", "B. 关闭窗口", "C. 更换主题", "D. 调整缩放"], "A", "文档保护通常通过密码或限制编辑完成。", ["安全", "办公"], "easy"),
        subjective("L1OFF-011", "short_answer", "简述制作一份规范汇报型 PPT 时至少应注意的三项排版原则。", "应回答出层级清晰、统一配色、字号对比、留白合理、图文平衡等原则。", [rubric_item("层级清晰", ["层级", "标题", "结构"], 3), rubric_item("视觉统一", ["统一", "配色", "字体"], 3), rubric_item("留白或图文平衡", ["留白", "图文", "对齐"], 4)], ["PowerPoint", "表达"], "medium"),
        subjective("L1OFF-012", "short_answer", "说明在 Excel 中制作成绩表时，为什么要把原始数据区与统计分析区分开。", "应说明避免覆盖原始数据、便于公式管理、方便数据透视或筛选。", [rubric_item("避免覆盖原始数据", ["覆盖", "原始数据"], 4), rubric_item("便于公式管理", ["公式", "管理"], 3), rubric_item("便于筛选或透视", ["筛选", "透视", "分析"], 3)], ["Excel", "数据分析"], "medium"),
    ]
    return {
        "subject_code": "level1_office",
        "subject_name": "一级计算机基础及 MS Office 应用",
        "default_blueprint": {"duration_minutes": 30, "quotas": [{"type": "single_choice", "count": 5}, {"type": "fill_blank", "count": 2}, {"type": "short_answer", "count": 1}]},
        "questions": questions,
    }


def build_level2_python_bank():
    questions = [
        single_choice("L2PY-001", "Python 中列表推导式的主要作用是：", ["A. 定义类", "B. 快速构造列表", "C. 声明异常", "D. 导入模块"], "B", "列表推导式适合根据迭代规则快速生成列表。", ["Python", "语法"], "easy"),
        single_choice("L2PY-002", "表达式 `3 // 2` 的结果是：", ["A. 1", "B. 1.5", "C. 2", "D. 0"], "A", "`//` 表示整除。", ["Python", "运算"], "easy"),
        single_choice("L2PY-003", "下列哪一个是不可变类型？", ["A. list", "B. dict", "C. tuple", "D. set"], "C", "tuple 不可变。", ["Python", "数据类型"], "easy"),
        fill_blank("L2PY-004", "用于定义函数的关键字是 ______。", ["def"], "`def` 用于定义函数。", ["Python", "函数"], "easy"),
        code_completion("L2PY-005", "补全代码：`for i in ______(5):` 可以依次得到 0 到 4。", ["range"], "range(5) 生成 0 到 4。", ["Python", "循环"], "easy"),
        single_choice("L2PY-006", "读取文本文件常用的模式是：", ["A. wb", "B. rb", "C. r", "D. ab"], "C", "普通文本读取一般使用 r 模式。", ["Python", "文件"], "easy"),
        single_choice("L2PY-007", "若要随机打乱列表元素顺序，应使用模块：", ["A. math", "B. random", "C. csv", "D. pathlib"], "B", "random 模块提供 shuffle 等能力。", ["Python", "库"], "easy"),
        fill_blank("L2PY-008", "异常处理语句中，用于捕获异常的关键字是 ______。", ["except"], "try-except 用于异常处理。", ["Python", "异常"], "easy"),
        subjective("L2PY-009", "bug_fix", "说明为什么在函数参数中直接写可变默认值（如 `items=[]`）通常不推荐。", "应指出默认值只创建一次，可能导致多次调用共享同一对象。", [rubric_item("默认值只创建一次", ["一次", "创建"], 4), rubric_item("多次调用共享对象", ["共享", "同一对象"], 4), rubric_item("建议用 None 代替", ["None"], 2)], ["Python", "函数"], "medium"),
        subjective("L2PY-010", "programming", "编写思路：给定一组整数，统计其中偶数个数并输出平均值。说明你的实现步骤。", "答案应包含遍历、筛选偶数、累计求和与计数、除零判断。", [rubric_item("遍历序列", ["遍历", "循环"], 2), rubric_item("筛选偶数", ["偶数", "%2"], 3), rubric_item("累计求和与计数", ["求和", "计数"], 3), rubric_item("除零判断", ["除零", "没有偶数"], 2)], ["Python", "程序设计"], "medium"),
    ]
    return {
        "subject_code": "level2_python",
        "subject_name": "二级 Python 语言程序设计",
        "default_blueprint": {"duration_minutes": 45, "quotas": [{"type": "single_choice", "count": 4}, {"type": "fill_blank", "count": 2}, {"type": "bug_fix", "count": 1}, {"type": "programming", "count": 1}]},
        "questions": questions,
    }


def build_level3_network_bank():
    questions = [
        single_choice("L3NET-001", "IP 地址 192.168.1.1 属于哪一类常见网络用途？", ["A. 公网广播", "B. 私有地址", "C. 组播地址", "D. 环回地址"], "B", "192.168.x.x 是常见私有地址段。", ["网络基础", "IP"], "easy"),
        single_choice("L3NET-002", "HTTP 默认使用的传输层协议是：", ["A. UDP", "B. ICMP", "C. TCP", "D. ARP"], "C", "HTTP 基于 TCP。", ["网络协议", "HTTP"], "easy"),
        single_choice("L3NET-003", "交换机主要工作在 OSI 的哪一层？", ["A. 物理层", "B. 数据链路层", "C. 传输层", "D. 会话层"], "B", "传统交换机主要工作在二层。", ["网络设备"], "easy"),
        fill_blank("L3NET-004", "DNS 的主要作用是把域名解析为 ______。", ["IP地址", "IP"], "DNS 负责域名与 IP 的映射。", ["DNS"], "easy"),
        single_choice("L3NET-005", "使用 HTTPS 的主要安全收益是：", ["A. 增大带宽", "B. 加密与身份认证", "C. 自动备份", "D. 绕过防火墙"], "B", "HTTPS 基于 TLS 提供加密和认证。", ["安全", "HTTPS"], "medium"),
        code_completion("L3NET-006", "常见局域网中用于自动分配 IP 地址的协议是 ______。", ["DHCP"], "DHCP 用于动态分配地址。", ["网络协议"], "easy"),
        subjective("L3NET-007", "short_answer", "说明路由器与交换机在典型企业网络中的分工差异。", "应区分二层转发与三层互联、广播域隔离、跨网段通信。", [rubric_item("交换机负责二层转发", ["二层", "交换机"], 3), rubric_item("路由器负责三层互联", ["三层", "路由器", "跨网段"], 4), rubric_item("提到广播域或隔离", ["广播域", "隔离"], 3)], ["网络设备"], "medium"),
        subjective("L3NET-008", "bug_fix", "某管理员将服务器默认网关配置为错误地址，说明将导致什么现象以及如何排查。", "应说明本地通信可能正常但跨网段失败，可检查 IP、掩码、网关及路由。", [rubric_item("跨网段访问失败", ["跨网段", "外网", "失败"], 4), rubric_item("检查网关与路由", ["网关", "路由"], 4), rubric_item("检查地址与掩码", ["IP", "掩码"], 2)], ["网络运维"], "medium"),
    ]
    return {
        "subject_code": "level3_network",
        "subject_name": "三级网络技术",
        "default_blueprint": {"duration_minutes": 45, "quotas": [{"type": "single_choice", "count": 4}, {"type": "fill_blank", "count": 1}, {"type": "short_answer", "count": 1}, {"type": "bug_fix", "count": 1}]},
        "questions": questions,
    }


def build_level4_network_engineer_bank():
    questions = [
        single_choice("L4NE-001", "在企业网络中部署双核心冗余，主要目标之一是：", ["A. 增加桌面数量", "B. 提高可用性", "C. 减少日志", "D. 替代防病毒"], "B", "双核心设计主要用于提高可用性与容错。", ["架构", "高可用"], "medium"),
        single_choice("L4NE-002", "BGP 更适用于：", ["A. 单机文件管理", "B. 大规模自治系统之间路由交换", "C. 局域网打印共享", "D. 本地串口通信"], "B", "BGP 常用于自治系统之间的路由交换。", ["路由协议"], "medium"),
        fill_blank("L4NE-003", "常用来发现与修复系统漏洞的管理过程称为 ______ 管理。", ["补丁", "patch"], "补丁管理是运维安全的重要部分。", ["安全运维"], "medium"),
        subjective("L4NE-004", "short_answer", "说明在设计企业网络监控体系时，为什么既要关注链路状态，也要关注业务指标。", "应说明链路层正常不代表业务正常，需结合应用响应、错误率、吞吐与容量。", [rubric_item("链路正常不代表业务正常", ["链路", "业务正常"], 4), rubric_item("应用响应或错误率", ["响应", "错误率"], 3), rubric_item("吞吐、容量或趋势", ["吞吐", "容量", "趋势"], 3)], ["监控", "运维"], "medium"),
        subjective("L4NE-005", "programming", "说明设计一份网络变更实施方案时至少需要包含哪些核心部分。", "应包含变更目标、影响评估、实施步骤、回退方案、验证与通知。", [rubric_item("目标与范围", ["目标", "范围"], 2), rubric_item("影响评估", ["影响", "评估"], 2), rubric_item("实施步骤", ["步骤", "实施"], 2), rubric_item("回退方案", ["回退"], 2), rubric_item("验证与通知", ["验证", "通知"], 2)], ["工程管理"], "medium"),
    ]
    return {
        "subject_code": "level4_network_engineer",
        "subject_name": "四级网络工程师",
        "default_blueprint": {"duration_minutes": 40, "quotas": [{"type": "single_choice", "count": 2}, {"type": "fill_blank", "count": 1}, {"type": "short_answer", "count": 1}, {"type": "programming", "count": 1}]},
        "questions": questions,
    }


def build_level2_c_bank():
    questions = []
    questions.extend([
        single_choice("L2C-001", "下列关于算法的叙述中，正确的是：", ["A. 算法必须有穷结束", "B. 算法可以没有输出", "C. 算法只能用流程图表示", "D. 算法必须有两个以上输入"], "A", "算法应具备有穷性、确定性、可行性、输入和输出特征。", ["公共基础", "算法"], "easy"),
        single_choice("L2C-002", "下列数据结构中，属于非线性结构的是：", ["A. 栈", "B. 队列", "C. 二叉树", "D. 线性表"], "C", "二叉树属于树形结构，是典型非线性结构。", ["公共基础", "数据结构"], "easy"),
        single_choice("L2C-003", "在长度为 n 的顺序表中，平均查找时间最短的无序查找方法是：", ["A. 顺序查找", "B. 二分查找", "C. 哈希查找", "D. 归并查找"], "A", "无序顺序表只能顺序查找；二分查找要求有序。", ["公共基础", "查找"], "medium"),
        single_choice("L2C-004", "设循环队列的存储空间大小为 m，则队满条件常写为：", ["A. front == rear", "B. (rear + 1) % m == front", "C. rear == m", "D. front == -1"], "B", "循环队列通常预留一个空位，用于区分队空与队满。", ["公共基础", "队列"], "medium"),
        single_choice("L2C-005", "下列排序方法中，平均时间复杂度通常为 O(n log n) 的是：", ["A. 直接插入排序", "B. 冒泡排序", "C. 快速排序", "D. 简单选择排序"], "C", "快速排序平均复杂度为 O(n log n)，最坏可到 O(n^2)。", ["公共基础", "排序"], "easy"),
        single_choice("L2C-006", "数据库设计中，用于描述实体之间联系的模型通常是：", ["A. E-R 模型", "B. 队列模型", "C. 数组模型", "D. 递归模型"], "A", "E-R 模型用于概念设计阶段描述实体、属性与联系。", ["公共基础", "数据库"], "easy"),
        single_choice("L2C-007", "软件生命周期中，确定系统做什么而不是怎样做的阶段是：", ["A. 需求分析", "B. 编码", "C. 测试", "D. 维护"], "A", "需求分析关注功能与约束，是“做什么”。", ["公共基础", "软件工程"], "easy"),
        single_choice("L2C-008", "下列关于结构化程序设计的叙述中，正确的是：", ["A. 只允许顺序结构", "B. 只关注编码，不关注设计", "C. 强调顺序、选择和循环三种基本结构", "D. 不允许定义函数"], "C", "结构化程序设计建立在三种基本控制结构之上。", ["公共基础", "程序设计"], "easy"),
        single_choice("L2C-009", "下列 C 语言标识符中，合法的是：", ["A. 2sum", "B. total-score", "C. _count", "D. int"], "C", "标识符可由字母、数字和下划线组成，不能以数字开头，不能是关键字。", ["C基础", "标识符"], "easy"),
        single_choice("L2C-010", "表达式 `5/2` 在 C 语言中的结果是：", ["A. 2", "B. 2.5", "C. 3", "D. 2.0"], "A", "两个整型相除执行整除，结果仍为整型。", ["C基础", "运算"], "easy"),
        single_choice("L2C-011", "若 `int a = 3, b = 4;`，则表达式 `a > b ? a : b` 的值为：", ["A. 3", "B. 4", "C. 7", "D. 1"], "B", "条件运算符根据条件返回其中一个表达式值。", ["C基础", "运算"], "easy"),
        single_choice("L2C-012", "下列类型中，通常用于保存单个字符的是：", ["A. int", "B. float", "C. char", "D. double"], "C", "char 类型通常占 1 字节，用于存储字符。", ["C基础", "类型"], "easy"),
        single_choice("L2C-013", "执行 `printf(\"%d\", 3 + 4 * 2);` 的输出结果是：", ["A. 11", "B. 14", "C. 10", "D. 8"], "A", "乘法优先级高于加法，因此先算 4*2。", ["C基础", "表达式"], "easy"),
        single_choice("L2C-014", "若 `int x = 1;`，执行 `x += 2 * 3;` 后，x 的值为：", ["A. 5", "B. 6", "C. 7", "D. 8"], "C", "先计算 2*3，再执行 x=x+6。", ["C基础", "复合赋值"], "easy"),
        single_choice("L2C-015", "下列关于 `switch` 语句的叙述中，错误的是：", ["A. 表达式结果通常是整型或字符型", "B. `case` 后必须是常量表达式", "C. 每个 `case` 后都必须写 `break`", "D. 可以有 `default` 分支"], "C", "并非每个 case 都必须写 break，但不写时会发生贯穿。", ["控制结构", "switch"], "medium"),
        single_choice("L2C-016", "若 `i=0`，执行 `while(i<3) i++;` 后，i 的值为：", ["A. 0", "B. 2", "C. 3", "D. 4"], "C", "循环执行到 i 不再小于 3 时结束。", ["控制结构", "while"], "easy"),
        single_choice("L2C-017", "在 C 语言中，函数形参属于：", ["A. 全局变量", "B. 自动变量", "C. 静态变量", "D. 外部变量"], "B", "普通形参在函数调用时分配，属于自动存储期。", ["函数", "变量"], "medium"),
        single_choice("L2C-018", "若希望函数不返回任何值，函数返回类型应定义为：", ["A. int", "B. char", "C. void", "D. null"], "C", "void 表示函数无返回值。", ["函数", "基础"], "easy"),
        single_choice("L2C-019", "数组定义 `int a[5];` 后，其合法下标范围是：", ["A. 0~4", "B. 1~5", "C. 0~5", "D. 1~4"], "A", "C 语言数组下标从 0 开始。", ["数组", "基础"], "easy"),
        single_choice("L2C-020", "字符串常量 `\"abc\"` 在内存中实际占用的字符个数通常是：", ["A. 2", "B. 3", "C. 4", "D. 5"], "C", "字符串末尾会自动补充结束符 '\\0'。", ["字符串", "基础"], "easy"),
    ])
    questions.extend([
        single_choice("L2C-021", "设 `int a[3]={1,2,3};`，则 `*(a+1)` 的值为：", ["A. 1", "B. 2", "C. 3", "D. 地址值"], "B", "数组名在表达式中可退化为首元素地址，`a+1` 指向第二个元素。", ["指针", "数组"], "medium"),
        single_choice("L2C-022", "设 `char s[]=\"good\";`，则 `strlen(s)` 的值为：", ["A. 3", "B. 4", "C. 5", "D. 6"], "B", "strlen 返回字符串长度，不包含结束符。", ["字符串", "库函数"], "easy"),
        single_choice("L2C-023", "以下关于指针的叙述中，正确的是：", ["A. 指针变量只能保存整型值", "B. 指针变量保存的是地址", "C. `*p` 表示变量 p 的地址", "D. 指针变量不能为 NULL"], "B", "指针变量用于保存地址，`*p` 表示解引用。", ["指针", "基础"], "easy"),
        single_choice("L2C-024", "若 `int x=10; int *p=&x;`，执行 `*p = 20;` 后，x 的值为：", ["A. 10", "B. 20", "C. 0", "D. 不确定"], "B", "通过指针修改的是其所指向变量的值。", ["指针", "赋值"], "easy"),
        single_choice("L2C-025", "定义结构体变量时，正确的语句是：", ["A. `struct student s;`", "B. `student struct s;`", "C. `struct = student s;`", "D. `student s struct;`"], "A", "使用结构体标签定义变量时，语法为 `struct 标签名 变量名;`。", ["结构体", "基础"], "easy"),
        single_choice("L2C-026", "若有定义 `struct student st;`，访问成员 score 的正确写法是：", ["A. `st->score`", "B. `st.score`", "C. `score.st`", "D. `st::score`"], "B", "普通结构体变量用 `.` 访问成员，指针才用 `->`。", ["结构体", "成员访问"], "easy"),
        single_choice("L2C-027", "文件打开方式字符串 `\"r\"` 的含义是：", ["A. 只写文本文件", "B. 只读文本文件", "C. 追加文本文件", "D. 读写二进制文件"], "B", "r 表示以只读方式打开文本文件。", ["文件", "基础"], "easy"),
        single_choice("L2C-028", "若 `FILE *fp;`，要判断文件是否成功打开，通常应判断：", ["A. `fp == EOF`", "B. `fp == NULL`", "C. `fp == 0.0`", "D. `fp == '\\0'`"], "B", "fopen 失败时返回 NULL。", ["文件", "基础"], "easy"),
        single_choice("L2C-029", "预处理命令 `#define PI 3.14` 的作用是：", ["A. 定义变量", "B. 定义函数", "C. 宏替换", "D. 编译链接"], "C", "define 在预处理阶段进行文本替换。", ["预处理", "宏"], "easy"),
        single_choice("L2C-030", "若希望头文件在一个源文件中被多次包含时只生效一次，通常使用：", ["A. `#define int`", "B. 条件编译保护", "C. `#undef`", "D. `#pragma message`"], "B", "常见方式是配合 `#ifndef/#define/#endif` 使用。", ["预处理", "头文件"], "medium"),
        single_choice("L2C-031", "递归函数必须具备的条件之一是：", ["A. 至少有两个返回值", "B. 必须定义为 void", "C. 必须有结束条件", "D. 只能调用一次自身"], "C", "递归若无结束条件，将导致无限递归。", ["函数", "递归"], "easy"),
        single_choice("L2C-032", "下列关于 `static` 局部变量的叙述中，正确的是：", ["A. 每次调用函数都会重新初始化", "B. 生命周期延续到程序结束", "C. 只能在 main 中定义", "D. 不能赋初值"], "B", "静态局部变量作用域仍在函数内，但生命周期贯穿程序运行期。", ["存储类型", "static"], "medium"),
        single_choice("L2C-033", "若 `int a=1,b=2,c=3;`，表达式 `a<b && b<c` 的值为：", ["A. 0", "B. 1", "C. 2", "D. 3"], "B", "逻辑与在两个条件都为真时结果为 1。", ["C基础", "逻辑运算"], "easy"),
        single_choice("L2C-034", "C 语言中字符常量 `'A'` 与字符串常量 `\"A\"` 的主要区别是：", ["A. 前者是一个字符，后者是两个字符数组元素含结束符", "B. 二者完全等价", "C. 前者不能参与运算", "D. 后者长度为 1"], "A", "字符常量是单个字符值，字符串常量包含结束符。", ["字符", "字符串"], "medium"),
        single_choice("L2C-035", "函数 `gets` 不再推荐使用，主要原因是：", ["A. 速度太慢", "B. 只能读取数字", "C. 缺乏边界检查，容易造成缓冲区溢出", "D. 只能在 Linux 使用"], "C", "gets 无法限制读取长度，存在严重安全隐患。", ["字符串", "安全"], "medium"),
        single_choice("L2C-036", "对于二维数组 `int a[2][3];`，元素个数一共有：", ["A. 5", "B. 6", "C. 8", "D. 9"], "B", "二维数组元素总数是各维长度相乘。", ["数组", "二维数组"], "easy"),
        single_choice("L2C-037", "若要把整数按十进制形式输出，`printf` 常用的格式控制符是：", ["A. `%c`", "B. `%f`", "C. `%d`", "D. `%s`"], "C", "%d 用于按十进制输出 int。", ["输入输出", "printf"], "easy"),
        single_choice("L2C-038", "语句 `break;` 在循环中的作用是：", ["A. 结束本次循环，进入下一次", "B. 结束所在循环或 switch", "C. 终止整个程序", "D. 返回函数调用处"], "B", "break 会立即跳出最近一层循环或 switch。", ["控制结构", "break"], "easy"),
        single_choice("L2C-039", "语句 `continue;` 在循环中的作用是：", ["A. 跳出整个循环", "B. 返回上一层函数", "C. 结束本次循环并进入下一次", "D. 重新初始化循环变量"], "C", "continue 会跳过本次循环剩余语句。", ["控制结构", "continue"], "easy"),
        single_choice("L2C-040", "下列关于数组名的叙述中，正确的是：", ["A. 数组名是变量，可以自增", "B. 数组名在大多数表达式中可视为首元素地址", "C. 数组名总是等价于指针变量", "D. 可以给数组名重新赋值"], "B", "数组名不是普通变量，但在大多数表达式中会退化为首元素地址。", ["数组", "指针"], "medium"),
    ])
    questions.extend([
        fill_blank("L2C-041", "在 C 语言中，执行 `for(i=0;i<n;i++)` 时，循环体一共最多执行 ______ 次。", ["n"], "i 从 0 递增到 n-1，共执行 n 次。", ["控制结构", "for"], "easy"),
        fill_blank("L2C-042", "字符串结束标志是字符常量 ______。", ["\\0", "'\\0'"], "C 字符串以空字符作为结束标志。", ["字符串", "基础"], "easy"),
        fill_blank("L2C-043", "若要在函数内部修改主调函数中的变量值，常见做法是传入该变量的 ______。", ["地址", "指针"], "通过地址或指针传递可在函数内部修改实参对应变量。", ["函数", "指针"], "easy"),
        fill_blank("L2C-044", "文件操作完成后，应调用 ______ 函数关闭文件。", ["fclose"], "文件打开后应及时 fclose。", ["文件", "基础"], "easy"),
        fill_blank("L2C-045", "动态内存申请成功后，指针变量中保存的是所申请内存块的 ______。", ["首地址", "地址"], "malloc 等函数返回内存块首地址。", ["指针", "内存"], "medium"),
        fill_blank("L2C-046", "要判断字符 ch 是否为数字字符 `'0'` 到 `'9'`，可以利用字符编码的 ______ 性。", ["连续", "连续性"], "数字字符在编码表中通常连续排列。", ["字符", "基础"], "medium"),
        code_completion("L2C-047", "补全代码：`int max(int a,int b){ return a>b ? a : ______; }`", ["b"], "条件运算符在 a 不大于 b 时返回 b。", ["函数", "条件运算"], "easy"),
        code_completion("L2C-048", "补全代码：`for(i=0; i<10; i++) sum += a[____];`", ["i"], "遍历数组时通常使用当前循环变量作为下标。", ["数组", "循环"], "easy"),
        code_completion("L2C-049", "补全代码：`if(fp == NULL){ printf(\"open error\\n\"); return ______; }`，设该函数返回整型。", ["0", "-1"], "文件打开失败时通常提前返回约定的错误值。", ["文件", "错误处理"], "medium"),
        code_completion("L2C-050", "补全代码：`while( s[i] != '\\0' ) { i++; }` 用于统计字符串的 ______。", ["长度", "len"], "遍历到结束符即可得到字符串长度。", ["字符串", "算法"], "easy"),
        code_completion("L2C-051", "补全代码：`struct student *p = &st; printf(\"%d\", p->____);`，已知成员名为 score。", ["score"], "结构体指针访问成员需使用 `->`。", ["结构体", "指针"], "easy"),
        code_completion("L2C-052", "补全代码：`int *p = a; printf(\"%d\", *(p+____));`，若要输出第三个元素，应填写：", ["2"], "首元素偏移 2 对应第三个元素。", ["指针", "数组"], "medium"),
        subjective("L2C-053", "bug_fix", "某程序定义 `char name[5]; scanf(\"%s\", name);`，请说明该写法的主要风险并给出修正思路。", "风险是输入超长字符串会导致缓冲区溢出。应限制输入长度或改用更安全的输入方式。", [rubric_item("指出缓冲区溢出风险", ["溢出", "越界"], 4), rubric_item("提出限制长度", ["限制长度", "%4s", "宽度"], 3), rubric_item("提出更安全的输入方案", ["fgets", "安全"], 3)], ["字符串", "安全"], "medium"),
        subjective("L2C-054", "bug_fix", "某函数中定义了局部数组 `int a[10];`，随后将 `return a;` 作为返回值。说明问题所在。", "局部数组在函数结束后生命周期结束，返回其地址会成为悬空地址。", [rubric_item("指出局部对象生命周期结束", ["生命周期", "局部"], 4), rubric_item("指出返回地址无效", ["悬空", "无效地址"], 4), rubric_item("给出改进方向", ["静态", "动态内存", "参数传出"], 2)], ["函数", "内存"], "hard"),
        subjective("L2C-055", "bug_fix", "循环中把数组写成 `for(i=1;i<=n;i++) scanf(\"%d\", &a[i]);`，若数组长度为 n，请指出边界问题。", "若数组按 C 语言惯例定义为长度 n，则合法下标是 0 到 n-1，该循环会漏掉 a[0] 并越界访问 a[n]。", [rubric_item("指出下标从 0 开始", ["0", "下标"], 3), rubric_item("指出会越界访问 a[n]", ["a[n]", "越界"], 4), rubric_item("指出漏掉 a[0]", ["a[0]", "漏掉"], 3)], ["数组", "边界"], "medium"),
        subjective("L2C-056", "bug_fix", "有代码 `if(x = 0) printf(\"zero\");`，请说明错误原因及正确写法。", "这里把比较误写成赋值，导致条件表达式结果取决于赋值结果，应写为 `if(x == 0)`。", [rubric_item("指出赋值与比较混淆", ["赋值", "比较"], 4), rubric_item("给出正确写法 x==0", ["==", "x==0"], 4), rubric_item("说明原表达式含义", ["条件结果", "赋值结果"], 2)], ["运算", "常见错误"], "easy"),
        subjective("L2C-057", "short_answer", "简述指针与数组之间的联系和区别。", "应提到数组名常退化为首元素地址、指针可指向不同对象、数组大小固定且不是可赋值左值等。", [rubric_item("数组名常退化为首元素地址", ["首元素地址", "退化"], 4), rubric_item("指针可重新指向其他对象", ["重新指向", "地址"], 3), rubric_item("数组大小固定或数组名不可赋值", ["固定", "不可赋值"], 3)], ["数组", "指针"], "medium"),
        subjective("L2C-058", "short_answer", "说明为什么函数原型声明对大型 C 程序很重要。", "应说明它有助于类型检查、模块协作、接口约束和减少隐式声明带来的错误。", [rubric_item("类型检查", ["类型检查", "参数类型"], 3), rubric_item("模块间接口约束", ["接口", "模块"], 4), rubric_item("减少声明错误", ["隐式声明", "错误"], 3)], ["函数", "工程化"], "medium"),
        subjective("L2C-059", "programming", "说明设计一个函数 `int is_prime(int n)` 的核心思路。", "应提到小于 2 的处理、遍历可能因子、找到整除即返回假、遍历结束返回真。", [rubric_item("处理 n<2", ["n<2", "小于2"], 2), rubric_item("遍历可能因子", ["遍历", "因子"], 3), rubric_item("判断整除", ["整除", "%"], 3), rubric_item("正确返回结果", ["返回", "真", "假"], 2)], ["程序设计", "函数"], "medium"),
        subjective("L2C-060", "programming", "给定 10 个整数，说明如何统计最大值、最小值和平均值。", "应包括初始化、遍历比较更新、累计求和、最终求平均。", [rubric_item("初始化最大最小值", ["初始化", "最大", "最小"], 2), rubric_item("遍历并更新", ["遍历", "更新"], 3), rubric_item("累计求和", ["求和", "累计"], 3), rubric_item("求平均值", ["平均", "除以"], 2)], ["程序设计", "数组"], "easy"),
        subjective("L2C-061", "programming", "设计思路：将一个字符串逆序输出。请写出主要步骤。", "应包含求长度、首尾交换或逆序遍历、结束条件与字符串结束符处理。", [rubric_item("先求长度", ["长度", "strlen"], 2), rubric_item("首尾交换或逆序遍历", ["交换", "逆序"], 4), rubric_item("处理结束条件", ["结束", "条件"], 2), rubric_item("考虑结束符", ["结束符", "\\0"], 2)], ["程序设计", "字符串"], "medium"),
        subjective("L2C-062", "programming", "说明如何把学生成绩记录写入文本文件，并在写入结束后安全关闭文件。", "应包括 fopen、判空、按格式输出、fclose 等步骤。", [rubric_item("打开文件", ["fopen", "打开"], 3), rubric_item("判断打开是否成功", ["NULL", "判空"], 2), rubric_item("写入内容", ["fprintf", "写入"], 3), rubric_item("关闭文件", ["fclose", "关闭"], 2)], ["程序设计", "文件"], "medium"),
    ])
    questions.extend(
        build_level2_c_high_frequency_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_problem_solving_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_bug_trap_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_comprehensive_programming_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_file_linkedlist_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_string_file_advanced_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_pointer_algorithm_advanced_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_recursion_matrix_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_structure_memory_project_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_sort_search_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    questions.extend(
        build_level2_c_file_structure_case_pack(
            single_choice,
            fill_blank,
            code_completion,
            subjective,
            rubric_item,
        )
    )
    annotate_bank_questions(
        questions,
        high_frequency_ids={
            "L2C-009", "L2C-010", "L2C-015", "L2C-017", "L2C-019", "L2C-020",
            "L2C-021", "L2C-022", "L2C-023", "L2C-024", "L2C-027", "L2C-028",
            "L2C-029", "L2C-031", "L2C-032", "L2C-035", "L2C-040", "L2C-042",
            "L2C-043", "L2C-044", "L2C-047", "L2C-050", "L2C-053", "L2C-054",
            "L2C-055", "L2C-056", "L2C-057", "L2C-058", "L2C-059", "L2C-060",
            "L2C-061", "L2C-062",
            *{f"L2C-{i:03d}" for i in range(63, 421)},
        },
    )
    return {
        "subject_code": "level2_c",
        "subject_name": "二级 C 语言程序设计",
        "default_blueprint": {
            "duration_minutes": 120,
            "quotas": [
                {"type": "single_choice", "count": 20, "high_frequency_target": 12},
                {"type": "fill_blank", "count": 4, "high_frequency_target": 2},
                {"type": "code_completion", "count": 3, "high_frequency_target": 2},
                {"type": "bug_fix", "count": 2, "high_frequency_target": 1},
                {"type": "programming", "count": 1, "high_frequency_target": 1},
            ],
        },
        "questions": questions,
    }


def main():
    banks = [
        build_level1_office_bank(),
        build_level2_c_bank(),
        build_level2_python_bank(),
        build_level3_network_bank(),
        build_level4_network_engineer_bank(),
    ]

    subjects = []
    for bank in banks:
        bank_file = f"{bank['subject_code']}.json"
        high_frequency_count = sum(1 for question in bank["questions"] if question.get("frequency") == "high")
        topic_counter = Counter(question.get("topic") for question in bank["questions"] if question.get("topic"))
        top_topics = [topic for topic, _ in topic_counter.most_common(10)]
        subjects.append(
            {
                "code": bank["subject_code"],
                "name": bank["subject_name"],
                "level": bank["subject_name"][:2],
                "description": {
                    "level1_office": "覆盖办公软件与信息技术基础的入门训练题库。",
                    "level2_c": "内置覆盖 C 语言核心考点的重点题库，支持系统组卷与 AI 辅助讲评。",
                    "level2_python": "覆盖 Python 基础、文件、函数与程序设计的入门到中级练习。",
                    "level3_network": "覆盖网络基础、协议、安全与设备分工的训练题库。",
                    "level4_network_engineer": "覆盖网络工程、监控、变更与高可用场景的进阶题库。",
                }[bank["subject_code"]],
                "completeness": "broad" if bank["subject_code"] == "level2_c" else "starter",
                "bank_file": bank_file,
                "question_count": len(bank["questions"]),
                "high_frequency_question_count": high_frequency_count,
                "top_topics": top_topics[:10],
                "default_blueprint": bank["default_blueprint"],
            }
        )
        write_json(QUESTION_BANK_DIR / bank_file, bank)

    resources = [
        {"title": "二级 C 语言程序设计考试大纲（2025 年版）", "type": "official", "url": "https://ncre.neea.edu.cn/res/Home/2412/220876da81ad5d5657c599c68f81e8e9.pdf", "note": "用于核对考试范围与能力要求。"},
        {"title": "二级 C 语言程序设计样题及参考答案", "type": "official", "url": "https://ncre.neea.edu.cn/res/Home/2501/df07c4d26912fdac5b34a8496544c4ba.pdf", "note": "用于理解题型和作答形式。"},
        {"title": "全国计算机等级考试科目设置说明", "type": "official", "url": "https://ncre.neea.edu.cn/xhtml1/report/2412/138-1.htm", "note": "用于确认不同等级与科目分类。"},
        {"title": "OpenAI API Key 管理页", "type": "official", "url": "https://platform.openai.com/settings/organization/api-keys", "note": "用于获取或管理官方 OpenAI API Key。"},
        {"title": "OpenAI Structured Outputs 指南", "type": "official", "url": "https://platform.openai.com/docs/guides/structured-outputs", "note": "用于对接 JSON 结构化输出。"},
    ]

    write_json(DATA_DIR / "subjects.json", subjects)
    write_json(DATA_DIR / "resources.json", resources)
    print(f"Generated {len(subjects)} subject manifests and question banks.")


if __name__ == "__main__":
    main()
