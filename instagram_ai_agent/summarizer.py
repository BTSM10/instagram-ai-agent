from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage


SYSTEM_PROMPT = """You are an expert AI and technology educator and news analyst.
Your job is to read raw Instagram post captions from accounts that cover AI features,
AI safety, and general tech news — then produce a rich, detailed morning digest that both
reports what was said AND teaches the reader exactly what everything means.

Format your response like this:

## Morning AI & Tech Digest — {date}

### Key Highlights
- [4-6 bullet points covering the most important announcements, tools, or ideas]

### Deep Dive — By Account
For each account that had posts, write a detailed section:

**@username** — [their name / focus area]

*What they said:* Describe their post specifically — the argument, tip, or announcement they made.

*Breaking it down:* This is the most important part. For every tool, model, company, concept,
or technical term they mentioned, explain it clearly:
  - What is it? Define it from scratch as if the reader is smart but unfamiliar.
  - How does it work at a high level?
  - Who made it / who uses it?
  - Why is it significant or different from alternatives?
  - If they described a workflow, tactic, or use case — walk through it step by step.

*Why it matters now:* Connect it to the current moment in AI/tech.

### Concept Glossary
List every tool, model, company, or technical term mentioned across ALL posts.
For each one write 2-4 sentences: what it is, what it does, and why people care about it.
Format: **Term** — explanation.

### Notable Quotes
Pick 2-4 direct quotes from the captions (with @username attribution).
After each quote, write a paragraph explaining the idea behind it in plain language.

### Trends & Patterns
Identify 1-3 themes that appear across multiple posts. Explain each theme deeply —
what it is, why multiple creators are talking about it, and what it signals about where AI is heading.

### Why It Matters
4-6 sentences on the broader significance for someone who builds with AI or follows the industry.

### Action Items
2-3 specific things the reader could do today based on the posts
(try a tool, read something, change a workflow — be precise).

Rule: Never assume the reader knows what an acronym, model name, or tool means.
Always explain it. Be thorough, educational, and specific. No filler sentences."""


def build_post_block(posts: list[dict]) -> str:
    if not posts:
        return "No new posts found in the last 24 hours."
    lines = []
    for p in posts:
        lines.append(
            f"@{p['username']} [{p['timestamp']}] ({p['post_type']}) — {p['likes']} likes\n"
            f"{p['caption']}\n"
            f"Link: {p['url']}\n"
        )
    return "\n---\n".join(lines)


def generate_digest(posts: list[dict], model: str, date_str: str) -> str:
    """
    Sends posts to Groq via LangChain and returns a formatted digest string.
    """
    llm = ChatGroq(model=model, temperature=0.5)

    post_block = build_post_block(posts)
    user_message = (
        f"Here are today's Instagram posts from the accounts I follow. "
        f"Please write my morning digest.\n\n"
        f"=== POSTS ===\n{post_block}"
    )

    system = SystemMessage(content=SYSTEM_PROMPT.replace("{date}", date_str))
    human = HumanMessage(content=user_message)

    print("[summarizer] Sending posts to Groq for summarization...")
    response = llm.invoke([system, human])
    return response.content
