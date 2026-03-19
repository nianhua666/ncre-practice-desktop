# NCRE Practice

中国全国计算机等级考试模拟刷题桌面程序，当前重点覆盖二级 C 语言程序设计。

## Features

- 本地固定题库、系统组卷、专题冲刺、弱项补刷、错题重练
- AI 出题、AI 主观题讲评与批改
- OpenAI Compatible 接入，兼容 `Responses API`、`Chat Completions` 与 `Sub2API`
- 成绩记录、答题快照、错因分析、专题掌握度、自动复习建议
- Windows EXE 打包输出

## Built-in Bank

- 二级 C 语言程序设计：420 题
- 高频题：390 题
- 当前高频重点：程序设计、文件、结构体、字符串、算法与数据结构、数组、动态内存、函数

## Project Layout

```text
backend/     Python 本地服务与业务逻辑
frontend/    桌面 Web UI
data/        内置题库与资源
scripts/     生成题库、分析题库、打包与自测脚本
tests/       冒烟测试
```

## Development

运行源码版：

```powershell
python .\main.py --browser
```

运行单元测试：

```powershell
python -m unittest .\tests\smoke_test.py
```

分析题库：

```powershell
python .\scripts\analyze_question_banks.py
```

## AI Provider Setup

在“系统设置”页面中可以直接配置：

- OpenAI 官方 API
- OpenAI Compatible 网关
- Sub2API 最新兼容接入
- 一键应用 OpenAI / Sub2API 预设
- 直接测试连接是否可用

对于 Sub2API，直接填写网关地址即可，程序会自动规范 `/v1` 路径，并在 `chat/completions` 与 `responses` 之间自动兼容回退。

## Build EXE

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_exe.ps1
```

构建脚本会：

1. 重建题库
2. 打包 EXE
3. 自动执行打包版冒烟测试

打包产物：

```text
dist\NCREPractice\NCREPractice.exe
dist\NCREPractice-v0.3.3-win64.zip
```

注意：

- 不要运行 `build\NCREPractice\NCREPractice.exe`
- `build\` 目录是 PyInstaller 中间构建目录，不是最终发布产物
- 正式可运行版本始终使用 `dist\NCREPractice\NCREPractice.exe`

## License

MIT
