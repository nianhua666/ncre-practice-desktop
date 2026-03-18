from __future__ import annotations


def _tag(question, topic: str, frequency: str = "high") -> dict:
    question["topic"] = topic
    question["frequency"] = frequency
    question["source"] = "curated"
    return question


def build_level2_c_structure_memory_integrated_pack(single_choice, fill_blank, code_completion, subjective, rubric_item):
    return [
        _tag(single_choice("L2C-331", "若要动态申请一个结构体结点空间，较常见的表达式是：", ["A. `malloc(sizeof(struct node))`", "B. `fopen(sizeof(struct node))`", "C. `printf(struct node)`", "D. `free(struct node)`"], "A", "结构体动态分配通常基于 sizeof(struct node)。", ["高频", "结构体", "动态内存"], "easy"), "动态内存"),
        _tag(single_choice("L2C-332", "链表头插法的核心特点之一是：", ["A. 每次都插入到尾部", "B. 新结点插入后成为新的头结点", "C. 不需要 next 指针", "D. 只能用于数组"], "B", "头插法通过修改头指针把新结点放在最前面。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(single_choice("L2C-333", "若要把结构体数组按文本形式保存到文件，更常见的做法是：", ["A. 逐条用 fprintf 写入", "B. 直接用 strcmp", "C. 只用 scanf", "D. 把文件当作数组"], "A", "文本文件输出结构体记录通常逐条格式化写入。", ["高频", "文件", "结构体"], "medium"), "文件"),
        _tag(single_choice("L2C-334", "当链表为空时，头指针通常应为：", ["A. EOF", "B. 0.0", "C. NULL", "D. -1"], "C", "空链表的典型表示是空指针。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(single_choice("L2C-335", "若函数需要创建动态数组并返回给主调函数，更合理的返回类型通常是：", ["A. `int`", "B. `int *`", "C. `char`", "D. `void`"], "B", "动态数组返回的是首地址，因此类型通常是指针。", ["高频", "动态内存", "函数"], "easy"), "函数"),
        _tag(single_choice("L2C-336", "若结构体中含有字符数组成员 `name[20]`，要把字符串赋给它，较常用的做法是：", ["A. `name = \"abc\"`", "B. `strcpy(stu.name, \"abc\")`", "C. `stu.name == \"abc\"`", "D. `free(stu.name)`"], "B", "数组成员不能直接整体赋值，常用 strcpy 复制内容。", ["高频", "结构体", "字符串"], "medium"), "结构体"),
        _tag(single_choice("L2C-337", "顺序表删除一个中间元素后，通常需要：", ["A. 把其后元素前移", "B. 把其前元素后移", "C. 一定新建文件", "D. 删除整个数组"], "A", "顺序存储删除中间元素需补齐空缺。", ["高频", "数组", "数据结构"], "medium"), "算法与数据结构"),
        _tag(single_choice("L2C-338", "若结构体指针 p 指向学生结点，则访问学号成员 no 的写法通常是：", ["A. `p.no`", "B. `p->no`", "C. `*p.no`", "D. `p:no`"], "B", "结构体指针访问成员用箭头运算符。", ["高频", "结构体", "指针"], "easy"), "结构体"),
        _tag(single_choice("L2C-339", "若多次 `malloc` 后忘记 `free`，最典型的问题是：", ["A. 栈溢出", "B. 内存泄漏", "C. 数组越界", "D. 编译错误"], "B", "堆内存申请后不释放会泄漏。", ["高频", "动态内存", "bug"], "easy"), "动态内存"),
        _tag(single_choice("L2C-340", "若要从结构体数组中按条件筛选并写入新文件，本质上更接近：", ["A. 遍历 + 判断 + 文件输出", "B. 只做排序", "C. 只用递归", "D. 只用宏定义"], "A", "综合题通常是基础步骤的组合。", ["高频", "程序设计", "文件"], "easy"), "程序设计"),

        _tag(fill_blank("L2C-341", "若释放了动态申请的链表结点，常见函数是 ______。", ["free"], "释放堆内存的标准函数。", ["高频", "动态内存", "free"], "easy"), "动态内存"),
        _tag(fill_blank("L2C-342", "头插法建立链表时，新结点的 next 通常先指向原来的 ______。", ["头结点", "头指针所指结点", "链表头"], "头插法核心是把原头结点接到新结点后面。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(fill_blank("L2C-343", "若把结构体记录写入文本文件，每成功输出一条记录后，记录数通常加 ______。", ["1", "一"], "结构体文件题也离不开计数。", ["高频", "文件", "结构体"], "easy"), "文件"),
        _tag(fill_blank("L2C-344", "若函数返回值是动态数组首地址，则主调函数用完后通常应负责 ______ 它。", ["释放", "free"], "谁持有返回指针，谁通常要负责释放。", ["高频", "动态内存", "函数"], "medium"), "动态内存"),
        _tag(fill_blank("L2C-345", "若顺序表删除下标为 k 的元素，其后所有元素通常要向 ______ 移动一位。", ["前", "左"], "顺序表删除需要整体前移补位。", ["高频", "数组", "数据结构"], "easy"), "算法与数据结构"),
        _tag(fill_blank("L2C-346", "若结构体变量名为 stu，访问其成绩成员 score 应写作 `stu.______`。", ["score"], "结构体变量访问成员用点运算符。", ["高频", "结构体", "基础"], "easy"), "结构体"),

        _tag(code_completion("L2C-347", "补全代码：`struct node *s = (struct node*)malloc(sizeof(struct node)); if(s == NULL) return 0; s->next = ____;`", ["NULL"], "新结点通常先把 next 置空。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(code_completion("L2C-348", "补全代码：`for(i=k;i<n-1;i++) a[i] = a[____];`，实现删除顺序表第 k 个元素后的前移。", ["i+1"], "顺序表删除后的补位模板。", ["高频", "数组", "数据结构"], "easy"), "算法与数据结构"),
        _tag(code_completion("L2C-349", "补全代码：`fprintf(fp, \"%d %s %d\\n\", stu.no, stu.name, stu.____);`，已知成绩成员为 score。", ["score"], "结构体输出到文本文件的常见写法。", ["高频", "文件", "结构体"], "easy"), "文件"),
        _tag(code_completion("L2C-350", "补全代码：`p = (int*)malloc(sizeof(int)*n); if(p==NULL) return 0; for(i=0;i<n;i++) scanf(\"%d\", &p[____]);`", ["i"], "动态数组输入模板。", ["高频", "动态内存", "数组"], "easy"), "动态内存"),
        _tag(code_completion("L2C-351", "补全代码：`newnode->next = head; head = ______;`", ["newnode"], "头插法建立链表的核心两步。", ["高频", "结构体", "链表"], "easy"), "结构体"),
        _tag(code_completion("L2C-352", "补全代码：`if((fp = fopen(\"stu.txt\", \"w\")) == NULL) return 0; ... fclose(____);`", ["fp"], "文件关闭时应传入对应文件指针。", ["高频", "文件", "基础"], "easy"), "文件"),

        _tag(subjective("L2C-353", "bug_fix", "某程序头插法建立链表时写成 `head = head->next; newnode->next = head;`。请说明问题。", "先移动 head 会丢失原链表头结点，导致链表断裂或数据丢失。", [rubric_item("指出原头结点可能丢失", ["原头结点", "丢失"], 4), rubric_item("指出链接顺序错误", ["顺序错误", "链接"], 4), rubric_item("提出先 `newnode->next=head` 再 `head=newnode`", ["newnode->next", "head=newnode"], 2)], ["高频", "结构体", "bug_fix"], "hard"), "结构体"),
        _tag(subjective("L2C-354", "bug_fix", "某程序释放动态数组后仍继续访问 `p[i]`。请说明问题。", "释放后指针成为悬空指针，继续访问属于未定义行为。", [rubric_item("指出释放后为悬空指针", ["悬空", "释放后"], 5), rubric_item("指出继续访问未定义", ["未定义行为", "继续访问"], 3), rubric_item("提出释放后置空并停止使用", ["置空", "停止使用"], 2)], ["高频", "动态内存", "bug_fix"], "medium"), "动态内存"),
        _tag(subjective("L2C-355", "bug_fix", "某程序把结构体数组内容写文件时循环边界写成 `i<=n`。请说明风险。", "当 i=n 时会访问数组越界，可能把无效数据写入文件。", [rubric_item("指出数组越界", ["越界"], 5), rubric_item("指出可能写入无效数据", ["无效数据", "写入"], 3), rubric_item("提出应为 i<n", ["i<n"], 2)], ["高频", "文件", "bug_fix"], "easy"), "文件"),
        _tag(subjective("L2C-356", "bug_fix", "某函数返回动态结构体数组首地址，但主调函数声明为普通结构体变量接收。请说明问题。", "返回值类型与接收变量类型不匹配，会导致类型错误或地址丢失。", [rubric_item("指出返回的是地址", ["地址", "指针"], 4), rubric_item("指出接收类型不匹配", ["类型不匹配"], 4), rubric_item("提出应使用结构体指针接收", ["结构体指针"], 2)], ["高频", "结构体", "bug_fix"], "medium"), "结构体"),

        _tag(subjective("L2C-357", "programming", "说明如何编写函数，使用头插法建立一个存放 n 个整数的单链表。", "应包含循环读入数据、申请新结点、赋值、链接到头部、更新头指针。", [rubric_item("循环读入数据", ["循环", "读入"], 2), rubric_item("申请新结点", ["malloc", "新结点"], 3), rubric_item("赋值并链接头部", ["赋值", "链接"], 3), rubric_item("更新头指针", ["头指针"], 2)], ["高频", "程序设计", "链表"], "hard"), "程序设计"),
        _tag(subjective("L2C-358", "programming", "说明如何编写函数，将结构体数组中成绩不及格的记录写入新文件。", "应包含遍历结构体数组、按成绩判断、把不及格记录写入目标文件、最后关闭文件。", [rubric_item("遍历结构体数组", ["遍历", "结构体数组"], 2), rubric_item("按成绩筛选", ["成绩", "不及格"], 3), rubric_item("写入文件", ["写入文件", "fprintf"], 3), rubric_item("关闭文件", ["fclose"], 2)], ["高频", "程序设计", "文件"], "medium"), "程序设计"),
        _tag(subjective("L2C-359", "programming", "说明如何删除顺序表中所有重复元素，只保留第一次出现。", "应包含双重比较或辅助标记、发现重复时删除并前移、更新有效长度。", [rubric_item("识别重复元素", ["重复", "比较"], 4), rubric_item("删除并前移", ["前移", "删除"], 3), rubric_item("更新有效长度", ["长度"], 3)], ["高频", "程序设计", "数组"], "hard"), "程序设计"),
        _tag(subjective("L2C-360", "programming", "说明如何设计函数，释放整个单链表所占用的动态内存。", "应包含用指针遍历链表、先保存后继结点、释放当前结点、继续直到 NULL。", [rubric_item("遍历链表", ["遍历", "链表"], 3), rubric_item("先保存后继结点", ["后继", "保存"], 3), rubric_item("逐结点 free", ["free"], 2), rubric_item("直到 NULL 结束", ["NULL"], 2)], ["高频", "程序设计", "链表"], "medium"), "程序设计"),
    ]
