# Toodledo MCP Server - Product Requirements Document

## 1. Executive Summary

### Purpose
Create a Model Context Protocol (MCP) server that enables Claude (via Claude Code and Claude Desktop) to interact with the Toodledo task management system.

### Goals
1. Enable reading tasks from Toodledo through Claude
2. Support creating tasks from transcribed paper notes
3. Provide task management capabilities within AI conversations
4. Start simple and expand functionality iteratively

### Success Criteria
- Claude can successfully retrieve and display Toodledo tasks
- Tasks can be created through natural language commands
- Server runs reliably with minimal configuration
- Authentication process is simple and user-friendly

## 2. User Stories

### Phase 1 - MVP (Read-Only)
- **As a user**, I want to view my Toodledo tasks from Claude so I can review my todo list during AI conversations
- **As a user**, I want to filter tasks by completion status so I can focus on incomplete items
- **As a user**, I want simple authentication that doesn't require complex OAuth setup

### Phase 2 - Basic CRUD
- **As a user**, I want to create new tasks from Claude so I can add items without leaving my conversation
- **As a user**, I want to edit existing tasks so I can update details and mark items complete
- **As a user**, I want to delete tasks so I can remove items that are no longer needed
- **As a user**, I want to create multiple tasks at once from transcribed paper notes

### Phase 3 - Advanced Features
- **As a user**, I want tasks automatically organized into appropriate folders based on content
- **As a user**, I want natural language dates converted to proper due dates
- **As a user**, I want duplicate detection to avoid creating the same task multiple times
- **As a user**, I want to sync paper todo lists stored as markdown files

## 3. Technical Requirements

### 3.1 MVP Requirements (Phase 1)

#### Authentication
- Use Toodledo App Token (simple 2-hour token)
- Store token in environment variable
- Manual refresh process (user gets new token from website)
- Clear error messages when token expires

#### MCP Tools
Single tool implementation:
- **get_tasks**
  - Optional filter by completion status (incomplete/complete/all)
  - Return task title, due date, folder, priority
  - Maximum 1000 tasks per request
  - Simple JSON response format

#### Technology Stack
- **Language:** Python 3.11+
- **MCP Framework:** fastmcp (latest version)
- **Dependencies:** Minimal (requests, python-dotenv)
- **Configuration:** Environment variables only

### 3.2 Phase 2 Requirements - Basic CRUD

#### Additional MCP Tools
- **create_task**
  - Required: title
  - Optional: folder, due date, priority, notes
  - Single task creation

- **create_tasks_batch**
  - Create up to 50 tasks in one request
  - Parse markdown checklist format
  - Return success/failure for each task

- **edit_task**
  - Update any task field
  - Support marking tasks complete

- **delete_task**
  - Delete by task ID
  - Confirmation of deletion

#### Organization Tools
- **get_folders** - List available folders with IDs
- **get_contexts** - List available contexts with IDs

### 3.3 Phase 3 Requirements - Advanced Features

#### OAuth2 Authentication (Optional)
- Full OAuth2 flow implementation
- Automatic token refresh
- Secure token storage
- PKCE support for security

#### Smart Features
- **Natural Language Processing**
  - Extract due dates from text ("next Monday", "tomorrow")
  - Infer priority from keywords ("urgent", "important")
  - Detect folder from content

- **Duplicate Detection**
  - Check for similar existing tasks
  - Configurable similarity threshold
  - Option to skip or update existing

- **Batch Processing**
  - Parse multiple file formats (markdown, plain text)
  - Support for daily briefing workflow
  - Progress reporting for large batches

## 4. Architecture Design

### 4.1 System Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│   Claude Code   │────▶│  MCP Server  │────▶│ Toodledo API │
│  Claude Desktop │◀────│   (FastMCP)  │◀────│   (HTTPS)    │
└─────────────────┘     └──────────────┘     └──────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │ .env Config  │
                        │ (App Token)  │
                        └──────────────┘
```

### 4.2 File Structure

```
toodledo-mcp/
├── main.py              # FastMCP server entry point
├── .env                 # Environment variables (token)
├── .env.example         # Template for configuration
├── pyproject.toml       # Poetry dependencies
├── poetry.lock          # Locked dependencies
├── README.md            # Setup and usage instructions
├── PRD.md              # This document
├── CHANGELOG.md        # Version history
│
├── tools/              # MCP tool implementations (Phase 2+)
│   ├── __init__.py
│   ├── get_tasks.py
│   ├── create_task.py
│   └── ...
│
├── utils/              # Utility functions (Phase 2+)
│   ├── __init__.py
│   ├── auth.py
│   └── validation.py
│
└── tests/              # Test files (Phase 2+)
    ├── __init__.py
    └── test_tools.py
```

### 4.3 Configuration Management

#### Environment Variables (.env)
```
# Required
TOODLEDO_ACCESS_TOKEN=your_app_token_here

# Optional (Phase 3)
TOODLEDO_CLIENT_ID=oauth_client_id
TOODLEDO_CLIENT_SECRET=oauth_client_secret
TOODLEDO_REDIRECT_URI=http://localhost:8000/callback
```

### 4.4 API Integration

#### Request Flow
1. Claude sends request to MCP server
2. MCP server validates request parameters
3. Server adds authentication token to API request
4. Server forwards request to Toodledo API
5. Response processed and returned to Claude

#### Error Handling
- Network timeouts: 5 second connect, 30 second read
- Token expiration: Clear message with refresh instructions
- API errors: User-friendly error messages
- Validation errors: Detailed parameter requirements

## 5. Implementation Phases

### Phase 1: MVP (Week 1)
**Goal:** Working read-only MCP server

**Deliverables:**
1. Project setup with Poetry
2. Single-file main.py implementation
3. get_tasks tool with basic filtering
4. Environment-based configuration
5. Basic documentation (README)

**Acceptance Criteria:**
- [ ] Server starts without errors
- [ ] Can retrieve tasks with valid token
- [ ] Clear error on invalid/expired token
- [ ] Tasks display correctly in Claude

### Phase 2: Basic CRUD (Week 2)
**Goal:** Full task management capabilities

**Deliverables:**
1. Modular tool structure
2. Create, edit, delete operations
3. Batch task creation
4. Organization list tools
5. Basic test suite

**Acceptance Criteria:**
- [ ] All CRUD operations functional
- [ ] Batch creation handles 50 tasks
- [ ] Folder/context lists retrieved
- [ ] Error handling for all operations

### Phase 3: Smart Features (Week 3)
**Goal:** Enhanced usability and automation

**Deliverables:**
1. Natural language date parsing
2. Smart folder assignment
3. Duplicate detection
4. Markdown file parsing
5. OAuth2 implementation (optional)

**Acceptance Criteria:**
- [ ] Dates parsed correctly
- [ ] Duplicates detected accurately
- [ ] Markdown lists converted properly
- [ ] OAuth flow works (if implemented)

### Phase 4: Production Ready (Week 4)
**Goal:** Polished, documented, reliable server

**Deliverables:**
1. Comprehensive documentation
2. Docker support (optional)
3. Performance optimizations
4. Claude Desktop configuration
5. Example workflows

**Acceptance Criteria:**
- [ ] All features thoroughly tested
- [ ] Documentation complete
- [ ] Performance acceptable (<1s response)
- [ ] Works in Claude Desktop

## 6. Non-Functional Requirements

### Performance
- Response time: <1 second for single operations
- Batch operations: <5 seconds for 50 tasks
- Memory usage: <100MB runtime
- Concurrent requests: Support 10 simultaneous

### Security
- No credentials in logs
- Secure token storage (file permissions 600)
- HTTPS only for API communication
- Input validation on all parameters

### Reliability
- Graceful handling of network issues
- Automatic retry with backoff
- Clear error messages
- No data loss on failures

### Usability
- Simple setup process (<5 minutes)
- Clear documentation with examples
- Intuitive tool names and parameters
- Helpful error messages

## 7. Testing Strategy

### Unit Tests (Phase 2+)
- Tool parameter validation
- API response parsing
- Error handling logic
- Date parsing functions

### Integration Tests
- End-to-end API calls
- Token expiration handling
- Batch operation limits
- Network error recovery

### Manual Testing
- Claude Code integration
- Various task formats
- Edge cases (empty lists, special characters)
- Performance with large task lists

## 8. Documentation Requirements

### README.md
- Quick start guide
- Installation instructions
- Configuration steps
- Basic usage examples
- Troubleshooting section

### API Reference (inline)
- Tool descriptions
- Parameter documentation
- Response formats
- Error codes

### Example Workflows
- Getting started with App Token
- Creating tasks from conversation
- Syncing paper todos
- Batch task creation

## 9. Future Enhancements (Post-MVP)

### Potential Features
1. Task templates for common items
2. Recurring task support
3. Task dependencies (parent/child)
4. Time tracking integration
5. Natural language search
6. Task recommendations based on context
7. Integration with calendar systems
8. Voice input support
9. Photo OCR for paper todos
10. Collaboration features

### Technical Improvements
1. Caching for performance
2. WebSocket support for real-time updates
3. Database for token/cache storage
4. Multi-user support
5. Rate limiting implementation
6. Metrics and monitoring
7. Automated testing pipeline
8. Cloud deployment options

## 10. Success Metrics

### Quantitative
- Setup time: <5 minutes
- Response time: <1 second average
- Error rate: <1%
- Token refresh frequency: <1 per day
- Batch success rate: >95%

### Qualitative
- User can manage tasks without leaving Claude
- Clear and helpful error messages
- Intuitive tool usage
- Reliable operation
- Smooth upgrade path from MVP to full features

## 11. Risk Assessment

### Technical Risks
1. **Token Expiration**
   - Impact: High
   - Mitigation: Clear messages, easy refresh process

2. **API Changes**
   - Impact: Medium
   - Mitigation: Version checking, documentation

3. **Rate Limiting**
   - Impact: Low
   - Mitigation: Batch operations, request throttling

### Operational Risks
1. **Complex Setup**
   - Impact: High
   - Mitigation: Start with simple App Token

2. **User Confusion**
   - Impact: Medium
   - Mitigation: Clear documentation, examples

3. **Data Loss**
   - Impact: High
   - Mitigation: Validation, confirmation prompts

## 12. Decision Log

### Decisions Made
1. **Start with App Token**: Simpler than OAuth, good for MVP
2. **Use FastMCP**: Proven framework, good documentation
3. **Python Implementation**: Fast development, good libraries
4. **Environment Variables**: Simple configuration management
5. **Single File MVP**: Reduce complexity for initial version

### Open Questions
1. Should we implement OAuth in Phase 3 or wait for user demand?
2. Is Docker support necessary for initial release?
3. Should we cache folder/context lists locally?
4. What's the optimal batch size for paper todo sync?
5. Should we support multiple Toodledo accounts?

## Appendix A: Working Document Workflow

### Location
`/Users/hom/Sync/MasterFiles/business/todo-daily-briefing/`

### File Format
```markdown
# Daily Tasks - 2024-01-15

## Work
- [ ] Review quarterly reports
- [ ] Call client about project
- [ ] Update documentation

## Personal
- [ ] Buy groceries
- [ ] Schedule dentist appointment
```

### Sync Process
1. User creates/updates markdown file
2. Claude reads file using Read tool
3. Claude parses tasks and metadata
4. Claude calls create_tasks_batch
5. Results reported to user
6. File optionally archived or cleared

## Appendix B: Example Conversations

### Example 1: View Tasks
```
User: "Show me my incomplete tasks"
Claude: [Calls get_tasks with comp=0]
Claude: "Here are your incomplete tasks:
1. Review quarterly reports (Due: Tomorrow)
2. Call client (Priority: High)
3. Update documentation (Folder: Work)"
```

### Example 2: Create Task
```
User: "Add a task to call the dentist tomorrow"
Claude: [Calls create_task with title="Call the dentist", duedate="2024-01-16"]
Claude: "I've added 'Call the dentist' to your tasks with a due date of tomorrow."
```

### Example 3: Batch Creation
```
User: "I have a list of tasks to add:
- Email team about meeting
- Review pull requests
- Update project timeline"
Claude: [Calls create_tasks_batch with 3 tasks]
Claude: "I've added 3 new tasks to your Toodledo account:
✓ Email team about meeting
✓ Review pull requests
✓ Update project timeline"
```