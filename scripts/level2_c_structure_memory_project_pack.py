from __future__ import annotations


def _tag(question, topic: str, frequency: str = "high") -> dict:
    question["topic"] = topic
    question["frequency"] = frequency
    question["source"] = "curated"
    return question


def build_level2_c_structure_memory_project_pack(single_choice, fill_blank, code_completion, subjective, rubric_item):
    return [
        _tag(single_choice("L2C-331", "若要用结构体表示学生信息，学号、姓名、成绩通常作为结构体的：", ["A. 头文件", "B. 成员", "C. 宏参数", "D. 进程"], "B", "结构体的核心作用是把同类相关数据组织成一个整体。", ["高频", "结构体", "基础"], "easy"), "结构体"),
        _tag(single_choice("L2C-332", "在动态申请结构体数组后，若希望所有成绩初值为 0，更常见的函数是：", ["A. malloc", "B. calloc", "C. strcpy", "D. fopen"], "B", "calloc 申请后通常会把空间清零。", ["高频", "动态内存", "结构体"], "medium"), "动态内存"),
        _tag(single_choice("L2C-333", "若要按成绩从高到低排列结构体数组，排序时比较的通常是：", ["A. 结构体地址", "B. 成员 score", "C. 文件长度", "D. 数组下标奇偶性"], "B", "结构体排序的关键是明确比较字段。", ["高频", "结构体", "排序"], "easy"), "结构体"),
        _tag(single_choice("L2C-334", "若程序通过 `malloc` 申请了一个链表头结点但未再使用，该头结点不再需要时应：", ["A. 忽略即可", "B. free 释放", "C. fwrite 到文件", "D. 改成局部变量"], "B", "不再使用的动态内存应及时释放。", ["高频", "动态内存", "链表"], "easy"), "动态内存"),
        _tag(single_choice("L2C-335", "若结构体中包含字符数组 name[20]，输入姓名时更稳妥的做法通常是：", ["A. gets(name)", "B. fgets(name, 20, stdin)", "C. free(name)", "D. rewind(name)"], "B", "相比 gets，fgets 可限制长度。", ["高频", "结构体", "字符串"], "easy"), "结构体"),
        _tag(single_choice("L2C-336", "在顺序存储的学生结构体数组中查找最高分学生，最直接的算法通常是：", ["A. 顺序扫描", "B. 哈希删除", "C. 只看第一个元素", "D. 一定先写入文件"], "A", "未排序场景下直接线性扫描最直接。", ["高频", "结构体", "算法"], "easy"), "结构体"),
        _tag(single_choice("L2C-337", "若删除链表中间结点，需要特别注意的是：", ["A. 修改相邻指针并释放该结点", "B. 只修改数据域，不改指针", "C. 只关文件格式", "D. 只改头结点"], "A", "链表删除本质是改链接再释放空间。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(single_choice("L2C-338", "若动态申请的整型数组长度由用户输入决定，则长度变量 n 最合理的用途是：", ["A. 决定排序方向和申请空间大小", "B. 只用于 printf", "C. 只用于文件名", "D. 完全不用"], "A", "n 通常参与空间申请、循环边界等逻辑。", ["高频", "动态内存", "数组"], "easy"), "动态内存"),
        _tag(single_choice("L2C-339", "若结构体变量 stu 需要整体赋值给另一个同类型变量 tmp，C 语言中：", ["A. 通常允许直接赋值", "B. 一定要逐成员手写赋值", "C. 只能在文件中操作", "D. 一定编译失败"], "A", "同类型结构体变量通常支持整体赋值。", ["高频", "结构体", "基础"], "medium"), "结构体"),
        _tag(single_choice("L2C-340", "若程序要构造学生链表并保持按成绩降序，插入新结点时更关键的是：", ["A. 找到合适插入位置", "B. 删除全部旧结点", "C. 只改文件扩展名", "D. 只用递归"], "A", "有序链表插入的核心是定位插入位置。", ["高频", "链表", "结构体"], "hard"), "结构体"),

        _tag(fill_blank("L2C-341", "若结构体指针 p 指向学生结点，访问其成绩成员常写作 `p->______`。", ["score"], "结构体指针访问成员的基本语法。", ["高频", "结构体", "指针"], "easy"), "结构体"),
        _tag(fill_blank("L2C-342", "动态内存使用结束后应调用 ______ 释放申请到的空间。", ["free"], "malloc/calloc/free 是固定组合考点。", ["高频", "动态内存", "基础"], "easy"), "动态内存"),
        _tag(fill_blank("L2C-343", "若要在链表尾部增加新结点，通常需要先找到当前的尾 ______。", ["结点"], "链表尾插基础步骤。", ["高频", "链表", "结构体"], "easy"), "结构体"),
        _tag(fill_blank("L2C-344", "若结构体数组 `stu` 有 n 个元素，要遍历全部元素，循环边界常写为 `i < ______`。", ["n"], "结构体数组遍历与普通数组一致。", ["高频", "结构体", "数组"], "easy"), "结构体"),
        _tag(fill_blank("L2C-345", "若链表已经为空，头指针通常为 ______。", ["NULL"], "空链表判定基础点。", ["高频", "链表", "基础"], "easy"), "结构体"),
        _tag(fill_blank("L2C-346", "若要用动态内存存放 30 个学生结构体，申请空间的元素个数通常写成 ______。", ["30"], "申请结构体数组时元素个数是基础参数。", ["高频", "动态内存", "结构体"], "easy"), "动态内存"),

        _tag(code_completion("L2C-347", "补全代码：`stu = (struct student*)malloc(sizeof(struct student) * n); if(stu == NULL) return ____;`，设函数返回 int。", ["0", "-1"], "动态内存判空后的错误返回模板。", ["高频", "动态内存", "结构体"], "easy"), "动态内存"),
        _tag(code_completion("L2C-348", "补全代码：`for(i=0;i<n;i++) if(stu[i].score > max){ max = stu[i].score; pos = ____; }`", ["i"], "查找最高分学生时需要同步保存位置。", ["高频", "结构体", "程序设计"], "easy"), "结构体"),
        _tag(code_completion("L2C-349", "补全代码：`struct node *p = head; while(p->next != NULL) p = p->____;`", ["next"], "链表尾插前定位尾结点。", ["高频", "链表", "结构体"], "easy"), "结构体"),
        _tag(code_completion("L2C-350", "补全代码：`newnode = (struct node*)malloc(sizeof(struct node)); newnode->next = head; head = ______;`", ["newnode"], "头插法构造链表的标准模板。", ["高频", "链表", "结构体"], "easy"), "结构体"),
        _tag(code_completion("L2C-351", "补全代码：`q = p->next; p->next = q->next; free(q); q = ______;`", ["NULL"], "删除后置空是常见良好习惯。", ["高频", "链表", "动态内存"], "medium"), "动态内存"),
        _tag(code_completion("L2C-352", "补全代码：`for(i=0;i<n-1;i++) for(j=0;j<n-1-i;j++) if(stu[j].score < stu[j+1].score){ t = stu[j]; stu[j] = stu[j+1]; stu[j+1] = ____; }`", ["t"], "结构体数组按成绩排序的基础交换模板。", ["高频", "结构体", "排序"], "medium"), "结构体"),

        _tag(subjective("L2C-353", "bug_fix", "某程序对 `malloc` 返回值未判空，就直接访问 `stu[i]`。请说明风险。", "申请失败时返回 NULL，继续访问会导致非法内存访问或崩溃。", [rubric_item("指出未判空", ["判空", "NULL"], 4), rubric_item("指出非法访问风险", ["非法访问", "崩溃"], 4), rubric_item("提出先判断后使用", ["先判断"], 2)], ["高频", "动态内存", "bug_fix"], "medium"), "动态内存"),
        _tag(subjective("L2C-354", "bug_fix", "某程序删除链表首结点时先 `free(head)`，再写 `head = head->next;`。请说明问题。", "释放头结点后再访问它的 next 属于使用已释放内存，应先保存后继。", [rubric_item("指出释放后再访问错误", ["释放后", "访问"], 5), rubric_item("指出属于已释放内存使用", ["已释放"], 3), rubric_item("提出先保存 next 再 free", ["先保存", "next"], 2)], ["高频", "链表", "bug_fix"], "hard"), "结构体"),
        _tag(subjective("L2C-355", "bug_fix", "某程序将姓名读入 `char name[8]` 时直接使用 `%s`，且可能输入超长姓名。请说明问题。", "未限制输入长度会导致缓冲区溢出，应限制宽度或用 fgets。", [rubric_item("指出长度未限制", ["未限制", "宽度"], 4), rubric_item("指出缓冲区溢出", ["溢出"], 4), rubric_item("提出更安全输入方式", ["fgets", "%7s"], 2)], ["高频", "结构体", "bug_fix"], "medium"), "结构体"),
        _tag(subjective("L2C-356", "bug_fix", "某程序释放结构体数组后仍继续使用其中成员值。请说明问题。", "释放后的内存不再归程序安全使用，继续访问属于悬空访问。", [rubric_item("指出释放后不可继续使用", ["释放后", "不可使用"], 5), rubric_item("指出悬空访问风险", ["悬空", "非法"], 3), rubric_item("提出置空或重新申请", ["置空", "重新申请"], 2)], ["高频", "动态内存", "bug_fix"], "medium"), "动态内存"),

        _tag(subjective("L2C-357", "programming", "说明如何编写函数，统计学生结构体数组中及格人数和平均成绩。", "应包含遍历数组、判断是否及格、累计总分和人数、最后计算平均值。", [rubric_item("遍历结构体数组", ["遍历"], 2), rubric_item("统计及格人数", ["及格", "人数"], 3), rubric_item("累计总分", ["总分"], 2), rubric_item("计算平均成绩", ["平均"], 3)], ["高频", "程序设计", "结构体"], "medium"), "程序设计"),
        _tag(subjective("L2C-358", "programming", "说明如何用头插法建立一个单链表。", "应包含循环创建新结点、给新结点赋值、让其 next 指向当前头结点、更新头指针。", [rubric_item("创建新结点", ["创建", "malloc"], 2), rubric_item("新结点 next 指向当前头", ["next", "头结点"], 4), rubric_item("更新头指针", ["更新头指针"], 2), rubric_item("循环处理多个数据", ["循环"], 2)], ["高频", "程序设计", "链表"], "hard"), "程序设计"),
        _tag(subjective("L2C-359", "programming", "说明如何动态申请一个长度为 n 的整数数组并求其中最大值。", "应包含申请空间、判空、读入元素、遍历比较、释放空间。", [rubric_item("申请并判空", ["申请", "判空"], 3), rubric_item("读入元素", ["读入"], 2), rubric_item("遍历求最大值", ["最大值", "遍历"], 3), rubric_item("释放空间", ["释放"], 2)], ["高频", "程序设计", "动态内存"], "medium"), "程序设计"),
        _tag(subjective("L2C-360", "programming", "说明如何编写函数，按成绩降序删除链表中所有不及格学生结点后输出剩余链表。", "应包含遍历链表、判断成绩、正确处理头结点与中间结点删除、最后遍历输出。", [rubric_item("遍历链表", ["遍历"], 2), rubric_item("判断不及格并删除", ["不及格", "删除"], 3), rubric_item("正确处理头结点和中间结点", ["头结点", "中间结点"], 3), rubric_item("输出剩余链表", ["输出"], 2)], ["高频", "程序设计", "链表"], "hard"), "程序设计"),
    ]
