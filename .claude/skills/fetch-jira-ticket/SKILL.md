---
name: fetch-jira-ticket
description: Fetch a Jira ticket using the Jira MCP and extract key details into a structured summary. Use when the user wants to retrieve, view, or get information about a Jira ticket.
---

Fetch a Jira ticket using the Jira MCP and extract key details into a structured summary.

## Rules

- **Input Validation**: A Jira ticket ID must be provided (e.g., `JED-1204`, `PROJ-123`). If not provided, STOP and ask the user for the ticket ID.

- **Fetch via MCP**: Use the Jira MCP tool to retrieve the ticket. If the MCP call fails, report the error clearly and do not proceed.

- **Extract Key Details**: Parse and present the following fields from the ticket:
  1. **Title**: The ticket summary/title.
  2. **Description**: Full description text. Preserve formatting where possible.
  3. **Acceptance Criteria**: Extract if present (often in description or a custom field).
  4. **Implementation Plan**: Extract if present (often in description or a custom field).
  5. **Metadata**: Include:
     - Status
     - Priority
     - Assignee
     - Reporter
     - Created date
     - Updated date
     - Labels (if any)
     - Sprint (if applicable)
  6. **Comments**: List all comments with author and timestamp.

- **Attachments and Images**: Do **NOT** fetch attachments or images from Jira. Instead:
  - For attachments, first check if you can find them in the project, if not, add placeholder links (e.g., `[Attachment: <filename>]`)
  - For images, first check if you can find them in the project, if not, add placeholder links (e.g., `[Image: <filename or description>]`)
  - Do not download or embed attachment or image content

- **Output Format**: Present the ticket information in a clean markdown structure saved to `TICKET_INFO_<Ticket_num>.md` in the project root (e.g., `JED-1204` as `TICKET_INFO_1204.md`):
  ```
  # <Ticket ID>: <Title>

  ## Metadata
  - **Status**: ...
  - **Priority**: ...
  - **Assignee**: ...
  - **Reporter**: ...
  - **Created**: ...
  - **Updated**: ...
  - **Labels**: ...
  - **Sprint**: ...

  ## Description
  <description content>

  ## Acceptance Criteria
  <acceptance criteria if found, otherwise "Not specified">

  ## Implementation Plan
  <implementation plan if found, otherwise "Not specified">

  ## Comments
  ### <Author> - <Timestamp>
  <comment content>
  ```

- **Missing Fields**: If a field is empty or not present, indicate "Not specified" rather than omitting the section.

- **No Hallucinations**: Only include information that exists in the ticket. Do not infer or guess content.