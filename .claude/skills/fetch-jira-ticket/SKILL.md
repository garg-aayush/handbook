---
name: fetch-jira-ticket
description: Fetch a Jira ticket using the Atlassian MCP plugin and extract key details into a structured summary. Use when the user wants to retrieve, view, or get information about a Jira ticket.
---

Fetch a Jira ticket using the Atlassian MCP plugin and extract key details into a structured summary.

## Rules

- **Input Validation**: A Jira ticket ID must be provided (e.g., `JED-1204`, `PROJ-123`). If not provided, STOP and ask the user for the ticket ID.

- **Atlassian Cloud ID**: Use cloud ID `8e5e4495-e477-4a3f-af21-f2ff97eae820` (dekeo.atlassian.net) for all requests. If this fails, call `mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources` to discover the correct cloud ID.

- **Fetch via Atlassian MCP Plugin**: Use `mcp__plugin_atlassian_atlassian__getJiraIssue` with the following parameters:
  - `cloudId`: `8e5e4495-e477-4a3f-af21-f2ff97eae820`
  - `issueIdOrKey`: the ticket ID
  - `responseContentFormat`: `markdown`
  - `expand`: `renderedFields,names`
  - `fields`: `["summary", "description", "status", "priority", "assignee", "reporter", "created", "updated", "resolutiondate", "resolution", "labels", "sprint", "parent", "duedate", "comment", "attachment", "customfield_10020", "customfield_10015", "customfield_10037", "customfield_10036"]`

- **Handling Large Responses**: The API response may be too large to display inline. If the result is saved to a file, use `jq` via Bash to extract fields. Run two jq commands:
  1. **Metadata extraction**:
     ```bash
     cat <result_file> | jq '{
       summary: .issues.nodes[0].fields.summary,
       status: .issues.nodes[0].fields.status.name,
       resolution: .issues.nodes[0].fields.resolution.name,
       priority: .issues.nodes[0].fields.priority.name,
       assignee: .issues.nodes[0].fields.assignee.displayName,
       reporter: .issues.nodes[0].fields.reporter.displayName,
       created: .issues.nodes[0].fields.created,
       updated: .issues.nodes[0].fields.updated,
       resolutiondate: .issues.nodes[0].fields.resolutiondate,
       labels: .issues.nodes[0].fields.labels,
       duedate: .issues.nodes[0].fields.duedate,
       parent_key: .issues.nodes[0].fields.parent.key,
       parent_summary: .issues.nodes[0].fields.parent.fields.summary,
       parent_status: .issues.nodes[0].fields.parent.fields.status.name,
       size: .issues.nodes[0].fields.customfield_10037,
       team: .issues.nodes[0].fields.customfield_10036,
       attachment_names: [.issues.nodes[0].fields.attachment[]?.filename],
       comment_count: .issues.nodes[0].fields.comment.total
     }'
     ```
  2. **Description extraction**:
     ```bash
     cat <result_file> | jq '.issues.nodes[0].fields.description'
     ```

- **Comment Extraction**: Comments may be in ADF (Atlassian Document Format) instead of plain text. To extract readable text from ADF comments, use this jq command on the comments file:
  ```bash
  cat <comments_file> | jq -r '
  def extract_text:
    if type == "object" then
      if .type == "text" then .text // ""
      elif .type == "hardBreak" then "\n"
      elif .type == "heading" then
        "\n" + (if .attrs.level == 1 then "# " elif .attrs.level == 2 then "## " elif .attrs.level == 3 then "### " else "" end) + ([.content[]? | extract_text] | join("")) + "\n"
      elif .type == "paragraph" then ([.content[]? | extract_text] | join("")) + "\n"
      elif .type == "bulletList" then ([.content[]? | extract_text] | join(""))
      elif .type == "orderedList" then ([.content[]? | extract_text] | join(""))
      elif .type == "listItem" then "- " + ([.content[]? | extract_text] | join(""))
      elif .type == "codeBlock" then "```\n" + ([.content[]? | extract_text] | join("")) + "\n```\n"
      elif .type == "mediaInline" or .type == "mediaSingle" or .type == "media" then "[Image]"
      elif .type == "inlineCard" then "[Link: " + (.attrs.url // "unknown") + "]"
      else ([.content[]? | extract_text] | join(""))
      end
    elif type == "array" then [.[] | extract_text] | join("")
    else "" end;
  .[] | "### " + .author + " - " + .created + "\n\n" + (.body | extract_text) + "\n---"
  '
  ```
  First try to get comments from the main result file:
  ```bash
  cat <result_file> | jq '[.issues.nodes[0].fields.comment.comments[] | {author: .author.displayName, created: .created, body: .body}]'
  ```
  If the output is too large, it will be saved to a separate file — run the ADF extraction on that file.

- **Extract Key Details**: Parse and present the following fields from the ticket:
  1. **Title**: The ticket summary/title.
  2. **Description**: Full description text. Preserve formatting where possible.
  3. **Acceptance Criteria**: Extract if present (often in description or a custom field).
  4. **Implementation Plan**: Extract if present (often in description or a custom field).
  5. **Metadata**: Include:
     - Status
     - Resolution
     - Priority
     - Assignee
     - Reporter
     - Created date
     - Updated date
     - Resolution Date
     - Labels (if any)
     - Sprint (if applicable)
     - Parent Epic (key + summary + status)
     - Due Date
     - Size (if applicable)
     - Team (if applicable)
  6. **Attachments**: List all attachment filenames.
  7. **Comments**: List all comments with author and timestamp, with full text content extracted from ADF.

- **Attachments and Images**: Do **NOT** fetch attachments or images from Jira. Instead:
  - For attachments, first check if you can find them in the project, if not, add placeholder links (e.g., `[Attachment: <filename>]`)
  - For images embedded in comments, use `[Image]` placeholder
  - Do not download or embed attachment or image content

- **Output Format**: Present the ticket information in a clean markdown structure saved to `TICKET_INFO_<Ticket_num>.md` in the project root (e.g., `JED-1204` as `TICKET_INFO_1204.md`):
  ```
  # <Ticket ID>: <Title>

  ## Metadata
  - **Status**: ...
  - **Resolution**: ...
  - **Priority**: ...
  - **Assignee**: ...
  - **Reporter**: ...
  - **Created**: ...
  - **Updated**: ...
  - **Resolution Date**: ...
  - **Labels**: ...
  - **Sprint**: ...
  - **Parent Epic**: <KEY> - <Summary> (<Status>)
  - **Due Date**: ...
  - **Size**: ...
  - **Team**: ...

  ## Description
  <description content>

  ## Acceptance Criteria
  <acceptance criteria if found, otherwise "Not specified">

  ## Implementation Plan
  <implementation plan if found, otherwise "Not specified">

  ## Attachments
  - [Attachment: <filename>]

  ## Comments
  ### <Author> - <Timestamp>
  <comment content>
  ```

- **Missing Fields**: If a field is empty or not present, indicate "Not specified" rather than omitting the section.

- **No Hallucinations**: Only include information that exists in the ticket. Do not infer or guess content.

- **If the MCP call fails**: Report the error clearly. Common issues:
  - Wrong cloud ID → call `getAccessibleAtlassianResources` to discover correct one
  - Permission denied → inform the user to check their Atlassian plugin authorization
