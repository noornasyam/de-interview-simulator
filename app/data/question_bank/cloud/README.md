# Cloud Question Bank

This folder stores provider-specific questions for GCP, AWS, and Azure.

Use `cloud` when the question depends on a named cloud provider, service, permission model, pricing behavior, monitoring tool, or architecture pattern.

Each provider has two tracks:

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
  "id": "gcp-bq-mid-001",
  "role_targets": ["data_engineer", "senior_data_engineer"],
  "platform": "GCP",
  "cloud": "gcp",
  "level": "Mid-Level",
  "mode": "interview",
  "type": "interview",
  "domain": "bigquery",
  "category": "cloud_gcp",
  "difficulty": 5,
  "scenario": "",
  "question": "",
  "options": [],
  "correct_answer": "",
  "acceptable_answers": [],
  "expected_answer": "",
  "expected_points": [
    {
      "point": "Mentions partitioning or clustering",
      "keywords": ["partition", "cluster", "clustering"],
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

Add provider-specific questions under:

- `cloud/gcp`
- `cloud/aws`
- `cloud/azure`

Use provider-specific service names in `domain` when useful, such as:

- `bigquery`
- `cloud_storage`
- `pubsub`
- `s3`
- `redshift`
- `glue`
- `blob_storage`
- `synapse`
- `data_factory`

## Domains And Cloud Providers

Use `category` for broad reporting, such as:

- `cloud_gcp`
- `cloud_aws`
- `cloud_azure`
- `security`
- `monitoring`
- `cost`
- `architecture`

Use `domain` for the specific technical area or service.

Cloud questions can still include cross-cutting topics like security, monitoring, and cost, but they should be anchored in a specific provider.
