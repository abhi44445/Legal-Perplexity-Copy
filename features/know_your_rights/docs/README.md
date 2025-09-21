# Know Your Rights - Feature Documentation

## Overview

The **Know Your Rights** feature provides constitutional guidance for real-world legal situations. Users can describe scenarios like bribery, threats, harassment, or workplace issues and receive AI-powered legal advice based on the Indian Constitution, complete with citations and actionable recommendations.

## Features

### Core Functionality
- **Scenario-based Input**: Six predefined scenarios (bribery, threats, harassment, online harassment, workplace, other)
- **Dynamic AI Analysis**: Reuses existing RAG system with specialized prompts
- **Constitutional Foundation**: All responses grounded in Indian Constitution and law
- **Actionable Guidance**: Specific recommendations with urgency classification
- **Citation System**: Legal references with constitutional articles and statutes

### User Interface
- **Responsive Design**: Mobile-friendly with Tailwind CSS
- **Interactive Scenario Selection**: Visual cards with context-aware placeholders
- **Real-time Validation**: Form validation with character limits
- **Results Display**: Structured output with copy/download functionality
- **Accessibility**: ARIA labels and keyboard navigation

### Backend Architecture
- **FastAPI Integration**: RESTful API endpoints
- **RAG Reuse**: Leverages existing vector store and retrieval system
- **Schema Validation**: Strict Pydantic models
- **PII Protection**: Automatic sanitization in logs
- **Error Handling**: Graceful degradation with fallback responses

## API Endpoints

### POST `/api/know-your-rights/query`

Main endpoint for processing rights queries.

**Request:**
```json
{
  "user_id": "optional_user_identifier",
  "scenario": "bribe|threat|harassment|online_harassment|workplace|other",
  "text": "Detailed situation description",
  "language": "en"
}
```

**Response:**
```json
{
  "legal_advice": "Detailed constitutional guidance...",
  "citations": [
    {
      "type": "constitution",
      "reference": "Article 21",
      "link": null
    }
  ],
  "recommended_actions": ["document_incident", "contact_authorities"],
  "urgency": "medium",
  "follow_up_questions": ["Do you have evidence?"],
  "disclaimer": "This is informational only...",
  "source_docs": [
    {
      "id": "doc_1",
      "score": 0.9,
      "snippet": "Constitutional text..."
    }
  ]
}
```

### POST `/api/know-your-rights/validate`

Validation endpoint for evaluation and fine-tuning.

**Request:**
```json
{
  "output_id": "unique_output_id",
  "expected": {"urgency": "high", "citations_count": 2},
  "score": 0.85,
  "notes": "Good constitutional grounding"
}
```

### GET `/api/know-your-rights/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Know Your Rights service is operational"
}
```

## File Structure

```
features/know_your_rights/
├── backend/
│   ├── router.py              # FastAPI router with endpoints
│   └── service.py             # Core business logic
├── frontend/
│   ├── KnowYourRightsPage.tsx # Main React component
│   ├── types.ts               # TypeScript interfaces
│   └── useKnowYourRights.ts   # Custom React hook
├── tests/
│   ├── nyar.spec.ts           # Playwright E2E tests
│   └── test_service.py        # Python unit tests
├── docs/
│   ├── README.md              # This file
│   └── golden/
│       └── golden_dataset.py  # Evaluation dataset
└── mcp/
    ├── mcp_check.py           # Model connectivity check
    ├── validation_harness.py  # Validation script
    └── evaluate.py            # Automated evaluation
```

## Usage

### Running Locally

1. **Start Backend:**
   ```bash
   cd /path/to/repo
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Feature:**
   Navigate to `http://localhost:5174/know-your-rights`

### Environment Variables

Required environment variables (same as existing system):
```env
OPENROUTER_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
CLAUDE_API_KEY=your_key_here
```

## Testing

### Playwright E2E Tests

```bash
cd features/know_your_rights/tests
npx playwright test nyar.spec.ts
```

**Key Tests:**
- Dynamic response validation (different inputs → different outputs)
- Citation presence and structure
- Urgency classification accuracy
- Disclaimer requirements
- Error handling

### Python Unit Tests

```bash
cd features/know_your_rights/tests
pytest test_service.py -v
```

**Test Coverage:**
- Input sanitization and validation
- Citation extraction (constitutional, statutory, case law)
- Urgency determination logic
- Action recommendation generation
- PII redaction utilities

### Model Connectivity Check

```bash
cd features/know_your_rights/mcp
python mcp_check.py
```

Validates:
- API endpoint availability
- Response schema compliance
- Model output quality
- Response time performance

### Automated Evaluation

```bash
cd features/know_your_rights/mcp
python evaluate.py --report
```

Runs golden dataset scenarios and generates:
- Pass/fail rates by scenario type
- Citation accuracy metrics
- Fine-tuning recommendations
- Detailed performance reports

## Quality Assurance

### Golden Dataset

Eight curated test scenarios covering:
- Police bribery with detailed context
- Family safety threats
- Workplace sexual harassment
- Online doxxing and harassment
- Caste-based discrimination
- Government corruption
- Illegal eviction threats
- Public transport harassment

### Validation Criteria

**Critical Requirements (must pass):**
- Citations present in response
- Disclaimer included
- Constitutional grounding

**Quality Metrics:**
- Response length (200-2000 characters)
- Urgency classification accuracy
- Specific action recommendations
- Context-aware responses

**Pass Thresholds:**
- Individual scenario: 70% of checks pass
- Overall system: 6/8 scenarios pass, <70% average score

### Anti-Hardcoding Measures

**Dynamic Response Testing:**
- Same scenario, different inputs must produce different responses
- User-specific details must appear in responses
- Empty retrieval must trigger low-confidence responses

**Schema Validation:**
- All responses follow strict JSON schema
- Enumerated values for urgency and actions
- Required fields validation

## Security & Privacy

### PII Protection

Automatic redaction in logs:
- Phone numbers → `[PHONE_REDACTED]`
- Email addresses → `[EMAIL_REDACTED]`
- Names → `[NAME_REDACTED]`
- Addresses → `[ADDRESS_REDACTED]`

### Input Sanitization

- Length limits (10-2000 characters)
- Dangerous pattern detection
- Script injection prevention
- SQL injection protection

### Legal Disclaimer

Every response includes:
> "This is informational only and not legal advice. Consult a qualified lawyer for legal advice."

## Performance

### Response Times
- Target: <30 seconds for typical queries
- Timeout: 120 seconds maximum
- Monitoring: Built-in performance tracking

### Scalability
- Reuses existing vector store (no duplication)
- Stateless service design
- Efficient caching with LRU cache

## Integration

### Existing System Integration

**Vector Store:** Reuses `ConstitutionDatabase` from existing system
**RAG Pipeline:** Leverages `ConstitutionRAG.retrieve_relevant_context()`
**Model Client:** Uses same OpenRouter API configuration
**Frontend:** Integrates with existing React app and styling

**No Breaking Changes:** Constitution Chat functionality preserved

### API Service Integration

Added endpoints to existing `frontend/src/services/api.ts`:
```typescript
knowYourRights: {
  query: async (request) => { /* implementation */ },
  validate: async (validationRequest) => { /* implementation */ },
  healthCheck: async () => { /* implementation */ }
}
```

## Troubleshooting

### Common Issues

**1. "RAG system not available" error:**
- Check if vectorstore exists: `ls vectorstore/constitution_faiss/`
- Recreate if needed: `python recreate_vectorstore.py`

**2. Long response times (>2 minutes):**
- Check API key configuration
- Verify model endpoint connectivity
- Monitor system resources

**3. "Connection refused" error:**
- Ensure backend server is running on port 8000
- Check CORS configuration in main.py

**4. Missing citations in responses:**
- Verify vector store contains constitutional content
- Check citation extraction regex patterns
- Review prompt templates for citation emphasis

### Debug Commands

```bash
# Check API health
curl http://localhost:8000/api/know-your-rights/health

# Test basic query
curl -X POST http://localhost:8000/api/know-your-rights/query \
  -H "Content-Type: application/json" \
  -d '{"scenario": "other", "text": "What are my basic rights?", "language": "en"}'

# Run MCP validation
python features/know_your_rights/mcp/mcp_check.py

# Run evaluation suite
python features/know_your_rights/mcp/evaluate.py
```

## Roadmap & Extensions

### Planned Enhancements
- Multi-language support (Hindi, regional languages)
- Voice input/output capabilities
- Integration with legal aid directories
- Emergency contact integration
- Document template generation

### Fine-tuning Opportunities
- Scenario-specific prompt optimization
- Regional law integration
- Case law database expansion
- Response personalization

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review test logs and validation results
3. Run MCP checks for model connectivity
4. Examine API logs for error details

## License & Disclaimer

This feature is part of the Legal Perplexity system and inherits the same license. All responses include appropriate legal disclaimers. The system is designed for informational purposes only and does not constitute legal advice.