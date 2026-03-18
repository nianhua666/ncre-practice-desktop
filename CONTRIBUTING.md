# Contributing

## Scope

优先提交以下类型的改进：

- 二级 C 语言题库扩展
- 题目解析、评分点和错因说明增强
- 组卷策略优化
- UI 可用性优化
- AI 兼容层稳定性增强

## Quality Bar

- 不要只加选择题，优先补程序设计、改错、代码补全
- 新增题目必须带 `analysis`
- 新增题目应尽量带 `topic` 和 `frequency`
- 修改组卷逻辑后必须跑 `tests/smoke_test.py`
- 修改打包链路后必须跑打包版自测

## Suggested Flow

```powershell
python .\scripts\generate_seed_banks.py
python -m unittest .\tests\smoke_test.py
python .\scripts\analyze_question_banks.py
```
