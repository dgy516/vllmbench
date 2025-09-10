# vLLM 基准体系 — SRS + HLD 合并稿（精简版）
**版本**：v1.0  **日期**：2025-09-10 09:39

- 仅 vLLM；Ascend 910B/910C；Euler + Docker + K8s + CANN 8.2；Python 3.11
- 对比：当前 commit vs D-1 vs 7-day（同一 pd_mode 内）
- 精度：数值一致性（logits 余弦 + EM），任务集：GPQA-diamond / HumanEval（simple_evals）；多模态：MME
- 性能：acs-bench；全部流式（功能 CI 另测非流式）
- 指标：吞吐、TTFT、TPOT、成功率 + CPU/内存/网络；Prom + Grafana；HTML 一页总览
- 配置：单场景单 YAML；base+overlay；pd_mode=mixed|separated；failure_policy=stop|continue（默认 stop）
- 数据：内网 NFS；JSONL 不脱敏；保留 90 天

## 架构概览
Scenario Loader → Orchestrator → Driver/Router（mixed/separated）→ LoadGen（OpenAI SSE/非流式）→
Perf Runner（acs-bench）/ Eval Runner（simple_evals/MME）→ Metrics → Aggregator → Prom Exporter →
Baseline Comparator & Gate → HTML Report → Artifacts Manager

## 产物与契约
- JSONL（请求级）、CSV（场景级）、manifest.yaml、HTML 报告（命名规范统一）
- Prom 指标名与标签（不含 service_params；含 pd_mode）

## 配置示例（节选）
schema_version: v1
scenario_name: basic_stream_toppp
workload: { streaming: true, input_len: [256,1024], output_cap: [256,512], concurrency: [4,16,64] }
pd: { mode: mixed }
service: { params: { max_num_seqs: 256, max_model_len: 8192, paged_kv: true } }
ci: { repeats: 1, timeout_minutes: 90, failure_policy: stop }
reports: { html: true, grafana: true, pr_comment: false }

详细长版请在项目 README 的「SRS-HLD.md」获取。
