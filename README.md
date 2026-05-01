# HackerRank Orchestrate - Support Triage Agent

A terminal-based support triage agent that classifies and routes support tickets across three product ecosystems: HackerRank, Claude, and Visa.

## Overview

This agent processes support tickets and produces structured output with:
- **status**: whether to reply or escalate
- **product_area**: the relevant support category
- **response**: a user-facing answer (corpus-grounded or escalation message)
- **justification**: traceable explanation of the decision
- **request_type**: classification (product_issue, feature_request, bug, invalid)

## Architecture

```
Input (CSV) 
    ↓
[Classifier] → request_type, product_area, company inference
    ↓
[Retriever] → TF-IDF document matching from corpus
    ↓
[Risk Assessment] → detect security/fraud keywords
    ↓
[Escalation Logic] → decide replied vs escalated
    ↓
[Response Generator] → corpus-grounded or safe escalation message
    ↓
Output (CSV)
```

### Key Design Decisions

1. **Document Retrieval**: Uses TF-IDF + cosine similarity instead of naive keyword counting
   - Precomputes vectors for each company's corpus
   - Returns confidence scores for all matches
   - Semantic ranking of documents

2. **Company Inference**: When company field is missing
   - Uses keyword matching (HackerRank: "test", "assessment"; Claude: "api", "model"; Visa: "card", "fraud")
   - Counts keyword overlap to determine best match

3. **Escalation Strategy**:
   - High-risk: fraud, security, unauthorized access
   - Bugs: always escalated to engineering
   - Sensitive areas: billing, account access, fraud (unless high confidence)
   - No relevant docs: escalate rather than hallucinate
   - Disputes/refunds: always escalated

4. **Response Generation**:
   - Never hallucinates policies or generic troubleshooting
   - Extracts relevant sections from corpus OR generates safe escalation message
   - Feature requests get acknowledgment responses

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Verify corpus is present**:
   - `../data/claude/` — Claude Help Center docs
   - `../data/hackerrank/` — HackerRank support docs
   - `../data/visa/` — Visa support docs

## Usage

### Run the Agent

```bash
cd code/
python main.py
```

The agent will:
1. Load and index the support corpus (~7.8MB, takes 5-10 seconds)
2. Process each ticket in `../support_tickets/support_tickets.csv`
3. Write predictions to `../support_tickets/output.csv`

### Output Format

`output.csv` will have 5 columns:
| Column | Example |
|--------|---------|
| status | "replied" or "escalated" |
| product_area | "assessments", "api_authentication", "payments_transactions" |
| response | "Based on our documentation: ...[extracted text]..." |
| justification | "Request: product_issue \| Area: assessments \| Company: HackerRank \| Match: 0.82 \| Decision: REPLIED (answer_from_corpus)" |
| request_type | "product_issue", "bug", "feature_request", "invalid" |

## Key Modules

### `main.py`
- Entry point
- Coordinates all components
- Handles I/O (CSV read/write)
- Tracks statistics

### `classifier.py`
- **`infer_company()`**: Infer company from keywords if missing
- **`classify_request()`**: Classify as product_issue, feature_request, bug, or invalid
- **`classify_product_area()`**: Route to specific support category
- **`is_invalid()`**: Check if request is too vague

### `retriever.py`
- **`DocumentRetriever`**: TF-IDF-based document ranking
  - Precomputes vectors for fast retrieval
  - Returns both document and confidence score
  - Supports single-company and cross-company search
- **`load_docs()`**: Load all corpus files

### `risk.py`
- **`assess_risk()`**: Detect high-risk keywords (fraud, stolen, unauthorized, etc.)
- Returns: "high", "medium", or "low"

### `escalation.py`
- **`assess_escalation()`**: Comprehensive escalation decision
- Checks: risk level, request type, sensitive areas, doc confidence, disputes
- Returns: ("replied" or "escalated", reason_code)

### `responder.py`
- **`extract_relevant_section()`**: Find best paragraph from corpus
- **`generate_response()`**: Build corpus-grounded or safe escalation response
- **`build_justification()`**: Create traceable decision explanation

## Testing

### Against Sample Data

Test your implementation against sample tickets:

```python
# In code/
import pandas as pd
from main import *

# Load and manually test a few rows
sample = pd.read_csv("../support_tickets/sample_support_tickets.csv")
print(sample[["Issue", "Response", "Product Area", "Status", "Request Type"]].head())

# Run your agent and compare
```

### Validation Checklist

- [ ] No hallucinated policies (all responses from corpus or safe escalations)
- [ ] Company inference working (test with `company_field = None`)
- [ ] Retrieval scoring sensible (high scores for exact matches, low for mismatches)
- [ ] Escalation logic capturing bugs, fraud, sensitive areas
- [ ] Output CSV has 5 columns and matches schema

## Determinism & Reproducibility

- **Seeding**: Retriever deterministic (TF-IDF/cosine similarity, no randomness)
- **Dependencies**: Pinned in `requirements.txt`
- **Reproducibility**: Same input → same output every time

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sklearn'"
**Solution**: `pip install scikit-learn`

### Issue: Corpus not loading
**Solution**: Check paths:
```bash
ls ../data/claude/
ls ../data/hackerrank/
ls ../data/visa/
```

### Issue: Very low match scores (<0.1) for all queries
**Solution**: Check that corpus documents are loaded properly. Print sample doc size:
```python
docs = load_docs()
print(f"Claude docs: {len(docs['Claude'])}, avg size: {sum(len(d) for d in docs['Claude']) / len(docs['Claude']) if docs['Claude'] else 0:.0f}")
```

## Performance Notes

- **Indexing**: First run takes 5-10 seconds (precomputes TF-IDF for ~7000+ docs)
- **Per-ticket**: ~10-50ms average
- **Full run**: ~1-2 seconds for 30 tickets

## Design Trade-offs

| Aspect | Choice | Why |
|--------|--------|-----|
| Retrieval | TF-IDF | Fast, deterministic, proven for corpus search |
| Company inference | Keywords | Simple, interpretable, works well for distinct products |
| Escalation | Rule-based | Explainable, auditable, safe (favors escalation over hallucination) |
| Response | Corpus-grounded | Avoids hallucination penalty, better for judge interview |

## Future Improvements

1. **Semantic Search**: Use embeddings (sentence-transformers) for better semantic matching
2. **Hierarchical Chunking**: Split documents into sections for more granular retrieval
3. **Multi-turn Conversation**: Track ticket history and context
4. **LLM Summarization**: Use Claude to summarize relevant doc sections
5. **Active Learning**: Flag uncertain cases for human feedback

## Judge Interview Notes

Be prepared to explain:
- Why TF-IDF instead of naive keyword counting
- How company inference works and edge cases
- Escalation logic (especially for sensitive areas)
- Why responses are corpus-grounded and not hallucinated
- Trade-offs made (precision vs recall, safety vs coverage)

## Author Notes

This solution prioritizes:
1. **Safety**: Escalates when unsure rather than hallucinating
2. **Traceability**: Every decision logged with confidence scores and reasons
3. **Corpus-fidelity**: Responses extracted from provided docs, not invented
4. **Simplicity**: Rule-based logic is interpretable and auditable