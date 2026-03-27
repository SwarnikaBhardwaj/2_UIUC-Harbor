# 2. Cost Comparison and Infrastructure Planning

Harbor uses LLMs to understand short marketplace text that supports search and discovery, such as categorizing listings, extracting fields, summarizing descriptions, and assisting with simple user interactions :contentReference[oaicite:0]{index=0}.

---

## Daily Traffic Categories

| Daily Traffic Category | Daily Active Users |
|----------------------|------------------|
| Prototype | 1,000 |
| Early Startup | 10,000 |
| Growing Product | 100,000 |
| Large Platform | 1,000,000 |
| Mass Consumer App | 10,000,000 |
| Global Platform | 100,000,000 |

---

## 2.1 Estimated Token Usage

Average tokens per request = **250 tokens per request**

---

## 2.2 Compute Total Token Load

| Daily Traffic Category | Daily Active Users | Avg Tokens per Request | Total Daily Token Load |
|----------------------|------------------|----------------------|------------------------|
| Prototype | 1,000 | 250 | 250,000 |
| Early Startup | 10,000 | 250 | 2,500,000 |
| Growing Product | 100,000 | 250 | 25,000,000 |
| Large Platform | 1,000,000 | 250 | 250,000,000 |
| Mass Consumer App | 10,000,000 | 250 | 2,500,000,000 |
| Global Platform | 100,000,000 | 250 | 25,000,000,000 |

---

## 2.3 Hardware Cost Estimation (Local Hosting)

I standardized the cost of a local-hosting machine to $36/day / per machine. This is based off of a simplified estimate for a modest cloud inference box with GPU access, CPU, RAM, storage, and supporting overhead.

The machines needed follow a linear progression based on user growth.

| Model Name | Daily Traffic Category | Avg Tokens per User | Total Daily Token Load | Per Machine Cost (Cloud/day) | Machines Needed | Total Machine Cost/day |
|-----------|----------------------|--------------------|------------------------|-----------------------------|----------------|------------------------|
| Qwen/Qwen2.5-3B-Instruct | Prototype | 250 | 250,000 | $36.00 | 1 | $36.00 |
| Qwen/Qwen2.5-3B-Instruct | Early Startup | 250 | 2,500,000 | $36.00 | 2 | $72.00 |
| Qwen/Qwen2.5-3B-Instruct | Growing Product | 250 | 25,000,000 | $36.00 | 18 | $648.00 |
| Qwen/Qwen2.5-3B-Instruct | Large Platform | 250 | 250,000,000 | $36.00 | 175 | $6,300.00 |
| Qwen/Qwen2.5-3B-Instruct | Mass Consumer App | 250 | 2,500,000,000 | $36.00 | 1744 | $62,784.00 |
| Qwen/Qwen2.5-3B-Instruct | Global Platform | 250 | 25,000,000,000 | $36.00 | 17438 | $627,768.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Prototype | 250 | 250,000 | $36.00 | 1 | $36.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Early Startup | 250 | 2,500,000 | $36.00 | 2 | $72.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Growing Product | 250 | 25,000,000 | $36.00 | 15 | $540.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Large Platform | 250 | 250,000,000 | $36.00 | 148 | $5,328.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Mass Consumer App | 250 | 2,500,000,000 | $36.00 | 1478 | $53,208.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Global Platform | 250 | 25,000,000,000 | $36.00 | 14777 | $531,972.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Prototype | 250 | 250,000 | $36.00 | 1 | $36.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Early Startup | 250 | 2,500,000 | $36.00 | 2 | $72.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Growing Product | 250 | 25,000,000 | $36.00 | 12 | $432.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Large Platform | 250 | 250,000,000 | $36.00 | 117 | $4,212.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Mass Consumer App | 250 | 2,500,000,000 | $36.00 | 1165 | $41,940.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Global Platform | 250 | 25,000,000,000 | $36.00 | 11642 | $419,112.00 |
| Qwen/Qwen2.5-1.5B-Instruct | Prototype | 250 | 250,000 | $36.00 | 1 | $36.00 |
| Qwen/Qwen2.5-1.5B-Instruct | Early Startup | 250 | 2,500,000 | $36.00 | 2 | $72.00 |
| Qwen/Qwen2.5-1.5B-Instruct | Growing Product | 250 | 25,000,000 | $36.00 | 14 | $504.00 |
| Qwen/Qwen2.5-1.5B-Instruct | Large Platform | 250 | 250,000,000 | $36.00 | 136 | $4,896.00 |
| Qwen/Qwen2.5-1.5B-Instruct | Mass Consumer App | 250 | 2,500,000,000 | $36.00 | 1359 | $48,924.00 |
| Qwen/Qwen2.5-1.5B-Instruct | Global Platform | 250 | 25,000,000,000 | $36.00 | 13588 | $489,168.00 |

---

## Step 2.4: Hugging Face Inference API Cost Comparison

These calculations are based on assumptions that the platform will manage on average 1 request per user day. This is reasonable as students are given a finite pool to trustworthy buyers and sellers each day reducing the need for over 1 request per user (also considering that it would not be typical for the average student with the app to use it every single day).

| Local Model | Comparable Paid Model | HF Hosted | Cost/token | Traffic | Token Load | API Cost | Machines | Total Cost |
|------------|----------------------|----------|-----------|--------|-----------|----------|----------|-----------|
| Qwen 3B | Medium hosted model | Yes | 0.00000075 | Prototype | 250,000 | $0.19 | 0 | $0.19 |
| Qwen 3B | Medium hosted model | Yes | 0.00000075 | Early Startup | 2,500,000 | $1.88 | 0 | $1.88 |
| Qwen 3B | Medium hosted model | Yes | 0.00000075 | Growing Product | 25,000,000 | $18.75 | 0 | $18.75 |
| Qwen 3B | Medium hosted model | Yes | 0.00000075 | Large Platform | 250,000,000 | $187.50 | 0 | $187.50 |
| Qwen 3B | Medium hosted model | Yes | 0.00000075 | Mass Consumer App | 2,500,000,000 | $1,875.00 | 0 | $1,875.00 |
| Qwen 3B | Medium hosted model | Yes | 0.00000075 | Global Platform | 25,000,000,000 | $18,750.00 | 0 | $18,750.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Small hosted instruct model | Yes | 0.00000010 | Prototype | 250,000 | $0.03 | 0 | $0.03 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Small hosted instruct model | Yes | 0.00000010 | Early Startup | 2,500,000 | $0.25 | 0 | $0.25 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Small hosted instruct model | Yes | 0.00000010 | Growing Product | 25,000,000 | $2.50 | 0 | $2.50 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Small hosted instruct model | Yes | 0.00000010 | Large Platform | 250,000,000 | $25.00 | 0 | $25.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Small hosted instruct model | Yes | 0.00000010 | Mass Consumer App | 2,500,000,000 | $250.00 | 0 | $250.00 |
| HuggingFaceTB/SmolLM2-360M-Instruct | Small hosted instruct model | Yes | 0.00000010 | Global Platform | 25,000,000,000 | $2,500.00 | 0 | $2,500.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Small hosted instruct model | Yes | 0.00000010 | Prototype | 250,000 | $0.03 | 0 | $0.03 |
| Qwen/Qwen2.5-0.5B-Instruct | Small hosted instruct model | Yes | 0.00000010 | Early Startup | 2,500,000 | $0.25 | 0 | $0.25 |
| Qwen/Qwen2.5-0.5B-Instruct | Small hosted instruct model | Yes | 0.00000010 | Growing Product | 25,000,000 | $2.50 | 0 | $2.50 |
| Qwen/Qwen2.5-0.5B-Instruct | Small hosted instruct model | Yes | 0.00000010 | Large Platform | 250,000,000 | $25.00 | 0 | $25.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Small hosted instruct model | Yes | 0.00000010 | Mass Consumer App | 2,500,000,000 | $250.00 | 0 | $250.00 |
| Qwen/Qwen2.5-0.5B-Instruct | Small hosted instruct model | Yes | 0.00000010 | Global Platform | 25,000,000,000 | $2,500.00 | 0 | $2,500.00 |
| Qwen/Qwen2.5-1.5B-Instruct | Medium hosted model | Yes | 0.00000025 | Prototype | 250,000 | $0.06 | 0 | $0.06 |
| Qwen/Qwen2.5-1.5B-Instruct | Medium hosted model | Yes | 0.00000025 | Early Startup | 2,500,000 | $0.63 | 0 | $0.63 |
| Qwen/Qwen2.5-1.5B-Instruct | Medium hosted model | Yes | 0.00000025 | Growing Product | 25,000,000 | $6.25 | 0 | $6.25 |
| Qwen/Qwen2.5-1.5B-Instruct | Medium hosted model | Yes | 0.00000025 | Large Platform | 250,000,000 | $62.50 | 0 | $62.50 |
| Qwen/Qwen2.5-1.5B-Instruct | Medium hosted model | Yes | 0.00000025 | Mass Consumer App | 2,500,000,000 | $625.00 | 0 | $625.00 |
| Qwen/Qwen2.5-1.5B-Instruct | Medium hosted model | Yes | 0.00000025 | Global Platform | 25,000,000,000 | $6,250.00 | 0 | $6,250.00 |

---

## 2.5 Analysis

### At what scale is local hosting cheaper?

Based on the cost estimates calculated, local hosting isn’t cheaper at any of the evaluated traffic scales. Even at the largest scale considered (Global Platform), the total daily cost of running local infrastructure remains significantly higher than the cost of using a hosted API. This may be due to the high number of machines that are required to handle large token loads, which leads to substantial infrastructure costs. Therefore, local hosting is not more cost-effective than API usage at any point.

---

### At what scale is API usage cheaper?

API usage is cheaper at all traffic scales analyzed, including Prototype, Early Startup, Growing Product, Large Platform, Mass Consumer App, and Global Platform. At lower scales, API usage is cost-effective because it avoids fixed infrastructure costs and allows the systems to pay only for actual usage. Even at higher scales, the total API costs grow linearly with token usage but still remains below the cost of maintaining large numbers of machines required for local hosting.

---

### When would you switch your architecture?

Based on the results so far, there isn’t a clear point at which switching from API-based inference to local hosting becomes more cost-efficient. Therefore, the system would continue using API-based inference across all traffic levels. However, a switch to local hosting could be considered in the future if conditions change, such as an increase in API pricing, significantly higher token usage per request, or the need for greater control over data privacy or system customization.