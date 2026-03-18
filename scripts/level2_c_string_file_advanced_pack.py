from __future__ import annotations


def _tag(question, topic: str, frequency: str = "high") -> dict:
    question["topic"] = topic
    question["frequency"] = frequency
    question["source"] = "curated"
    return question


def build_level2_c_string_file_advanced_pack(single_choice, fill_blank, code_completion, subjective, rubric_item):
    return [
        _tag(single_choice("L2C-241", "若要删除字符串尾部的换行符，最常见的前提是该换行符通常由哪个函数读入？", ["A. malloc", "B. fgets", "C. printf", "D. free"], "B", "fgets 读取整行时常把换行符一并读入缓冲区。", ["高频", "字符串", "文件"], "easy"), "字符串"),
        _tag(single_choice("L2C-242", "比较两个字符串字典序大小时，更常用的库函数是：", ["A. strcpy", "B. strcat", "C. strcmp", "D. strlen"], "C", "strcmp 返回比较结果，适用于字符串顺序判断。", ["高频", "字符串", "库函数"], "easy"), "字符串"),
        _tag(single_choice("L2C-243", "若要把文本文件中的一行完整读入字符数组，较合适的函数是：", ["A. scanf", "B. fgets", "C. putchar", "D. fwrite"], "B", "读取一整行文本时，fgets 是常见方案。", ["高频", "文件", "字符串"], "easy"), "文件"),
        _tag(single_choice("L2C-244", "若 `char s[20]=\"abc\";`，执行 `strcat(s,\"xyz\")` 后，s 的内容为：", ["A. abc", "B. xyz", "C. abcxyz", "D. zyxabc"], "C", "strcat 会把源串追加到目标串尾部。", ["高频", "字符串", "库函数"], "easy"), "字符串"),
        _tag(single_choice("L2C-245", "使用 `fprintf` 写文本文件时，格式控制符 `%s` 通常对应：", ["A. 一个整型变量", "B. 一个字符", "C. 一个字符串", "D. 一个地址常量"], "C", "fprintf 的格式控制与 printf 类似，%s 对应字符串。", ["高频", "文件", "fprintf"], "easy"), "文件"),
        _tag(single_choice("L2C-246", "若要统计字符串中某个字符出现次数，更自然的思路是：", ["A. 排序整个字符串", "B. 逐字符遍历并判断", "C. 只比较首尾两个字符", "D. 改成链表"], "B", "字符统计问题本质上是遍历 + 条件判断 + 计数。", ["高频", "字符串", "程序设计"], "easy"), "程序设计"),
        _tag(single_choice("L2C-247", "若程序要把若干整数写入二进制文件，较合适的函数是：", ["A. fprintf", "B. fwrite", "C. fgets", "D. puts"], "B", "二进制文件通常用 fwrite 成块写入。", ["高频", "文件", "二进制"], "medium"), "文件"),
        _tag(single_choice("L2C-248", "若想求字符串长度而不包含结束符，更常用的函数是：", ["A. sizeof", "B. strlen", "C. strcpy", "D. strcat"], "B", "strlen 统计字符串中的字符个数，不含 \\0。", ["高频", "字符串", "库函数"], "easy"), "字符串"),
        _tag(single_choice("L2C-249", "若程序用 `fscanf(fp, \"%d\", &x)` 读整数，则循环结束更稳妥的依据是：", ["A. 先看 feof", "B. 直接判断 fscanf 返回值", "C. 先 free(fp)", "D. 一定读到 0 才结束"], "B", "读函数返回值最能准确反映读入是否成功。", ["高频", "文件", "读取"], "medium"), "文件"),
        _tag(single_choice("L2C-250", "若把字符串中的每个小写字母转成大写字母，较常见的处理方式是：", ["A. 对满足范围的字符减去 32", "B. 所有字符都加 32", "C. 用 strcmp", "D. 用 fopen"], "A", "ASCII 环境下小写转大写常利用编码差值 32。", ["高频", "字符串", "字符处理"], "medium"), "字符串"),

        _tag(fill_blank("L2C-251", "若读取文件时希望从头重新开始，可调用函数 ______ 将文件位置移回开头。", ["rewind"], "rewind 是文件位置重置的典型考点。", ["高频", "文件", "文件指针"], "easy"), "文件"),
        _tag(fill_blank("L2C-252", "若要把字符串中所有字符复制到另一个字符数组并保证结束符一起复制，常用函数是 ______。", ["strcpy"], "strcpy 会复制字符直到包括结束符。", ["高频", "字符串", "库函数"], "easy"), "字符串"),
        _tag(fill_blank("L2C-253", "文本文件中每读取成功一个整数就让计数器加 ______。", ["1", "一"], "文件统计整数个数的基础模板。", ["高频", "文件", "程序设计"], "easy"), "程序设计"),
        _tag(fill_blank("L2C-254", "若用指针遍历字符串，遇到字符 ______ 时通常表示字符串结束。", ["\\0", "空字符"], "字符串结束符是基础高频点。", ["高频", "字符串", "基础"], "easy"), "字符串"),
        _tag(fill_blank("L2C-255", "若想把格式化内容写入文件，应先确保文件指针不为 ______。", ["NULL"], "文件判空是安全写入的前提。", ["高频", "文件", "错误处理"], "easy"), "文件"),
        _tag(fill_blank("L2C-256", "若比较两个字符串内容是否完全相等，更合理的做法是检查 `strcmp` 的返回值是否等于 ______。", ["0"], "strcmp 返回 0 表示内容相同。", ["高频", "字符串", "比较"], "easy"), "字符串"),

        _tag(code_completion("L2C-257", "补全代码：`if(s[i] == ' ') continue; else t[k++] = s[____];`", ["i"], "删除空格时，保留非空格字符即可。", ["高频", "字符串", "程序设计"], "easy"), "程序设计"),
        _tag(code_completion("L2C-258", "补全代码：`while(fscanf(fp, \"%d\", &x) == 1){ count++; sum += ____; }`", ["x"], "文件读整数求和常见模板。", ["高频", "文件", "程序设计"], "easy"), "文件"),
        _tag(code_completion("L2C-259", "补全代码：`if(ch >= 'a' && ch <= 'z') ch = ch - ____;`", ["32"], "小写转大写常用减 32。", ["高频", "字符串", "字符处理"], "easy"), "字符串"),
        _tag(code_completion("L2C-260", "补全代码：`if((fp = fopen(\"a.txt\", \"r\")) == NULL) return 0; while(fgets(s, sizeof(s), fp) != NULL) puts(____);`", ["s"], "读一行、输出一行的基础模型。", ["高频", "文件", "字符串"], "easy"), "文件"),
        _tag(code_completion("L2C-261", "补全代码：`for(i=0; s[i] != '\\0'; i++) if(s[i] == key) ______;`，设统计 key 出现次数。", ["count++", "++count"], "字符计数本质上是条件满足时自增。", ["高频", "字符串", "程序设计"], "easy"), "程序设计"),
        _tag(code_completion("L2C-262", "补全代码：`n = fwrite(a, sizeof(int), m, fp); if(n != m) printf(\"write ______\\n\");`", ["error"], "fwrite 返回值可用于检查写入是否完整。", ["高频", "文件", "二进制"], "medium"), "文件"),

        _tag(subjective("L2C-263", "bug_fix", "某程序用 `scanf(\"%s\", s)` 读取可能含空格的句子。请说明问题。", "这种写法会在空格处停止，无法读取整句内容；若未限宽还可能溢出。", [rubric_item("指出遇空格停止", ["空格", "停止"], 4), rubric_item("指出可能溢出", ["溢出", "限宽"], 3), rubric_item("给出 fgets 或更稳妥输入方案", ["fgets"], 3)], ["高频", "字符串", "bug_fix"], "medium"), "字符串"),
        _tag(subjective("L2C-264", "bug_fix", "某程序把 `fgets` 读入的一行直接与目标字符串比较，却忽略了行末可能保留的换行符。请说明影响。", "换行符会参与比较，导致看似相同的内容比较失败，应先去掉换行。", [rubric_item("指出换行符被保留", ["换行符"], 4), rubric_item("指出比较可能失败", ["比较失败"], 3), rubric_item("提出先删除换行符", ["删除换行", "\\n"], 3)], ["高频", "字符串", "bug_fix"], "medium"), "字符串"),
        _tag(subjective("L2C-265", "bug_fix", "某程序写文件后没有判断 `fprintf` 或 `fwrite` 的结果。请说明隐患。", "写入失败时程序可能误以为成功，导致数据丢失却没有被发现。", [rubric_item("指出缺少结果检查", ["检查", "返回值"], 4), rubric_item("指出可能数据丢失", ["数据丢失"], 4), rubric_item("提出根据返回值处理异常", ["返回值", "异常"], 2)], ["高频", "文件", "bug_fix"], "medium"), "文件"),
        _tag(subjective("L2C-266", "bug_fix", "某程序在 `strcpy(dest, src)` 前没有确认 dest 空间是否足够。请说明问题。", "若目标数组过小，复制会越界写入，造成缓冲区溢出。", [rubric_item("指出目标空间不足风险", ["空间不足"], 4), rubric_item("指出越界写入或溢出", ["越界", "溢出"], 4), rubric_item("提出检查长度或扩容", ["长度", "扩容"], 2)], ["高频", "字符串", "bug_fix"], "medium"), "字符串"),

        _tag(subjective("L2C-267", "programming", "说明如何编写函数，统计文本文件中行数、单词数和字符数。", "应包含逐字符或逐行读取、区分空白与单词边界、分别累计三类计数。", [rubric_item("读取文件内容", ["读取", "文件"], 2), rubric_item("统计行数", ["行数"], 2), rubric_item("统计单词数", ["单词", "空白"], 3), rubric_item("统计字符数", ["字符数"], 3)], ["高频", "程序设计", "文件"], "hard"), "程序设计"),
        _tag(subjective("L2C-268", "programming", "说明如何编写函数，将字符串中的连续多个空格压缩成一个空格。", "应包含遍历字符串、记录前一个字符是否为空格、按条件写入新位置并补结束符。", [rubric_item("遍历字符串", ["遍历"], 2), rubric_item("识别连续空格", ["连续空格"], 3), rubric_item("按条件写回", ["写回", "压缩"], 3), rubric_item("补结束符", ["结束符"], 2)], ["高频", "程序设计", "字符串"], "hard"), "程序设计"),
        _tag(subjective("L2C-269", "programming", "说明如何把一个文本文件中的所有小写字母转换为大写后输出到另一个文件。", "应包含打开两个文件、逐字符读取、判断并转换小写字母、写入目标文件、关闭文件。", [rubric_item("打开源和目标文件", ["打开文件"], 2), rubric_item("逐字符读取", ["逐字符"], 2), rubric_item("判断并转换小写字母", ["小写", "转换"], 4), rubric_item("写入并关闭文件", ["写入", "关闭"], 2)], ["高频", "程序设计", "文件"], "hard"), "程序设计"),
        _tag(subjective("L2C-270", "programming", "说明如何设计函数，判断字符串 t 是否为字符串 s 的子串。", "应包含遍历 s 的起始位置、逐字符比较 t、找到匹配即返回成功。", [rubric_item("遍历起始位置", ["起始位置", "遍历"], 3), rubric_item("逐字符比较", ["逐字符", "比较"], 4), rubric_item("匹配成功及时返回", ["返回", "成功"], 3)], ["高频", "程序设计", "字符串"], "hard"), "程序设计"),
    ]
