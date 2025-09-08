# Story-Goal MCP Examples

Real-world examples of using the Story-Goal MCP server for different development scenarios.

## 🚀 Getting Started Example

Complete walkthrough from zero to tracking your first goal:

```bash
# 1. Create your user workspace
python3 story_goal_mcp.py handshake dev123 "Alex Developer"
# Returns: {"user_key": "dev123", "goals": 0, "stories": 0, "active_stories": 0}

# 2. Create your first goal
python3 story_goal_mcp.py create-goal dev123 \
  "Build Personal Blog" \
  "Create a blog where I can share technical articles and thoughts" \
  "Blog is live with 5+ published articles"

# 3. Break it down into stories
python3 story_goal_mcp.py create-story dev123 \
  "Blog Homepage" \
  "As a visitor" \
  "I want to see recent blog posts" \
  "So that I can discover interesting content"

python3 story_goal_mcp.py create-story dev123 \
  "Article Writing Interface" \
  "As a blogger" \
  "I want to write posts in Markdown" \
  "So that I can focus on content, not formatting"

# 4. Check your progress
python3 story_goal_mcp.py list-goals dev123
python3 story_goal_mcp.py list-stories dev123
```

## 📱 Mobile App Development

Building a mobile app with user-focused stories:

```bash
# Sprint Goal
python3 story_goal_mcp.py create-goal mobile-dev \
  "Fitness Tracker MVP" \
  "Users can track workouts and see progress over time" \
  "100+ daily active users logging workouts"

# Core user journeys
python3 story_goal_mcp.py create-story mobile-dev \
  "Workout Logging" \
  "As a fitness enthusiast" \
  "I want to quickly log my workout" \
  "So that I can track progress without disrupting my routine"

python3 story_goal_mcp.py create-story mobile-dev \
  "Progress Visualization" \
  "As a user" \
  "I want to see my fitness trends over time" \
  "So that I stay motivated and can adjust my routine"

python3 story_goal_mcp.py create-story mobile-dev \
  "Offline Capability" \
  "As a gym user" \
  "I want to log workouts without internet" \
  "So that poor cell coverage doesn't break my tracking"
```

## 🏢 Enterprise Feature Development

Building business software with stakeholder value:

```bash
# Business Objective
python3 story_goal_mcp.py create-goal enterprise-team \
  "Customer Portal Self-Service" \
  "Reduce support ticket volume by enabling customer self-service" \
  "30% reduction in support tickets, 90%+ customer satisfaction"

# Stakeholder-driven stories
python3 story_goal_mcp.py create-story enterprise-team \
  "Account Information Access" \
  "As a customer" \
  "I want to view my account details and billing history" \
  "So that I don't need to call support for basic information"

python3 story_goal_mcp.py create-story enterprise-team \
  "Ticket Status Tracking" \
  "As a customer" \
  "I want to see real-time status of my support requests" \
  "So that I know what's happening and can plan accordingly"

python3 story_goal_mcp.py create-story enterprise-team \
  "Knowledge Base Integration" \
  "As a customer" \
  "I want to search help articles from my account page" \
  "So that I can solve problems myself quickly"
```

## 🐛 Bug Fixing as User Stories

Reframe bugs as user value:

```bash
# Bug Goal (focused on user impact)
python3 story_goal_mcp.py create-goal bug-squad \
  "Checkout Flow Reliability" \
  "Users can complete purchases without frustration or errors" \
  "Cart abandonment rate below 10%, payment success rate >99%"

# Bug stories with user context
python3 story_goal_mcp.py create-story bug-squad \
  "Payment Processing Error Handling" \
  "As a customer" \
  "I want clear error messages when my payment fails" \
  "So that I know exactly how to fix the issue and complete my purchase"

python3 story_goal_mcp.py create-story bug-squad \
  "Cart Persistence" \
  "As a shopper" \
  "I want my cart items to remain when I return later" \
  "So that I don't lose my selection and can complete purchase when ready"
```

## 🔧 Technical Debt as Stories

Make technical work outcome-focused:

```bash
# Technical Goal with Business Value
python3 story_goal_mcp.py create-goal tech-lead \
  "API Performance Optimization" \
  "Fast, reliable API responses that support business growth" \
  "API response times <200ms, supports 10x current traffic"

# Technical stories with user impact
python3 story_goal_mcp.py create-story tech-lead \
  "Database Query Optimization" \
  "As an API user" \
  "I want faster response times for data queries" \
  "So that my application feels responsive and users don't abandon actions"

python3 story_goal_mcp.py create-story tech-lead \
  "Caching Layer Implementation" \
  "As a system administrator" \
  "I want reduced database load during traffic spikes" \
  "So that the system remains stable and performant for all users"
```

## 👥 Team Collaboration

Multiple developers working toward shared goals:

```bash
# Shared goal, different developers
python3 story_goal_mcp.py create-goal frontend-dev \
  "E-commerce Checkout Redesign" \
  "Streamlined checkout process that increases conversion" \
  "Checkout completion rate >85%, average time <3 minutes"

python3 story_goal_mcp.py create-goal backend-dev \
  "E-commerce Checkout Redesign" \
  "Streamlined checkout process that increases conversion" \
  "Checkout completion rate >85%, average time <3 minutes"

# Frontend stories
python3 story_goal_mcp.py create-story frontend-dev \
  "One-Page Checkout" \
  "As a customer" \
  "I want all checkout steps on one page" \
  "So that I can complete my purchase quickly without confusion"

# Backend stories  
python3 story_goal_mcp.py create-story backend-dev \
  "Payment Processing Pipeline" \
  "As a customer" \
  "I want my payment to process securely and quickly" \
  "So that I can complete purchases with confidence"
```

## 📊 Progress Tracking Patterns

How to use phases effectively:

```bash
# Story starts in "defining" phase
python3 story_goal_mcp.py create-story dev123 \
  "User Profile Management" \
  "As a user" \
  "I want to update my profile information" \
  "So that my account reflects current details"

# Move through phases with progress updates
# TODO: These commands need to be implemented
python3 story_goal_mcp.py update-story dev123 story-id \
  "developing" \
  "Started implementing profile edit form with validation"

python3 story_goal_mcp.py update-story dev123 story-id \
  "validating" \
  "Form complete, running tests and getting user feedback"

python3 story_goal_mcp.py update-story dev123 story-id \
  "complete" \
  "Feature deployed, users can successfully update profiles"
```

## 🎯 Goal Achievement Patterns

Structuring goals for success:

### Feature Goals
```bash
# Good: Outcome-focused with measurable success
python3 story_goal_mcp.py create-goal team \
  "User Onboarding Experience" \
  "New users understand and can use core features immediately" \
  "90%+ onboarding completion, time-to-first-value <5 minutes"
```

### Performance Goals  
```bash
python3 story_goal_mcp.py create-goal devops \
  "System Reliability" \
  "Users experience consistent, fast service" \
  "99.9% uptime, <100ms response times, zero data loss"
```

### Learning Goals
```bash
python3 story_goal_mcp.py create-goal individual \
  "GraphQL Mastery" \
  "Confident building efficient GraphQL APIs" \
  "Built production GraphQL service, mentored 2 team members"
```

## 🔍 Querying Your Data

Find specific stories and track progress:

```bash
# List all goals with story counts
python3 story_goal_mcp.py list-goals your-username

# Filter stories by goal
python3 story_goal_mcp.py list-stories your-username goal-id-here

# Filter stories by phase
python3 story_goal_mcp.py list-stories your-username "" "developing"

# See current active work
python3 story_goal_mcp.py list-stories your-username "" "developing"
python3 story_goal_mcp.py list-stories your-username "" "validating"
```

## 💭 Story Writing Tips

### Good Story Structure
```
Title: "Password Reset Flow"
As a: "As a user who forgot their password"
I want: "I want to reset my password via email"
So that: "So that I can regain access to my account quickly and securely"
```

### Common Patterns

**User Stories:**
- As a [user type], I want [capability], so that [benefit]

**Developer Stories:**
- As a developer, I want [tool/system], so that [development benefit]

**Stakeholder Stories:**  
- As a business owner, I want [metric/outcome], so that [business value]

**System Stories:**
- As a system administrator, I want [capability], so that [operational benefit]

---

*These examples show how Story-Goal MCP transforms development from task-checking to value-delivery.*