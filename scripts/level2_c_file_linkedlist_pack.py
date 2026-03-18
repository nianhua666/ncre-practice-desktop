from __future__ import annotations


def _tag(question, topic: str, frequency: str = "high") -> dict:
    question["topic"] = topic
    question["frequency"] = frequency
    question["source"] = "curated"
    return question


def build_level2_c_file_linkedlist_pack(single_choice, fill_blank, code_completion, subjective, rubric_item):
    return [
        _tag(single_choice("L2C-211", "在链表中插入新结点时，最关键的操作之一通常是：", ["A. 修改若干指针链接关系", "B. 改变数组长度", "C. 调整文件读写位置", "D. 使用 switch"], "A", "链表插入的本质是修改指针指向关系。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(single_choice("L2C-212", "若以文本方式向文件写入一行学生信息，更常用的函数是：", ["A. fscanf", "B. fprintf", "C. getchar", "D. malloc"], "B", "fprintf 用于格式化写文件。", ["高频", "文件", "输出"], "easy"), "文件"),
        _tag(single_choice("L2C-213", "在创建单链表结点时，若用动态内存申请空间，更合理的步骤是：", ["A. 先 free 再 malloc", "B. 申请空间后先判断是否成功", "C. 申请后无需初始化 next", "D. 一定写入文件"], "B", "malloc 返回值应判空，再初始化数据域和 next 域。", ["高频", "结构体", "动态内存"], "easy"), "动态内存"),
        _tag(single_choice("L2C-214", "若要把若干结构体记录完整写入二进制文件，更常用的函数是：", ["A. fread", "B. fwrite", "C. fgets", "D. puts"], "B", "fwrite 常用于按块写入二进制数据。", ["高频", "文件", "二进制"], "medium"), "文件"),
        _tag(single_choice("L2C-215", "在单链表遍历中，常见的结束条件是当前指针：", ["A. 等于 0.0", "B. 指向头结点前一个位置", "C. 等于 NULL", "D. 等于 EOF"], "C", "链表遍历通常以空指针作为结束标志。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(single_choice("L2C-216", "若程序需要统计文件中整数的个数，较自然的思路是：", ["A. 逐个读取并计数", "B. 只读取第一行", "C. 必须先把文件删掉", "D. 只能用递归"], "A", "文件统计问题本质上是循环读取 + 累加。", ["高频", "文件", "程序设计"], "easy"), "文件"),
        _tag(single_choice("L2C-217", "链表相比顺序表更适合频繁插入删除的主要原因是：", ["A. 链表一定更省空间", "B. 插入删除不必整体移动大量元素", "C. 链表元素必须连续", "D. 链表不需要指针"], "B", "链表通过修改链接即可完成局部插入删除。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(single_choice("L2C-218", "若程序把结构体数组写入文件后立刻退出却忘记关闭文件，主要风险之一是：", ["A. 文件内容可能没有完整刷新", "B. 程序自动更快", "C. 结构体自动排序", "D. 指针自动置空"], "A", "未关闭文件可能导致缓冲区未完全刷新。", ["高频", "文件", "fclose"], "easy"), "文件"),
        _tag(single_choice("L2C-219", "在删除单链表首结点时，头指针通常应更新为：", ["A. NULL", "B. 原首结点的 next", "C. 原首结点本身", "D. 文件指针"], "B", "删除首结点后，头指针应指向下一个结点。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(single_choice("L2C-220", "若用 `fread` 从二进制文件读取结构体数组，其返回值更常用于表示：", ["A. 文件名长度", "B. 实际读取到的对象个数", "C. 内存地址", "D. 错题数"], "B", "fread/fwrite 返回成功读写的对象个数。", ["高频", "文件", "二进制"], "medium"), "文件"),

        _tag(fill_blank("L2C-221", "若结构体结点定义中用于链接后继结点的成员名为 next，则遍历链表时通常写成 `p = p->______`。", ["next"], "单链表遍历的基础模板。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(fill_blank("L2C-222", "若要把一个结构体变量按文本格式写到文件中，更常用的函数是 ______。", ["fprintf"], "文本文件输出结构体记录通常依赖 fprintf。", ["高频", "文件", "输出"], "easy"), "文件"),
        _tag(fill_blank("L2C-223", "动态申请链表结点空间成功后，应把新结点的 next 指针先初始化为 ______ 或合理目标位置。", ["NULL"], "初始化 next 是链表构造常见要求。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(fill_blank("L2C-224", "若要从二进制文件中按块读取数据，更常见的函数是 ______。", ["fread"], "二进制文件读写基础题。", ["高频", "文件", "二进制"], "easy"), "文件"),
        _tag(fill_blank("L2C-225", "删除链表结点并释放空间后，常见良好习惯是把相关悬空指针赋为 ______。", ["NULL"], "释放后置空有助于减少误用风险。", ["高频", "动态内存", "指针"], "easy"), "动态内存"),
        _tag(fill_blank("L2C-226", "若读取文件中每行一条记录，常配合 `while` 循环判断读函数返回值是否为 ______。", ["NULL", "EOF", "成功值"], "核心思想是根据返回值控制循环，而不是盲目循环。", ["高频", "文件", "循环"], "medium"), "文件"),

        _tag(code_completion("L2C-227", "补全代码：`struct node *s = (struct node*)malloc(sizeof(struct node)); if(s != NULL) s->____ = NULL;`", ["next"], "新建链表结点时常需先把 next 置空。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(code_completion("L2C-228", "补全代码：`fprintf(fp, \"%d %s\\n\", stu.no, stu.____);`，已知成员名为 name。", ["name"], "结构体文本输出模板。", ["高频", "文件", "结构体"], "easy"), "文件"),
        _tag(code_completion("L2C-229", "补全代码：`while(p != NULL){ count++; p = p->____; }`", ["next"], "统计链表长度的标准遍历写法。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(code_completion("L2C-230", "补全代码：`n = fread(stu, sizeof(struct student), 20, fp); printf(\"%d\", ______);`", ["n"], "fread 返回实际读取对象数。", ["高频", "文件", "二进制"], "easy"), "文件"),
        _tag(code_completion("L2C-231", "补全代码：`struct node *q = p->next; p->next = q->next; ______(q);`", ["free"], "删除链表结点后应释放其空间。", ["高频", "结构体", "动态内存"], "medium"), "动态内存"),
        _tag(code_completion("L2C-232", "补全代码：`if((fp = fopen(\"stu.dat\", \"wb\")) == NULL) return 0; fwrite(stu, sizeof(struct student), n, ____);`", ["fp"], "写入二进制文件时最后一个参数是文件指针。", ["高频", "文件", "二进制"], "easy"), "文件"),

        _tag(subjective("L2C-233", "bug_fix", "某程序删除链表结点后只 `free(q)`，却没有把前驱结点的 next 改到 q 的后继。请说明问题。", "仅释放目标结点而不改链，链表仍保留错误链接，结构损坏。", [rubric_item("指出前驱 next 未修改", ["前驱", "next"], 4), rubric_item("指出链表结构损坏", ["结构损坏", "链表"], 4), rubric_item("说明正确顺序应先改链再释放", ["先改链", "再释放"], 2)], ["高频", "结构体", "bug_fix"], "hard"), "结构体"),
        _tag(subjective("L2C-234", "bug_fix", "某程序写成 `while(!feof(fp)){ fread(&stu, sizeof(struct student), 1, fp); ... }`。说明这种写法的问题。", "feof 在读失败后才置位，可能多处理一次无效数据，应依据 fread 返回值判断。", [rubric_item("指出 feof 判断滞后", ["feof", "滞后"], 4), rubric_item("指出可能多处理无效数据", ["多处理", "无效"], 3), rubric_item("提出用 fread 返回值控制循环", ["fread", "返回值"], 3)], ["高频", "文件", "bug_fix"], "hard"), "文件"),
        _tag(subjective("L2C-235", "bug_fix", "某程序创建新结点后没有给 `data` 和 `next` 成员赋初值就直接使用。请说明风险。", "未初始化成员含有不确定值，会导致数据错误或非法链接。", [rubric_item("指出成员未初始化", ["未初始化"], 4), rubric_item("指出 data 或 next 会是不确定值", ["不确定值"], 4), rubric_item("提出初始化再使用", ["初始化"], 2)], ["高频", "结构体", "bug_fix"], "medium"), "结构体"),
        _tag(subjective("L2C-236", "bug_fix", "某程序从文件读学生成绩时，数组已满仍继续写入数组。请说明问题。", "这会造成数组越界写入，破坏内存安全。", [rubric_item("指出数组越界", ["越界"], 5), rubric_item("指出需判断记录数上限", ["上限", "数组已满"], 3), rubric_item("提出停止读取或扩容思路", ["停止", "扩容"], 2)], ["高频", "文件", "bug_fix"], "medium"), "文件"),

        _tag(subjective("L2C-237", "programming", "说明如何编写函数，在链表尾部插入一个新结点。", "应包含创建结点、初始化数据和 next、遍历到尾结点、链接新结点。", [rubric_item("创建并初始化新结点", ["创建", "初始化"], 3), rubric_item("遍历到尾结点", ["遍历", "尾结点"], 3), rubric_item("修改尾结点 next", ["next", "链接"], 2), rubric_item("考虑空链表", ["空链表"], 2)], ["高频", "程序设计", "链表"], "hard"), "程序设计"),
        _tag(subjective("L2C-238", "programming", "说明如何把文本文件中的学生记录读入结构体数组并统计平均成绩。", "应包含打开文件、循环读取字段、累计总分和人数、求平均值、关闭文件。", [rubric_item("打开文件并判空", ["打开文件", "NULL"], 2), rubric_item("循环读取记录", ["循环读取"], 3), rubric_item("累计总分和人数", ["总分", "人数"], 3), rubric_item("求平均并关闭文件", ["平均", "关闭"], 2)], ["高频", "程序设计", "文件"], "hard"), "程序设计"),
        _tag(subjective("L2C-239", "programming", "说明如何编写函数，删除链表中所有值等于 x 的结点。", "应包含遍历链表、处理头结点连续匹配、修改前驱与当前指针、释放被删结点。", [rubric_item("遍历链表", ["遍历"], 2), rubric_item("处理头结点情况", ["头结点"], 3), rubric_item("修改链接关系", ["链接", "next"], 3), rubric_item("释放删除结点", ["free"], 2)], ["高频", "程序设计", "链表"], "hard"), "程序设计"),
        _tag(subjective("L2C-240", "programming", "说明如何把结构体数组按成绩从高到低写入文本文件。", "应包含先排序结构体数组，再依次用 fprintf 按格式写出并关闭文件。", [rubric_item("先排序结构体数组", ["排序", "结构体"], 4), rubric_item("依次写入文件", ["fprintf", "写入"], 3), rubric_item("关闭文件", ["fclose"], 2), rubric_item("按成绩降序", ["降序"], 1)], ["高频", "程序设计", "文件"], "medium"), "程序设计"),
    ]
