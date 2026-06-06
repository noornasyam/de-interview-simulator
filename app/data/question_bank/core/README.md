# Core Question Bank

This folder stores cloud-neutral questions for Data Engineer, Senior Data Engineer, Lead Data Engineer, and Architect preparation.

Use `core` for skills that apply across GCP, AWS, Azure, and multi-cloud roles:

- `sql`
- `python`
- `terraform`
- `git`
- `data_modeling`
- `streaming`
- `architecture`

Each domain has two tracks:

- `certification`: objective questions such as `mcq` and `fill_blank`
- `interview`: scenario and rubric-based questions

## Question Schema

Question files should be JSON arrays. Recommended filename pattern:

```text
level0.json
junior.json
mid_level.json
senior.json
lead.json
architect.json
```

Recommended fields:

```json
{
  "id": "sql-mid-001",
  "role_targets": ["data_engineer", "senior_data_engineer"],
  "platform": "core",
  "cloud": null,
  "level": "Mid-Level",
  "mode": "interview",
  "type": "interview",
  "domain": "sql",
  "category": "query_optimization",
  "difficulty": 5,
  "scenario": "",
  "question": "",
  "options": [],
  "correct_answer": "",
  "acceptable_answers": [],
  "expected_answer": "",
  "expected_points": [
    {
      "point": "Uses partition pruning",
      "keywords": ["partition", "pruning", "filter"],
      "weight": 20
    }
  ],
  "rubric": {
    "pass_score": 70
  },
  "explanation": "",
  "key_takeaways": [],
  "follow_ups": []
}
```

## Adding Questions

Add new questions to the domain that best represents the skill being tested. For example:

- SQL joins and window functions: `core/sql`
- Python data processing: `core/python`
- Terraform state and modules: `core/terraform`
- Git branching and pull requests: `core/git`
- Facts, dimensions, and grain: `core/data_modeling`
- Kafka/Pub/Sub/Kinesis concepts without vendor lock-in: `core/streaming`
- System design and trade-offs: `core/architecture`

Keep `difficulty` numeric from `1` to `10`.

## Domains And Cloud Providers

Use `core` when the question is cloud-neutral. Use the `cloud` question bank when the question depends on a named provider or provider-specific service.

Examples:

- Cloud-neutral: "Explain idempotent pipeline design."
- GCP-specific: "When would you use BigQuery partitioning?"
- AWS-specific: "How would you secure an S3 data lake?"
- Azure-specific: "How would you orchestrate with Azure Data Factory?"
