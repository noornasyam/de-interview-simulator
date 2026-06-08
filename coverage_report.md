# V2 Question Bank Coverage Report

Generated for `app/data/question_bank/v2`.

## Executive Summary

- Total curated v2 questions: 480
- Completed domains found: Airflow, AWS, Azure, Data Modeling, GCP / BigQuery, Python, SQL, Terraform
- Completed levels per domain: Beginner, Junior Data Engineer, Mid-Level Data Engineer, Senior Data Engineer, Lead Data Engineer, Architect
- Every detected domain currently has 60 questions, with 10 questions per level.
- Schema validation status: compatible with the current v2 validator shape.

The question-bank foundation is strong: every completed domain has the expected level ladder and the early levels use objective question types while senior levels move toward scenario, troubleshooting, design, governance, reliability, and architecture prompts.

The biggest gaps are not count-related. They are coverage and variety issues:

- Databricks, dbt, Git, and Production Engineering are still missing as standalone v2 domains.
- AWS and Azure are valid and useful, but many senior/lead/architect prompts share the same wording pattern across both clouds.
- Several senior-level prompts are intentionally broad, which is useful for interview simulation but can become repetitive if a user takes multiple cloud interviews.
- Difficulty labels are not fully normalized. Some files use `scenario`, `advanced`, and `expert` as difficulty values alongside `easy`, `medium`, and `hard`.

## Overall Domain Summary

| Domain | Total Questions | Levels Complete | Main Strength | Main Concern |
|---|---:|---:|---|---|
| Airflow | 60 | 6/6 | Strong orchestration and Composer coverage | Duplicate concepts: task idempotency, Composer worker scaling |
| AWS | 60 | 6/6 | Strong AWS data platform, S3, Glue, Athena, Redshift coverage | Several prompt templates mirror Azure closely |
| Azure | 60 | 6/6 | Strong Azure platform, ADF, ADLS, Synapse, Purview coverage | Several prompt templates mirror AWS closely |
| Data Modeling | 60 | 6/6 | Strong dimensional modeling and governance coverage | Less emphasis on concrete SQL DDL/model implementation exercises |
| GCP / BigQuery | 60 | 6/6 | Strong BigQuery, Composer, Dataflow, cost, governance coverage | Naming still uses `gcp_bigquery`; user-facing target is GCP |
| Python | 60 | 6/6 | Strong production Python, ETL, testing, observability coverage | Could use more objective questions for early Python syntax/data structures |
| SQL | 60 | 6/6 | Strong progression from basics to production SQL architecture | Advanced levels lean broad; fewer engine-specific debugging examples |
| Terraform | 60 | 6/6 | Strong IaC, state, modules, governance, platform standards coverage | Could add more hands-on plan/state interpretation questions later |

## Per-Domain, Per-Level Coverage

### Airflow

| Level | Count | Type Distribution | Difficulty Distribution |
|---|---:|---|---|
| Beginner | 10 | fill_blank: 3, match: 3, mcq: 4 | easy: 10 |
| Junior Data Engineer | 10 | fill_blank: 2, match: 2, mcq: 3, short_answer: 3 | easy: 3, medium: 7 |
| Mid-Level Data Engineer | 10 | mcq: 2, scenario: 3, short_answer: 3, troubleshooting: 2 | easy: 1, medium: 4, scenario: 4, hard: 1 |
| Senior Data Engineer | 10 | design_decision: 3, reliability: 2, scenario: 2, troubleshooting: 3 | medium: 2, scenario: 3, hard: 5 |
| Lead Data Engineer | 10 | architecture: 2, governance: 2, reliability: 2, stakeholder_impact: 2, trade_off: 2 | medium: 2, scenario: 2, hard: 6 |
| Architect | 10 | cost_optimization: 2, enterprise_architecture: 1, governance: 2, platform_design: 2, reliability: 2, security: 1 | advanced: 5, expert: 5 |

Concepts covered:

- Beginner: DAG basics, tasks, operators, dependencies, retries, schedules, sensors, Cloud Composer, metadata.
- Junior: catchup, idempotency, task states, XCom, backfills, connections, branching, variables.
- Mid-Level: pools, backfill planning, stuck tasks, DAG parsing, `max_active_runs`, sensor design, failed tasks, testing, Composer scaling.
- Senior: production DAG design, scheduler issues, event-driven orchestration, SLAs, dynamic DAGs, backfill incidents, XCom alternatives, CI/CD, branching and quality.
- Lead: enterprise standards, centralized vs domain-owned orchestration, incident communication, access controls, reliability model, reusable templates, secrets governance, migration roadmap.
- Architect: orchestration strategy, Composer platform design, governance, cost, reliability, security, multi-tenant Airflow, lifecycle governance, DR, migration from Airflow.

Duplicate concepts detected:

- `Task idempotency`: 2 occurrences.
- `Cloud Composer worker scaling`: 2 occurrences.

Difficulty progression assessment:

- Good progression by level.
- Needs normalization because `scenario` appears as a difficulty value in Mid-Level, Senior, and Lead files.

### AWS

| Level | Count | Type Distribution | Difficulty Distribution |
|---|---:|---|---|
| Beginner | 10 | fill_blank: 3, match: 3, mcq: 4 | easy: 10 |
| Junior Data Engineer | 10 | fill_blank: 2, match: 2, mcq: 3, short_answer: 3 | easy: 5, medium: 5 |
| Mid-Level Data Engineer | 10 | mcq: 2, scenario: 3, short_answer: 3, troubleshooting: 2 | medium: 8, hard: 2 |
| Senior Data Engineer | 10 | cost_optimization: 2, design_decision: 2, scenario: 3, troubleshooting: 3 | medium: 3, hard: 7 |
| Lead Data Engineer | 10 | architecture: 2, governance: 2, reliability: 2, stakeholder_impact: 2, trade_off: 2 | hard: 10 |
| Architect | 10 | cost_optimization: 2, enterprise_architecture: 2, governance: 2, reliability: 2, security: 2 | hard: 10 |

Concepts covered:

- Beginner: S3, IAM, Glue, Athena, file formats, messaging, CloudWatch, Glue Data Catalog, storage zones.
- Junior: partition pruning, Redshift, file formats, S3 ingestion, crawlers, Lambda, orchestration, IAM roles, Kinesis, CloudWatch troubleshooting.
- Mid-Level: Athena cost, Glue bookmarks, raw-to-curated pipelines, missing partitions, SQS, Redshift loading, Glue performance, Lake Formation, streaming, lake security.
- Senior: lakehouse ingestion, Athena cost spikes, Glue vs EMR, storage/warehouse costs, Lake Formation rollout, Kinesis incidents, Step Functions vs Airflow, data quality, Redshift performance, streaming cost.
- Lead: AWS platform architecture, Redshift vs Athena, governance adoption, ownership, reliability standards, multi-account platform, operating model, cost accountability, sensitive data, DR.
- Architect: enterprise platform, federated governance, FinOps, critical reliability, data lake security, data mesh, metadata/lineage, workload placement, multi-region DR, auditability.

Duplicate concepts detected:

- No duplicate concept strings within AWS.

Difficulty progression assessment:

- Strong progression and normalized difficulty labels.
- Lead and Architect are all `hard`, which is acceptable but loses nuance between senior leadership and enterprise architecture difficulty.

### Azure

| Level | Count | Type Distribution | Difficulty Distribution |
|---|---:|---|---|
| Beginner | 10 | fill_blank: 3, match: 3, mcq: 4 | easy: 10 |
| Junior Data Engineer | 10 | fill_blank: 2, match: 2, mcq: 3, short_answer: 3 | easy: 5, medium: 5 |
| Mid-Level Data Engineer | 10 | mcq: 2, scenario: 3, short_answer: 3, troubleshooting: 2 | medium: 8, hard: 2 |
| Senior Data Engineer | 10 | cost_optimization: 2, design_decision: 2, scenario: 3, troubleshooting: 3 | medium: 3, hard: 7 |
| Lead Data Engineer | 10 | architecture: 2, governance: 2, reliability: 2, stakeholder_impact: 2, trade_off: 2 | hard: 10 |
| Architect | 10 | cost_optimization: 2, enterprise_architecture: 2, governance: 2, reliability: 2, security: 2 | hard: 10 |

Concepts covered:

- Beginner: ADLS Gen2, ADF, Synapse, managed identities, Key Vault, messaging, Azure Monitor, Parquet, lake zones.
- Junior: linked services, RBAC, file formats, ADLS checks, private endpoints, Event Hubs, orchestration options, Key Vault, Purview, ADF troubleshooting.
- Mid-Level: partitioning, ADF parameters, raw-to-curated pipelines, copy failures, Service Bus, Synapse serving, Databricks performance, Purview, Event Hubs ingestion, security controls.
- Senior: Azure lakehouse ingestion, ADF incidents, ADF vs Databricks vs Synapse, cost controls, Purview rollout, Event Hubs lag, private networking, data quality, Synapse regression, streaming cost.
- Lead: Azure platform architecture, Synapse vs Databricks, governance adoption, ownership, reliability standards, multi-subscription platform, operating model, cost accountability, sensitive data, DR.
- Architect: enterprise platform, federated governance, FinOps, critical reliability, security architecture, data mesh, metadata/lineage, workload placement, multi-region DR, auditability.

Duplicate concepts detected:

- No duplicate concept strings within Azure.

Difficulty progression assessment:

- Strong progression and normalized difficulty labels.
- Lead and Architect are all `hard`, similar to AWS.

### Data Modeling

| Level | Count | Type Distribution | Difficulty Distribution |
|---|---:|---|---|
| Beginner | 10 | fill_blank: 3, match: 3, mcq: 4 | easy: 10 |
| Junior Data Engineer | 10 | fill_blank: 2, match: 2, mcq: 3, short_answer: 3 | easy: 3, medium: 7 |
| Mid-Level Data Engineer | 10 | mcq: 2, scenario: 3, short_answer: 3, troubleshooting: 2 | easy: 1, medium: 4, scenario: 4, hard: 1 |
| Senior Data Engineer | 10 | design_decision: 2, scenario: 3, trade_off: 2, troubleshooting: 3 | medium: 2, scenario: 3, hard: 5 |
| Lead Data Engineer | 10 | architecture: 2, governance: 2, reliability: 2, stakeholder_impact: 2, trade_off: 2 | medium: 2, scenario: 2, hard: 6 |
| Architect | 10 | cost_optimization: 1, enterprise_architecture: 2, governance: 2, platform_design: 2, reliability: 2, security: 1 | advanced: 5, expert: 5 |

Concepts covered:

- Beginner: entities, attributes, primary keys, foreign keys, facts, dimensions, OLTP/OLAP, grain, denormalization, modeling outputs.
- Junior: normalization, foreign keys, fact/dimension examples, fact grain, star schema, surrogate keys, SCD Type 1, SCD types, conformed dimensions, source-to-target mapping.
- Mid-Level: snowflake schema, many-to-many, grain mismatch, SCD Type 2 duplicates, schema evolution, event modeling, reporting models, natural key instability, data quality, data marts.
- Senior: dimensional design, metric disagreement, SCD Type 1 vs Type 2, denormalization trade-offs, semantic layer, schema breakage, Data Vault, ML vs reporting, PII, conformed dimension drift.
- Lead: enterprise standards, star vs snowflake, metric ownership, PII/access, model reliability, layered architecture, Data Vault vs marts, review process, backward compatibility, roadmap.
- Architect: enterprise standards, modeling platform, ownership governance, cloud warehouse cost, reliability architecture, security-aware design, canonical model, semantic governance, AI use cases, enterprise change management.

Duplicate concepts detected:

- No duplicate concept strings within Data Modeling.

Difficulty progression assessment:

- Strong pedagogical progression.
- Needs normalization because `scenario`, `advanced`, and `expert` appear as difficulty values.

### GCP / BigQuery

| Level | Count | Type Distribution | Difficulty Distribution |
|---|---:|---|---|
| Beginner | 10 | fill_blank: 3, match: 3, mcq: 4 | easy: 10 |
| Junior Data Engineer | 10 | fill_blank: 2, light_scenario: 2, mcq: 3, short_answer: 3 | easy: 2, medium: 8 |
| Mid-Level Data Engineer | 10 | mcq: 2, scenario: 3, short_answer: 3, troubleshooting: 2 | easy: 1, medium: 4, scenario: 4, hard: 1 |
| Senior Data Engineer | 10 | cost_optimization: 2, descriptive: 1, design_decision: 2, scenario: 2, troubleshooting: 3 | medium: 2, scenario: 3, hard: 5 |
| Lead Data Engineer | 10 | architecture: 2, governance: 2, reliability: 2, stakeholder_impact: 2, trade_off: 2 | medium: 2, scenario: 2, hard: 6 |
| Architect | 10 | cost_optimization: 2, enterprise_architecture: 1, governance: 2, multi_region: 2, reliability: 2, security: 1 | advanced: 5, expert: 5 |

Concepts covered:

- Beginner: BigQuery basics, datasets, tables, schemas, GCS loading, partitioning, optimization concepts, IAM, Composer, monitoring/audit.
- Junior: load jobs, bytes scanned, partition filters, CSV safety, Pub/Sub, service accounts, Dataflow, Composer, external tables, audit logs.
- Mid-Level: clustering, materialized views, partitioned ingestion, high bytes scanned, slots, streaming, Composer DAG design, permission issues, external tables, freshness monitoring.
- Senior: production BigQuery design, cost optimization, streaming lag, batch vs streaming, reservations/slots, Composer failure, external vs native tables, guardrails, IAM, schema evolution.
- Lead: GCP data platform architecture, reservations vs on-demand, incident communication, dataset access, SLOs, Dataflow templates, centralized vs domain datasets, VPC Service Controls, backfills, cost governance.
- Architect: enterprise GCP platform, multi-region strategy, column governance, FinOps, critical reliability, defense in depth, DR, data sharing, workload isolation, lineage/blast radius.

Duplicate concepts detected:

- No duplicate concept strings within GCP / BigQuery.

Difficulty progression assessment:

- Strong progression, but the domain label should be renamed from GCP / BigQuery to GCP if the product direction is now broader cloud coverage.
- Needs difficulty normalization because `scenario`, `advanced`, and `expert` appear as difficulty values.

### Python

| Level | Count | Type Distribution | Difficulty Distribution |
|---|---:|---|---|
| Beginner | 10 | fill_blank: 3, match: 3, mcq: 4 | easy: 10 |
| Junior Data Engineer | 10 | fill_blank: 2, light_scenario: 2, mcq: 3, short_answer: 3 | easy: 2, medium: 8 |
| Mid-Level Data Engineer | 10 | mcq: 2, scenario: 3, short_answer: 3, troubleshooting: 2 | easy: 1, medium: 4, scenario: 4, hard: 1 |
| Senior Data Engineer | 10 | descriptive: 1, design_decision: 3, scenario: 3, troubleshooting: 3 | medium: 2, scenario: 3, hard: 5 |
| Lead Data Engineer | 10 | architecture: 4, descriptive: 1, stakeholder_impact: 2, trade_off: 3 | medium: 2, scenario: 2, hard: 6 |
| Architect | 10 | cost_optimization: 2, enterprise_architecture: 2, governance: 2, reliability: 2, trade_off: 2 | advanced: 5, expert: 5 |

Concepts covered:

- Beginner: lists, dictionaries, file context manager, data structures, pandas DataFrame, exceptions, ETL steps, logging, JSON parsing, basic quality.
- Junior: CSV loading, environment variables, idempotency, API pagination, safe file writes, logging context, unit testing, bad records, memory-efficient iteration, function design.
- Mid-Level: pandas merge, chunked processing, API retry strategy, memory growth, schema validation, vectorization, incremental extraction, timezone bugs, dependency injection, pipeline tests.
- Senior: production ETL design, backfills, corruption incidents, pandas vs distributed processing, secrets, duplicate ingestion, package structure, observability, dependency failures, validation framework.
- Lead: shared ingestion framework, framework vs scripts, incidents, testing strategy, orchestration location, review standards, reusable quality library, build vs buy, migration planning, developer experience.
- Architect: Python platform, dependency governance, compute cost, reliability standards, Python vs SQL vs distributed engines, multi-tenant platform, sensitive data, FinOps, DR, ownership.

Duplicate concepts detected:

- No duplicate concept strings within Python.

Difficulty progression assessment:

- Strong progression from syntax/data handling to platform and operating-model questions.
- Needs difficulty normalization because `scenario`, `advanced`, and `expert` appear as difficulty values.

### SQL

| Level | Count | Type Distribution | Difficulty Distribution |
|---|---:|---|---|
| Beginner | 10 | fill_blank: 3, match: 3, mcq: 4 | easy: 10 |
| Junior Data Engineer | 10 | fill_blank: 2, light_scenario: 2, mcq: 3, short_answer: 3 | easy: 2, medium: 8 |
| Mid-Level Data Engineer | 10 | mcq: 2, scenario: 3, short_answer: 3, troubleshooting: 2 | easy: 1, medium: 4, scenario: 4, hard: 1 |
| Senior Data Engineer | 10 | descriptive: 2, design_decision: 3, scenario: 2, troubleshooting: 3 | medium: 2, scenario: 3, hard: 5 |
| Lead Data Engineer | 10 | architecture: 4, descriptive: 1, stakeholder_impact: 2, trade_off: 3 | medium: 2, scenario: 2, hard: 6 |
| Architect | 10 | cost_optimization: 2, enterprise_architecture: 2, governance: 2, reliability: 2, trade_off: 2 | advanced: 5, expert: 5 |

Concepts covered:

- Beginner: SELECT, WHERE, sorting, COUNT, GROUP BY, clauses, INNER JOIN, null checks, aggregates, data types.
- Junior: LEFT JOIN, HAVING, COUNT variants, DISTINCT, COALESCE, aliases, date filtering, logical query order, duplicate joins, LIMIT determinism.
- Mid-Level: window functions, deduplication, incremental models, join grain, sargable predicates, UNION vs UNION ALL, quality checks, late-arriving data, CTEs, slow query optimization.
- Senior: production SQL design, slow warehouse queries, metric regression, incremental strategy, data contracts, null semantics, materialization, SCDs, query correctness, PII handling.
- Lead: semantic governance, centralization vs autonomy, incident communication, layering, freshness vs cost, review standards, quality platform, denormalization, prioritization, migration.
- Architect: metric architecture, PII governance, warehouse cost controls, analytical reliability, lakehouse vs warehouse SQL, data product contracts, self-service analytics, FinOps, DR, standard vs engine-specific SQL.

Duplicate concepts detected:

- No duplicate concept strings within SQL.

Difficulty progression assessment:

- Strong progression from fundamentals to senior production ownership.
- Needs difficulty normalization because `scenario`, `advanced`, and `expert` appear as difficulty values.

### Terraform

| Level | Count | Type Distribution | Difficulty Distribution |
|---|---:|---|---|
| Beginner | 10 | fill_blank: 3, match: 3, mcq: 4 | easy: 10 |
| Junior Data Engineer | 10 | fill_blank: 1, light_scenario: 2, match: 1, mcq: 3, short_answer: 3 | easy: 2, medium: 8 |
| Mid-Level Data Engineer | 10 | mcq: 2, scenario: 3, short_answer: 3, troubleshooting: 2 | easy: 1, medium: 4, scenario: 4, hard: 1 |
| Senior Data Engineer | 10 | cost_optimization: 1, descriptive: 1, design_decision: 2, scenario: 3, troubleshooting: 3 | medium: 2, scenario: 3, hard: 5 |
| Lead Data Engineer | 10 | architecture: 2, governance: 2, reliability: 2, stakeholder_impact: 2, trade_off: 2 | medium: 2, scenario: 2, hard: 6 |
| Architect | 10 | cost_optimization: 2, enterprise_architecture: 2, governance: 2, reliability: 2, security: 1, trade_off: 1 | advanced: 5, expert: 5 |

Concepts covered:

- Beginner: IaC, providers, plan, workflow, state, variables, blocks, modules, remote state, data platform resources.
- Junior: plan review, environment naming, remote state locking, landing buckets, least privilege, drift, files, modules, sensitive outputs, tags/labels.
- Mid-Level: import, module versioning, CI/CD, state locks, `for_each`, `prevent_destroy`, environment promotion, unexpected replacement, data sources, IAM modules.
- Senior: IaC strategy, BigQuery governance, state drift, workspaces vs directories, policy as code, provider upgrades, cost controls, repo strategy, Composer as code, state sensitivity.
- Lead: platform standards, central modules vs custom Terraform, deletion risk, IAM governance, release reliability, multi-cloud structure, ownership, compliance evidence, backend resilience, adoption roadmap.
- Architect: enterprise IaC model, policy architecture, FinOps, control-plane reliability, secrets/state security, standardization vs innovation, multi-account foundations, drift at scale, chargeback, DR.

Duplicate concepts detected:

- No duplicate concept strings within Terraform.

Difficulty progression assessment:

- Strong progression.
- Needs difficulty normalization because `scenario`, `advanced`, and `expert` appear as difficulty values.

## Duplicate Question Detection

### Exact duplicate question text

These are exact question-text duplicates across different files. Some are acceptable generic prompts, but they reduce perceived variety in interview sessions:

- `What operating model would you recommend?`
  - `airflow_lead_trade_002`
  - `aws_lead_trade_007`
  - `azure_lead_trade_007`
- `What governance changes would you introduce?`
  - `airflow_lead_gov_008`
  - `data_modeling_lead_gov_004`
- `How would you plan the migration?`
  - `airflow_lead_stake_010`
  - `python_lead_stake_009`
- `What would you check?`
  - `airflow_mid_trouble_004`
  - `python_mid_trouble_008`
- `What enterprise architecture would you define?`
  - `aws_arch_enterprise_001`
  - `azure_arch_enterprise_001`
- `What reliability architecture would you require?`
  - `aws_arch_reliability_004`
  - `azure_arch_reliability_004`
- `What security architecture would you define?`
  - `aws_arch_security_005`
  - `azure_arch_security_005`
- `What metadata and lineage strategy would you put in place?`
  - `aws_arch_gov_007`
  - `azure_arch_gov_007`
- `How would you evaluate and respond?`
  - `aws_arch_reliability_009`
  - `azure_arch_reliability_009`
- `What controls and evidence would you design for?`
  - `aws_arch_security_010`
  - `azure_arch_security_010`
- `What reference architecture would you propose?`
  - `aws_lead_arch_001`
  - `azure_lead_arch_001`
- `How would you lead the rollout?`
  - `aws_lead_stakeholder_003`
  - `azure_lead_stakeholder_003`
- `How would you establish ownership and accountability?`
  - `aws_lead_gov_004`
  - `azure_lead_gov_004`
- `What reliability standards would you introduce?`
  - `aws_lead_reliability_005`
  - `azure_lead_reliability_005`
- `What governance controls would you prioritize?`
  - `aws_lead_gov_009`
  - `azure_lead_gov_009`
- `How would you troubleshoot the slowdown?`
  - `aws_mid_trouble_007`
  - `azure_mid_trouble_007`
- `What trade-offs would you discuss?`
  - `aws_senior_design_003`
  - `azure_senior_design_003`
  - `data_modeling_senior_trade_004`
  - `gcp_bigquery_senior_design_007`
  - `terraform_senior_design_004`
- `How would you reduce cost without hurting reliability?`
  - `aws_senior_cost_004`
  - `azure_senior_cost_004`
- `How would you diagnose and improve performance?`
  - `aws_senior_trouble_009`
  - `azure_senior_trouble_009`
- `How would you investigate and prevent recurrence?`
  - `azure_senior_trouble_002`
  - `python_senior_trouble_003`

### Near-duplicate pattern detection

The strongest near-duplicate clusters are:

- AWS and Azure cloud architecture prompts. Many differ mainly by cloud service names.
- Generic Lead/Architect governance prompts: ownership, access controls, cost accountability, reliability standards, auditability.
- Generic senior design prompts: "What trade-offs would you discuss?" is repeated across AWS, Azure, GCP, Terraform, and Data Modeling.
- Generic troubleshooting phrasing: "What would you check?" and "How would you troubleshoot the slowdown?"

Recommendation: keep the concepts, but rewrite question text so the scenario carries more domain-specific signal. For example:

- Instead of "What trade-offs would you discuss?", use "The Glue team wants serverless Spark, but platform operations prefers EMR for dependency control. How would you decide?"
- Instead of "What enterprise architecture would you define?", use "Your Azure tenant has restricted public endpoints, regulatory PII, and three regional data product teams. How would you design the platform?"

## Missing Concept Detection

### Missing standalone domains

The current v2 folder does not yet include these previously targeted domains:

- Databricks
- dbt
- Git
- Production Engineering

These are the weakest areas by absence, not by quality.

### Missing or underrepresented Data Engineering interview topics

Across all completed banks, these important topics are either missing or underrepresented:

- CDC patterns beyond high-level ingestion.
- Kafka as a non-cloud-specific streaming platform.
- dbt-specific modeling, tests, exposures, snapshots, incremental models, and deployment patterns.
- Git workflows for data teams: branching, pull requests, code review, release management, rollback, and conflict handling.
- Databricks-specific Delta Lake, Unity Catalog, Auto Loader, job clusters, DLT, medallion implementation, and Photon.
- Production Engineering as its own domain: SLOs, incident command, postmortems, observability, on-call, runbooks, release safety, capacity planning.
- Data privacy and compliance frameworks such as GDPR, HIPAA, PCI, retention policies, and right-to-delete workflows.
- Data contracts as an operational practice across producers and consumers.
- Lineage tooling beyond cloud catalog mentions.
- Testing strategy depth: unit, integration, contract, data quality, replay, backfill, and migration tests.
- Migration case studies: warehouse migration, Airflow/Composer migration, cloud-to-cloud migration, monolith-to-domain data products.
- ML/AI data platform concerns: feature stores, offline/online parity, embedding/vector data pipelines, evaluation datasets, model-monitoring data feeds.

### Missing concepts by existing domain

- Airflow: deferrable operators, datasets, task groups, trigger rules, executor choices, Airflow 2 asset scheduling, dataset-aware scheduling.
- AWS: Redshift Serverless, Glue streaming, Iceberg on AWS, EMR Serverless, MSK, DMS/CDC, IAM Access Analyzer, Macie.
- Azure: Fabric, Delta Lake/OneLake, Synapse dedicated vs serverless SQL depth, Azure Stream Analytics, Defender for Cloud, policy-as-code.
- Data Modeling: physical DDL design, indexing/clustering by warehouse, schema registry, data contracts, real example source-to-target mapping exercises.
- GCP / BigQuery: Dataplex, BigLake, BigQuery Omni, Dataform, policy tags depth, row access policies, Data Catalog/Dataplex governance split.
- Python: async APIs, multiprocessing, packaging/dependency locking, typing, Pydantic, CLI design, orchestration integration, secrets rotation.
- SQL: recursive CTEs, query plan interpretation, transaction isolation, merge/upsert syntax, stored procedure trade-offs, engine-specific SQL differences.
- Terraform: Terraform Cloud/Enterprise, OpenTofu discussion, Sentinel/OPA examples, provider aliasing, module testing, import blocks, state surgery.

## Overrepresented Topics

- Governance appears heavily in Lead and Architect across most domains.
- Cost optimization appears repeatedly in cloud and platform domains.
- Reliability/DR appears repeatedly in Lead and Architect.
- Generic architecture prompts are common at the highest levels.
- Cloud service mapping appears often in Beginner levels, which is fine, but future early-level banks should include more applied mini-scenarios.

This overrepresentation is not harmful for a senior interview simulator, but the wording should be diversified so users do not feel they are answering the same prompt with different product names.

## Weak Domains

Weak by absence:

1. Databricks
2. dbt
3. Git
4. Production Engineering

Weak by repetition risk:

1. AWS
2. Azure
3. Lead and Architect levels across cloud domains

Weak by difficulty-label consistency:

1. Airflow
2. Data Modeling
3. GCP / BigQuery
4. Python
5. SQL
6. Terraform

## Difficulty Progression Assessment

Overall progression is good:

- Beginner: mostly MCQ, fill_blank, match; all easy.
- Junior: mostly objective plus short_answer; easy to medium.
- Mid-Level: practical scenarios and troubleshooting begin.
- Senior: production scenarios, troubleshooting, design decisions, and cost trade-offs.
- Lead: architecture, governance, reliability, trade-offs, stakeholder impact.
- Architect: enterprise architecture, governance, reliability, cost, security.

Primary issue:

- Difficulty values are inconsistent. Suggested normalized set:
  - `easy`
  - `medium`
  - `hard`
  - `advanced`
  - `expert`

Do not use `scenario` as a difficulty value; scenario belongs in `type`.

## Recommendations

1. Complete missing domains next: Databricks, dbt, Git, Production Engineering.
2. Normalize difficulty labels across all banks.
3. Rename GCP / BigQuery user-facing domain to GCP if the product direction is broader GCP.
4. Rewrite exact duplicate prompts, especially AWS/Azure Lead and Architect questions.
5. Add more concrete incident/debugging questions with realistic symptoms, logs, or metrics.
6. Add data contract, CDC, lineage, privacy, and testing depth across multiple domains.
7. Add a lightweight duplicate-detection check to the validation script for exact question text and duplicate concepts within a domain.

## Release Readiness Assessment

The v2 question bank is strong enough for curated hybrid sessions across the 8 completed domains. The quality is especially good for SQL, Python, GCP / BigQuery, Terraform, Airflow, Data Modeling, AWS, and Azure as domain-only practice.

Before promoting this as a complete all-domain product, finish Databricks, dbt, Git, and Production Engineering, then perform one copy-edit pass to reduce repeated high-level prompt templates.
