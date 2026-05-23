# Accessing the Claude via API

## Overview of the Models

**Claude Model Family**

| | **Claude Opus** | **Claude Sonnet** | **Claude Haiku** |
|---|---|---|---|
| **Description** | Highest level of intelligence | Intelligent model that balances quality, speed, cost | Most cost-efficient and latency-optimized model |
| **Cost** | High | Medium | Low |
| **Comparative latency** | Moderate | Fast | Fastest |
| **Supports reasoning** | Yes | Yes | No |
| **Best used for** | - Advanced software development, especially large-scale architecting<br>- Long running tasks that require sustained focus<br>- Strategic planning with multi-step problem solving<br>- Tasks that could benefit from advanced reasoning | - Common coding tasks<br>- Document creation and editing<br>- Content marketing and copywriting<br>- Data analysis and visualization projects<br>- Image analysis<br>- Process automation | - Quick code completions and suggestions<br>- Content moderation and filtering<br>- Data extraction and categorization<br>- Language translation<br>- Q&A systems and knowledge retrieval<br>- Most high-volume, straightforward text processing tasks |

**Notes**
- The most important part of this model family comparison is the "Best used for" column. This is because it tells you what the model is best suited for as per Anthropic team.
- Common approach is to use multiple models in same application based on specific task requirements rather than single model selection.

## Accessing the Claude API

**API Access Flow** = 5-step process from user input to response display

- Step 1: Client sends user text to developer's server (never access Anthropic API directly from client apps to keep API key secret)

- Step 2: Server makes request to Anthropic API using SDK (Python, TypeScript, JavaScript, Go, Ruby) or plain HTTP. Required parameters = API key + model name + messages list + max_tokens limit

- Step 3: Text generation process has 4 stages:
    - Tokenization = breaking input into tokens (words/word parts/symbols/spaces)
    - Embedding = converting tokens to number lists representing all possible word meanings
    - Contextualization = adjusting embeddings based on neighboring tokens to determine precise meaning
    - Generation = output layer produces probabilities for next word, model selects using probability + randomness, adds selected word, repeats process

- Step 4: Model stops when max_tokens reached or special end_of_sequence token generated

- Step 5: API returns response with generated text + usage counts + stop_reason to server, server sends to client for display
    - Token = text chunk (word/part/symbol)
    - Embedding = numerical representation of word meanings
    - Contextualization = meaning refinement using neighboring words
    - Max_tokens = generation length limit
    - Stop_reason = why model stopped generating

## Making requests to the Claude API

### Single request
See [01-access-with-api.ipynb](nbs/01-access-with-api.ipynb) for example.

### Multi-turn conversations
**Multi-Turn Conversations**: conversations with multiple back-and-forth exchanges that maintain context.

The key limitation of the Anthropic API is that it stores no messages. Each request is independent with no memory of previous exchanges. The system is state-less. You need to manually maintain message list in code and send entire conversation history with every follow-up request.

See example in [01-access-with-api.ipynb](nbs/01-access-with-api.ipynb).

### System prompts
- System prompts is a technique to customize Claude's response style and tone by assigning it a specific role or behavior pattern
- You can pass system prompt as plain string to create function using system keyword argument.

See example in [01-access-with-api.ipynb](nbs/01-access-with-api.ipynb).

### Temperature
- Temperature is a parameter that controls randomness in Claude's text generation by influencing token selection probabilities.
- The text generation process is as follows: Input text → tokenization → probability assignment to possible next tokens → token selection based on probabilities → repeat.
- Temperature effects:
    - Temperature 0 = deterministic output, always selects highest probability token
    - Higher temperature = increases chance of selecting lower probability tokens, more creative/unexpected outputs
- **Usage guidelines**:
    - Low temperature (near 0) = data extraction, factual tasks requiring consistency
    - High temperature (near 1) = creative tasks like brainstorming, writing, jokes, marketing
- **Implementation**: Add temperature parameter to model API calls. Higher values don't guarantee different outputs, just increase probability of variation.
- **Key insight**: Temperature directly manipulates the probability distribution of next token selection, making high-probability tokens more/less dominant in the selection process.

### Streaming the responses
- Response Streaming is a technique to display AI responses chunk-by-chunk as they're generated instead of waiting for complete response.
- Problem solved: AI responses can take 10-30 seconds. Users expect immediate feedback, not just spinners.
- How it works:
    - Server sends user message to Claude
    - Claude immediately sends initial response (no text, just acknowledgment)
    - Stream of events follows, each containing text chunks
    - Server forwards chunks to frontend for real-time display
    - Event types:
        - message_start = initial acknowledgment
        - content_block_start = text generation begins
        - content_block_delta = contains actual text chunks (most important)
        - content_block_stop/message_stop = generation complete

- **Implementation**: 
    - Basic: client.messages.create(stream=True) returns event iterator
    - Simplified: client.messages.stream() with text_stream property extracts just text
    - Final message: stream.get_final_message() assembles all chunks for storage

- **Key benefits**: Better UX through immediate response visibility, complete message capture for database storage.


### Controlling model output
- Controlling model output = two key techniques beyond prompt modification for precise control over response direction and length.
- **Pre-filling assistant messages**: manually add an assistant message at the end of the conversation to steer response direction.
- How it works:
    - Assemble messages list with user prompt + manual assistant message
    - Claude sees assistant message as already authored content
    - Claude continues response from exact end of pre-filled text
    - Response gets steered toward pre-filled direction
- **Key point**: Claude continues from exact endpoint of pre-fill, not complete sentences. Must stitch together pre-fill + generated response.
- Example: pre-fill `"Coffee is better because"` → Claude continues with justification for coffee
- **Stop sequences**: force Claude to halt generation when a specific string appears.
- How it works:
    - Provide stop sequence string in chat function
    - When Claude generates that exact string, response immediately stops
    - Generated stop sequence text not included in final output
- Example: prompt `"count 1 to 10"` + stop sequence `"five"` → output stops at `"four, "` (five not included)
- Refinement: stop sequence `", five"` → clean output `"one, two, three, four"`

See example in [01-access-with-api.ipynb](nbs/01-access-with-api.ipynb).

### Structured data
- Structured data generation = technique using assistant message prefilling + stop sequences to get raw output without Claude's natural explanatory headers/footers.
- Problem: Claude automatically adds markdown formatting, headers, and commentary when generating JSON/code/structured content. Users often want just the raw data for copy/paste functionality.
- Solution pattern:
    1. User message = request for structured data
    2. Assistant message prefill = opening delimiter (e.g., `"```json"`)
    3. Stop sequence = closing delimiter (e.g., `"```"`)
- How it works: Claude sees prefilled message, assumes it already started response, generates only the requested content, stops when hitting delimiter.
- Result: raw structured data output with no extra formatting or commentary.
- Application: works for any structured data type (JSON, Python code, lists, etc.), not just JSON. Use whenever you need clean, parseable output without explanatory text.
- **Key benefit**: output can be directly used/copied without manual selection or parsing of unwanted text.

See example in [01-access-with-api.ipynb](nbs/01-access-with-api.ipynb).