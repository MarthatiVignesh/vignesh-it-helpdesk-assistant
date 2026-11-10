# IT Helpdesk Assistant - Agent Specification

## 1. Goal

Build an AI-powered IT Helpdesk Assistant for TechNova Solutions. The assistant helps employees solve common IT problems related to Passwords, VPN, and Email, and classifies support requests.

## 2. Available Tools

### Tool 1: classify_ticket(description)

Purpose: Classifies IT support issues into categories and priorities.

Categories:
- Password
- VPN
- Email
- Unknown

Priorities:
- Low
- Medium
- High

### Tool 2: search_docs(question)

Purpose: Searches the IT Helpdesk Guide using Retrieval-Augmented Generation (RAG) and generates answers using relevant document chunks.

## 3. Agent Rules

1. Use search_docs for IT how-to and troubleshooting questions.
2. Use classify_ticket when an employee explicitly asks to raise a ticket.
3. Refuse questions unrelated to IT support.
4. Never ask employees to reveal passwords.
5. Never reveal passwords.
6. Use only information available in the IT Helpdesk Guide for troubleshooting answers.
7. Print the selected tool for every tool-based request.
8. Return clear and helpful responses.
9. Never claim that a ticket has been submitted or assigned.
10. Explain that classification does not submit an actual ticket.

## 4. Expected Behaviour

### Example 1
Question: How do I reset my password?
Selected tool: search_docs
Expected result: Provide password reset instructions from the IT Helpdesk Guide.

### Example 2
Question: My VPN keeps disconnecting. Please raise a ticket.
Selected tool: classify_ticket
Expected result:
- Category: VPN
- Priority: High

### Example 3
Question: What is the company leave policy?
Selected tool: No tool
Expected result: Politely refuse because the question is unrelated to IT support.
