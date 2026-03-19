from __future__ import annotations


def rubric_item(description, keywords, points):
    return {"description": description, "keywords": keywords, "points": points}


def starter_subject(subject_code, subject_name, quotas, questions):
    return {
        "subject_code": subject_code,
        "subject_name": subject_name,
        "default_blueprint": {"duration_minutes": 45, "quotas": quotas},
        "questions": questions,
    }


def sc(single_choice, qid, stem, options, answer, analysis, tags, difficulty="easy", score=2):
    return single_choice(qid, stem, options, answer, analysis, tags, difficulty, score)


def fb(fill_blank, qid, stem, answers, analysis, tags, difficulty="easy", score=5):
    return fill_blank(qid, stem, answers, analysis, tags, difficulty, score)


def cc(code_completion, qid, stem, answers, analysis, tags, difficulty="easy", score=5):
    return code_completion(qid, stem, answers, analysis, tags, difficulty, score)


def subj(subjective, qid, qtype, stem, analysis, rubric, tags, difficulty="medium", score=10):
    return subjective(qid, qtype, stem, analysis, rubric, tags, difficulty, score)


def build_level1_wps_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L1WPS-001", "在 WPS 文字中快速复制格式，常用工具是：", ["A. 格式刷", "B. 邮件合并", "C. 分栏", "D. 批注"], "A", "格式刷用于复制并应用已有格式。", ["WPS", "文字"]),
        sc(single_choice, "L1WPS-002", "WPS 表格中用于求和的函数通常是：", ["A. MAX", "B. SUM", "C. IF", "D. LEN"], "B", "SUM 是基础求和函数。", ["WPS", "表格"]),
        sc(single_choice, "L1WPS-003", "WPS 演示中让对象逐个出现，主要设置：", ["A. 动画", "B. 打印", "C. 页脚", "D. 拼写"], "A", "演示对象出现顺序通过动画设置控制。", ["WPS", "演示"]),
        sc(single_choice, "L1WPS-004", "WPS 云文档的主要价值之一是：", ["A. 自动关机", "B. 多端同步", "C. 只读模式", "D. 固定字体"], "B", "云文档可支持多端查看和同步。", ["WPS", "云文档"]),
        fb(fill_blank, "L1WPS-005", "WPS 表格中用于返回平均值的函数是 ______。", ["AVERAGE"], "AVERAGE 用于平均值统计。", ["WPS", "函数"]),
        fb(fill_blank, "L1WPS-006", "WPS 文字默认文档扩展名通常是 ______。", [".wps", "wps"], "WPS 文字传统格式扩展名为 wps。", ["WPS", "文件"]),
        subj(subjective, "L1WPS-007", "short_answer", "说明制作一份规范的 WPS 演示文稿时至少应注意的三项原则。", "应包含层级清晰、视觉统一、留白合理等。", [rubric_item("层级清晰", ["层级", "标题"], 3), rubric_item("视觉统一", ["统一", "配色", "字体"], 3), rubric_item("留白或对齐", ["留白", "对齐"], 4)], ["WPS", "演示"]),
    ]
    return starter_subject("level1_wps", "一级计算机基础及WPS Office应用", [{"type": "single_choice", "count": 4}, {"type": "fill_blank", "count": 2}, {"type": "short_answer", "count": 1}], questions)


def build_level1_photoshop_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L1PS-001", "Photoshop 中用于选取图像局部区域的基础工具是：", ["A. 画笔", "B. 选框工具", "C. 吸管", "D. 橡皮擦"], "B", "选框工具用于建立规则选区。", ["Photoshop", "选区"]),
        sc(single_choice, "L1PS-002", "图层的主要作用之一是：", ["A. 降低分辨率", "B. 分层编辑", "C. 锁定系统", "D. 自动存档"], "B", "图层便于独立编辑不同图像元素。", ["Photoshop", "图层"]),
        sc(single_choice, "L1PS-003", "若要撤销上一步操作，常用快捷键是：", ["A. Ctrl+S", "B. Ctrl+Z", "C. Ctrl+P", "D. Ctrl+N"], "B", "Ctrl+Z 是常见撤销操作。", ["Photoshop", "快捷键"]),
        sc(single_choice, "L1PS-004", "用于调整图像亮度、对比度的功能通常属于：", ["A. 图像调整", "B. 3D 设置", "C. 视频时间轴", "D. 字体安装"], "A", "亮度、对比度属于常见图像调整。", ["Photoshop", "调整"]),
        fb(fill_blank, "L1PS-005", "用于去除图像局部瑕疵的常用工具之一是 ______ 画笔。", ["修复", "修补"], "修复类工具可处理污点和瑕疵。", ["Photoshop", "修图"]),
        fb(fill_blank, "L1PS-006", "Photoshop 源文件常见扩展名是 ______。", [".psd", "psd"], "PSD 是常见工程源文件格式。", ["Photoshop", "文件"]),
        subj(subjective, "L1PS-007", "short_answer", "说明制作海报时为什么需要合理使用图层和文字样式。", "应说明便于分层编辑、后续修改和增强视觉层级。", [rubric_item("分层编辑", ["图层", "分层"], 4), rubric_item("便于修改", ["修改", "调整"], 3), rubric_item("增强视觉层级", ["层级", "文字样式"], 3)], ["Photoshop", "设计"]),
    ]
    return starter_subject("level1_photoshop", "一级计算机基础及Photoshop应用", [{"type": "single_choice", "count": 4}, {"type": "fill_blank", "count": 2}, {"type": "short_answer", "count": 1}], questions)


def build_level1_network_security_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L1SEC-001", "以下哪项更符合强密码要求？", ["A. 123456", "B. password", "C. A1!m7Qz9", "D. birthday"], "C", "强密码通常包含多类字符且避免明显规律。", ["网络安全", "密码"]),
        sc(single_choice, "L1SEC-002", "钓鱼邮件最常见的风险是：", ["A. 自动升级内存", "B. 骗取账号密码", "C. 提高网速", "D. 修复漏洞"], "B", "钓鱼邮件常诱导泄露敏感信息。", ["网络安全", "邮件"]),
        sc(single_choice, "L1SEC-003", "双重认证的主要价值是：", ["A. 减少分辨率", "B. 增加额外身份校验", "C. 关闭防火墙", "D. 取消密码"], "B", "双重认证能提高账户安全性。", ["网络安全", "认证"]),
        sc(single_choice, "L1SEC-004", "公共 Wi-Fi 下更需要注意的是：", ["A. 随意输入支付信息", "B. 核对网络并避免敏感操作", "C. 关闭系统更新", "D. 只看视频"], "B", "公共网络中应提高风险意识。", ["网络安全", "公共网络"]),
        fb(fill_blank, "L1SEC-005", "防火墙的主要作用之一是对网络 ______ 进行控制。", ["访问", "流量"], "防火墙用于访问和流量控制。", ["网络安全", "防火墙"]),
        fb(fill_blank, "L1SEC-006", "软件及时安装安全 ______ 可以降低漏洞风险。", ["补丁"], "补丁管理是基础安全措施。", ["网络安全", "补丁"]),
        subj(subjective, "L1SEC-007", "short_answer", "说明为什么企业或个人应定期备份重要数据。", "应说明防止误删、勒索、设备损坏和便于恢复。", [rubric_item("防止误删损失", ["误删"], 3), rubric_item("应对勒索或损坏", ["勒索", "损坏"], 4), rubric_item("便于恢复", ["恢复"], 3)], ["网络安全", "备份"]),
    ]
    return starter_subject("level1_network_security", "一级网络安全素质教育", [{"type": "single_choice", "count": 4}, {"type": "fill_blank", "count": 2}, {"type": "short_answer", "count": 1}], questions)


def build_level1_ai_foundation_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L1AI-001", "生成式 AI 的一个常见能力是：", ["A. 只做硬件维修", "B. 根据提示生成文本或图像", "C. 替代电源", "D. 固定网络拓扑"], "B", "生成式 AI 常根据提示生成内容。", ["人工智能", "生成式AI"]),
        sc(single_choice, "L1AI-002", "提示词优化的主要目标之一是：", ["A. 降低屏幕亮度", "B. 让模型输出更符合需求", "C. 删除文件系统", "D. 禁用输入法"], "B", "清晰提示可提升输出质量。", ["人工智能", "提示词"]),
        sc(single_choice, "L1AI-003", "在使用大模型时，以下更重要的是：", ["A. 盲目信任输出", "B. 结合事实核验结果", "C. 不做任何检查", "D. 永远离线"], "B", "模型输出可能有误，应结合核验。", ["人工智能", "应用"]),
        sc(single_choice, "L1AI-004", "以下哪项更符合 AI 使用伦理？", ["A. 伪造身份信息", "B. 明确标注 AI 辅助内容", "C. 批量传播谣言", "D. 泄露隐私"], "B", "透明标注更符合规范使用。", ["人工智能", "伦理"]),
        fb(fill_blank, "L1AI-005", "大模型输出前常基于用户输入形成的文本称为 ______。", ["提示词", "prompt"], "提示词是引导模型输出的关键输入。", ["人工智能", "提示词"]),
        fb(fill_blank, "L1AI-006", "在 AI 使用中，对输出进行事实 ______ 是重要步骤。", ["核验", "校验"], "核验有助于降低错误传播。", ["人工智能", "事实核验"]),
        subj(subjective, "L1AI-007", "short_answer", "说明在学习或办公中使用大模型时，为什么仍需要人工复核。", "应说明可能幻觉、上下文偏差和责任归属。", [rubric_item("模型可能出错", ["错误", "幻觉"], 4), rubric_item("需要人工判断", ["人工", "判断"], 3), rubric_item("涉及责任和准确性", ["责任", "准确性"], 3)], ["人工智能", "应用"]),
    ]
    return starter_subject("level1_ai_foundation", "一级人工智能与大模型基础", [{"type": "single_choice", "count": 4}, {"type": "fill_blank", "count": 2}, {"type": "short_answer", "count": 1}], questions)


def build_level2_java_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L2JAVA-001", "Java 中定义类的关键字是：", ["A. class", "B. struct", "C. func", "D. typedef"], "A", "Java 用 class 定义类。", ["Java", "基础"]),
        sc(single_choice, "L2JAVA-002", "Java 程序入口方法通常是：", ["A. init", "B. main", "C. runApp", "D. execute"], "B", "main 是常见入口方法。", ["Java", "基础"]),
        sc(single_choice, "L2JAVA-003", "以下更符合面向对象特征的是：", ["A. 封装", "B. 线性表", "C. 端口映射", "D. 进制转换"], "A", "面向对象通常强调封装、继承、多态。", ["Java", "面向对象"]),
        fb(fill_blank, "L2JAVA-004", "用于输出一行文本的常见语句是 `System.out.______`。", ["println"], "println 常用于输出并换行。", ["Java", "输出"]),
        cc(code_completion, "L2JAVA-005", "补全代码：`for(int i=0; i<10; i++){ sum += ______; }`，若要求把 i 累加到 sum。", ["i"], "基础循环累加模板。", ["Java", "循环"]),
        subj(subjective, "L2JAVA-006", "bug_fix", "说明为什么在 Java 中访问数组元素时需要注意下标边界。", "应指出越界会触发运行时异常。", [rubric_item("下标范围有限", ["下标", "范围"], 3), rubric_item("越界会异常", ["越界", "异常"], 5), rubric_item("应先判断长度", ["长度", "判断"], 2)], ["Java", "数组"]),
        subj(subjective, "L2JAVA-007", "programming", "说明如何编写 Java 方法，统计数组中偶数个数。", "应包含遍历数组、判断偶数、计数累加和返回值。", [rubric_item("遍历数组", ["遍历"], 2), rubric_item("判断偶数", ["偶数", "%2"], 3), rubric_item("计数累加", ["计数"], 3), rubric_item("返回结果", ["返回"], 2)], ["Java", "程序设计"]),
    ]
    return starter_subject("level2_java", "二级Java语言程序设计", [{"type": "single_choice", "count": 3}, {"type": "fill_blank", "count": 1}, {"type": "bug_fix", "count": 1}, {"type": "programming", "count": 1}], questions)


def build_level2_access_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L2ACCESS-001", "Access 中用于保存数据的基础对象通常是：", ["A. 表", "B. 幻灯片", "C. 页脚", "D. 编译器"], "A", "表是数据库记录的基础载体。", ["Access", "数据库"]),
        sc(single_choice, "L2ACCESS-002", "主键的主要作用是：", ["A. 重复标识记录", "B. 唯一标识记录", "C. 只用于打印", "D. 只存图片"], "B", "主键用于唯一标识一条记录。", ["Access", "主键"]),
        sc(single_choice, "L2ACCESS-003", "查询的主要作用之一是：", ["A. 检索满足条件的数据", "B. 关闭数据库", "C. 修改显示器", "D. 删除系统"], "A", "查询用于数据检索和筛选。", ["Access", "查询"]),
        fb(fill_blank, "L2ACCESS-004", "在数据库关系设计中，描述实体联系的常见模型是 ______ 模型。", ["E-R", "ER"], "E-R 模型用于概念设计。", ["Access", "设计"]),
        cc(code_completion, "L2ACCESS-005", "补全 SQL：`SELECT * FROM Student WHERE score > ______;`，若要求查询成绩大于 60 的记录。", ["60"], "基础条件查询模板。", ["Access", "SQL"]),
        subj(subjective, "L2ACCESS-006", "short_answer", "说明为什么设计表结构时要避免同一数据在多处重复存储。", "应涉及冗余、更新异常和一致性问题。", [rubric_item("减少冗余", ["冗余"], 3), rubric_item("避免更新异常", ["更新异常"], 4), rubric_item("保持一致性", ["一致性"], 3)], ["Access", "规范化"]),
        subj(subjective, "L2ACCESS-007", "programming", "说明如何设计学生成绩管理数据库的基本步骤。", "应包含表设计、字段设计、主键设置、关系设计和查询。", [rubric_item("设计表和字段", ["表", "字段"], 4), rubric_item("设置主键", ["主键"], 2), rubric_item("设计关系或查询", ["关系", "查询"], 4)], ["Access", "程序设计"]),
    ]
    return starter_subject("level2_access", "二级Access数据库程序设计", [{"type": "single_choice", "count": 3}, {"type": "fill_blank", "count": 1}, {"type": "short_answer", "count": 1}, {"type": "programming", "count": 1}], questions)


def build_level2_cpp_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L2CPP-001", "C++ 中用于定义类的关键字是：", ["A. class", "B. module", "C. import", "D. package"], "A", "C++ 中类使用 class 定义。", ["C++", "类"]),
        sc(single_choice, "L2CPP-002", "C++ 中引用的符号通常是：", ["A. *", "B. &", "C. ->", "D. %"], "B", "引用声明通常使用 &。", ["C++", "引用"]),
        sc(single_choice, "L2CPP-003", "构造函数的主要作用是：", ["A. 对象初始化", "B. 删除文件", "C. 强制退出", "D. 列表排序"], "A", "构造函数常用于对象创建时初始化。", ["C++", "构造函数"]),
        fb(fill_blank, "L2CPP-004", "用于输出到标准输出流的对象通常是 ______。", ["cout"], "cout 是常见输出流对象。", ["C++", "输出"]),
        cc(code_completion, "L2CPP-005", "补全代码：`for(int i=0;i<n;i++) sum += a[____];`", ["i"], "数组遍历求和模板。", ["C++", "循环"]),
        subj(subjective, "L2CPP-006", "bug_fix", "说明为什么动态申请内存后需要及时释放。", "应指出内存泄漏和资源占用问题。", [rubric_item("释放资源", ["释放", "资源"], 3), rubric_item("避免内存泄漏", ["内存泄漏"], 5), rubric_item("保持程序稳定", ["稳定"], 2)], ["C++", "内存"]),
        subj(subjective, "L2CPP-007", "programming", "说明如何编写 C++ 函数，找出数组中的最大值。", "应包含遍历、比较更新和返回结果。", [rubric_item("遍历数组", ["遍历"], 3), rubric_item("比较更新", ["比较", "更新"], 4), rubric_item("返回最大值", ["返回"], 3)], ["C++", "程序设计"]),
    ]
    return starter_subject("level2_cpp", "二级C++语言程序设计", [{"type": "single_choice", "count": 3}, {"type": "fill_blank", "count": 1}, {"type": "bug_fix", "count": 1}, {"type": "programming", "count": 1}], questions)


def build_level2_mysql_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L2MYSQL-001", "用于查询数据的 SQL 关键字通常是：", ["A. SELECT", "B. DELETE", "C. CREATE", "D. DROP"], "A", "SELECT 是基本查询语句。", ["MySQL", "SQL"]),
        sc(single_choice, "L2MYSQL-002", "用于唯一标识记录的字段通常称为：", ["A. 主键", "B. 视图", "C. 注释", "D. 主题"], "A", "主键是表中唯一标识。", ["MySQL", "主键"]),
        sc(single_choice, "L2MYSQL-003", "`WHERE` 子句的主要作用是：", ["A. 条件筛选", "B. 排序", "C. 分组", "D. 建库"], "A", "WHERE 用于条件过滤。", ["MySQL", "查询"]),
        fb(fill_blank, "L2MYSQL-004", "删除表中所有记录但保留表结构，常用语句可写为 `DELETE FROM ______`。", ["表名"], "DELETE FROM 表名是基础删除模板。", ["MySQL", "SQL"]),
        cc(code_completion, "L2MYSQL-005", "补全 SQL：`SELECT name FROM student ORDER BY score ______;`，若要求按分数降序。", ["DESC"], "DESC 表示降序。", ["MySQL", "排序"]),
        subj(subjective, "L2MYSQL-006", "short_answer", "说明为什么数据库设计中需要主键和索引。", "应涉及唯一标识、查询效率和数据一致性。", [rubric_item("唯一标识", ["唯一", "主键"], 3), rubric_item("提高查询效率", ["查询效率", "索引"], 4), rubric_item("便于关联或一致性", ["关联", "一致性"], 3)], ["MySQL", "设计"]),
        subj(subjective, "L2MYSQL-007", "programming", "说明如何查询成绩大于 80 分的学生姓名并按成绩降序显示。", "应包含 SELECT、WHERE、ORDER BY。", [rubric_item("SELECT 字段", ["SELECT"], 3), rubric_item("WHERE 条件", ["WHERE", "80"], 3), rubric_item("ORDER BY DESC", ["ORDER BY", "DESC"], 4)], ["MySQL", "程序设计"]),
    ]
    return starter_subject("level2_mysql", "二级MySQL数据库程序设计", [{"type": "single_choice", "count": 3}, {"type": "fill_blank", "count": 1}, {"type": "short_answer", "count": 1}, {"type": "programming", "count": 1}], questions)


def build_level2_web_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L2WEB-001", "HTML 中用于创建超链接的标签通常是：", ["A. <img>", "B. <a>", "C. <div>", "D. <table>"], "B", "<a> 标签用于超链接。", ["Web", "HTML"]),
        sc(single_choice, "L2WEB-002", "CSS 的主要作用通常是：", ["A. 控制页面样式", "B. 连接数据库", "C. 编译 Java", "D. 删除脚本"], "A", "CSS 用于页面表现层样式。", ["Web", "CSS"]),
        sc(single_choice, "L2WEB-003", "JavaScript 更常用于：", ["A. 客户端交互逻辑", "B. 图像压缩", "C. BIOS 设置", "D. 电源管理"], "A", "JavaScript 常用于 Web 交互。", ["Web", "JavaScript"]),
        fb(fill_blank, "L2WEB-004", "HTTP 请求中常见的提交表单方法包括 GET 和 ______。", ["POST"], "GET/POST 是基础请求方式。", ["Web", "HTTP"]),
        cc(code_completion, "L2WEB-005", "补全代码：`<input type=\"______\">`，若要求密码输入框。", ["password"], "password 类型用于密码输入。", ["Web", "表单"]),
        subj(subjective, "L2WEB-006", "short_answer", "说明为什么前端页面需要进行基本的表单校验。", "应涉及减少错误输入、改善体验和减轻后端压力。", [rubric_item("减少错误输入", ["错误输入"], 3), rubric_item("改善用户体验", ["体验"], 3), rubric_item("减轻后端压力", ["后端", "压力"], 4)], ["Web", "表单"]),
        subj(subjective, "L2WEB-007", "programming", "说明一个基础登录页通常需要包含哪些核心元素。", "应包含输入框、提交按钮、校验与反馈信息。", [rubric_item("用户名和密码输入框", ["用户名", "密码"], 4), rubric_item("提交按钮", ["按钮"], 2), rubric_item("校验或反馈", ["校验", "反馈"], 4)], ["Web", "程序设计"]),
    ]
    return starter_subject("level2_web", "二级Web程序设计", [{"type": "single_choice", "count": 3}, {"type": "fill_blank", "count": 1}, {"type": "short_answer", "count": 1}, {"type": "programming", "count": 1}], questions)


def build_level2_ms_office_advanced_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L2MSA-001", "二级 MS Office 高级应用常强调的能力之一是：", ["A. 单纯记忆菜单位置", "B. 综合办公场景处理", "C. 只会开关机", "D. 只看网页"], "B", "该科目更强调综合应用能力。", ["MS Office高级应用", "综合应用"]),
        sc(single_choice, "L2MSA-002", "在 Word 长文档处理中，样式的主要价值之一是：", ["A. 增强结构化排版", "B. 删除图片", "C. 禁用打印", "D. 关闭页面"], "A", "样式有助于统一标题和目录结构。", ["MS Office高级应用", "Word"]),
        sc(single_choice, "L2MSA-003", "在 Excel 中进行数据分析时，数据透视表常用于：", ["A. 汇总分析", "B. 画简单直线", "C. 改显示器", "D. 删除系统"], "A", "数据透视表用于汇总分析数据。", ["MS Office高级应用", "Excel"]),
        fb(fill_blank, "L2MSA-004", "PowerPoint 中用于控制对象出现次序的常见功能是 ______。", ["动画"], "动画顺序控制播放过程中的先后。", ["MS Office高级应用", "PowerPoint"]),
        cc(code_completion, "L2MSA-005", "补全函数：`=VLOOKUP(A2, $E$2:$G$20, 2, ______)`，若要求精确匹配。", ["FALSE", "0"], "精确匹配常写 FALSE 或 0。", ["MS Office高级应用", "Excel"]),
        subj(subjective, "L2MSA-006", "short_answer", "说明为什么办公自动化场景下需要兼顾文档规范、数据准确和展示效果。", "应涉及沟通效率、分析可靠性和表达质量。", [rubric_item("规范有助于沟通", ["规范", "沟通"], 3), rubric_item("数据准确很重要", ["准确"], 4), rubric_item("展示效果影响表达", ["展示", "表达"], 3)], ["MS Office高级应用", "综合应用"]),
        subj(subjective, "L2MSA-007", "programming", "说明完成一份办公综合任务通常会跨哪些 Office 组件协同。", "应涉及 Word、Excel、PowerPoint 等协作。", [rubric_item("Word 文档", ["Word"], 3), rubric_item("Excel 数据", ["Excel"], 3), rubric_item("PowerPoint 展示", ["PowerPoint"], 4)], ["MS Office高级应用", "程序设计"]),
    ]
    return starter_subject("level2_ms_office_advanced", "二级MS Office高级应用与设计", [{"type": "single_choice", "count": 3}, {"type": "fill_blank", "count": 1}, {"type": "short_answer", "count": 1}, {"type": "programming", "count": 1}], questions)


def build_level2_wps_advanced_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L2WPSA-001", "二级 WPS 高级应用强调的能力之一是：", ["A. 综合文档处理", "B. 只会打字", "C. 固定一个模板", "D. 不用表格"], "A", "该科目强调办公综合应用与设计。", ["WPS高级应用", "综合应用"]),
        sc(single_choice, "L2WPSA-002", "在 WPS 表格中，筛选和排序主要用于：", ["A. 数据整理分析", "B. 删除电源", "C. 安装驱动", "D. 控制风扇"], "A", "筛选排序是数据整理的基础。", ["WPS高级应用", "表格"]),
        sc(single_choice, "L2WPSA-003", "在 WPS 演示中版式统一的关键之一是：", ["A. 母版", "B. 回收站", "C. 任务管理器", "D. 防火墙"], "A", "母版有助于统一演示风格。", ["WPS高级应用", "演示"]),
        fb(fill_blank, "L2WPSA-004", "在 WPS 文字中自动生成目录通常依赖预先设置好的 ______。", ["样式"], "样式是目录和结构化排版基础。", ["WPS高级应用", "文字"]),
        cc(code_completion, "L2WPSA-005", "补全函数：`=SUMIF(B2:B20, \">=60\", ______)`，若要求统计 C 列对应分数。", ["C2:C20"], "SUMIF 常用于条件求和。", ["WPS高级应用", "表格"]),
        subj(subjective, "L2WPSA-006", "short_answer", "说明在 WPS 综合办公任务中，为什么模板与样式能显著提高效率。", "应涉及统一格式、减少重复劳动和便于维护。", [rubric_item("统一格式", ["统一", "格式"], 4), rubric_item("减少重复劳动", ["重复", "效率"], 3), rubric_item("便于维护", ["维护"], 3)], ["WPS高级应用", "综合应用"]),
        subj(subjective, "L2WPSA-007", "programming", "说明如何规划一份包含文字、表格和演示稿的 WPS 综合任务。", "应涉及文字撰写、数据表整理和演示汇报。", [rubric_item("文字文档", ["文字"], 3), rubric_item("表格数据", ["表格"], 3), rubric_item("演示汇报", ["演示"], 4)], ["WPS高级应用", "程序设计"]),
    ]
    return starter_subject("level2_wps_advanced", "二级WPS Office高级应用与设计", [{"type": "single_choice", "count": 3}, {"type": "fill_blank", "count": 1}, {"type": "short_answer", "count": 1}, {"type": "programming", "count": 1}], questions)


def build_level2_opengauss_bank(single_choice, fill_blank, code_completion, subjective):
    questions = [
        sc(single_choice, "L2OG-001", "openGauss 属于哪类软件平台？", ["A. 数据库管理系统", "B. 图片编辑器", "C. 浏览器", "D. 文本输入法"], "A", "openGauss 是数据库管理系统。", ["openGauss", "基础"]),
        sc(single_choice, "L2OG-002", "使用 SQL 创建表的关键字通常是：", ["A. CREATE TABLE", "B. DROP VIEW", "C. SELECT INTO", "D. OPEN FILE"], "A", "CREATE TABLE 用于建表。", ["openGauss", "SQL"]),
        sc(single_choice, "L2OG-003", "数据库中用于检索记录的语句通常是：", ["A. SELECT", "B. UPDATE", "C. DELETE", "D. ALTER"], "A", "SELECT 是基础查询语句。", ["openGauss", "SQL"]),
        fb(fill_blank, "L2OG-004", "若要修改表结构，常用 SQL 关键字是 ______。", ["ALTER"], "ALTER 常用于修改表结构。", ["openGauss", "SQL"]),
        cc(code_completion, "L2OG-005", "补全 SQL：`SELECT * FROM student WHERE score >= ______;`，若要求查询 60 分及以上记录。", ["60"], "基础条件查询模板。", ["openGauss", "查询"]),
        subj(subjective, "L2OG-006", "short_answer", "说明数据库表设计中为什么要考虑主键和数据类型。", "应涉及唯一标识、约束和数据一致性。", [rubric_item("唯一标识", ["唯一", "主键"], 3), rubric_item("数据类型合理", ["数据类型"], 3), rubric_item("约束和一致性", ["约束", "一致性"], 4)], ["openGauss", "设计"]),
        subj(subjective, "L2OG-007", "programming", "说明如何设计一个学生信息表并查询成绩前十名。", "应涉及字段设计、建表和排序查询。", [rubric_item("设计字段", ["字段", "建表"], 4), rubric_item("排序查询", ["排序", "前十"], 3), rubric_item("使用 SELECT 语句", ["SELECT"], 3)], ["openGauss", "程序设计"]),
    ]
    return starter_subject("level2_opengauss", "二级openGauss数据库程序设计", [{"type": "single_choice", "count": 3}, {"type": "fill_blank", "count": 1}, {"type": "short_answer", "count": 1}, {"type": "programming", "count": 1}], questions)
