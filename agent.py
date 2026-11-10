
import os
import json

from dotenv import load_dotenv
from groq import Groq

from rag import search_docs
from classify import classify_ticket


# ==========================================
# 1. GROQ CONFIGURATION
# ==========================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Please check your .env file."
    )

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"


# ==========================================
# 2. DEFINE AVAILABLE TOOLS
# ==========================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": (
                "Search the IT Helpdesk Guide to answer "
                "IT troubleshooting and how-to questions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Employee's IT question."
                    }
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "classify_ticket",
            "description": (
                "Classify an IT support issue when an employee "
                "explicitly asks to raise a ticket."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Employee's issue description."
                    }
                },
                "required": ["description"]
            }
        }
    }
]


# ==========================================
# 3. TOOL EXECUTION
# ==========================================

def execute_tool(tool_name, arguments):

    if tool_name == "search_docs":

        return search_docs(arguments["question"])

    elif tool_name == "classify_ticket":

        return classify_ticket(arguments["description"])

    else:

        return {"error": "Unknown tool selected."}


# ==========================================
# 4. AI AGENT
# ==========================================

def run_agent(question):

    system_prompt = """
You are a helpful IT Helpdesk Assistant for TechNova Solutions.

YOUR RESPONSIBILITIES:

1. Help employees with IT-related questions.
2. Answer troubleshooting questions using search_docs.
3. Use classify_ticket when an employee explicitly asks to
   raise a support ticket.
4. Refuse questions unrelated to IT support politely.

SECURITY GUARDRAILS:

5. Never ask employees to reveal their passwords.
6. Never reveal, repeat, or generate passwords.
7. Never provide information that is not supported by
   the retrieved IT Helpdesk Guide.
8. Never invent company policies, rules, or procedures.

TOOL RESPONSE RULES:

9. For search_docs answers, use only facts returned by
   the search_docs tool.
10. For classify_ticket, report only the category and
    priority returned by the classification tool.
11. Never claim that a ticket has been submitted,
    created, or assigned.
12. Never promise that a technician will follow up.
13. Explain that the tool only classifies the issue
    and does not submit a ticket.

RESPONSE STYLE:

14. Give clear, simple, and helpful answers.
15. If information is unavailable, say so clearly.
16. Do not call tools for non-IT questions.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # ======================================
    # 5. ASK GROQ TO SELECT A TOOL
    # ======================================

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    # ======================================
    # 6. EXECUTE SELECTED TOOL
    # ======================================

    if assistant_message.tool_calls:

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print("\n" + "=" * 40)
            print("SELECTED TOOL:", tool_name)
            print("=" * 40)

            result = execute_tool(
                tool_name,
                arguments
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    result,
                    ensure_ascii=False
                )
            })

        # ==================================
        # 7. GENERATE FINAL RESPONSE
        # ==================================

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        answer = (
            final_response.choices[0].message.content
            or "I could not generate a response."
        )

        print("\n" + "=" * 40)
        print("AI AGENT RESPONSE")
        print("=" * 40)
        print(answer)

        return answer

    # ======================================
    # 8. DIRECT RESPONSE / REFUSAL
    # ======================================

    answer = (
        assistant_message.content
        or "I could not generate a response."
    )

    print("\n" + "=" * 40)
    print("AI AGENT RESPONSE")
    print("=" * 40)
    print(answer)

    return answer


# ==========================================
# 9. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("\n" + "=" * 50)
    print("       TECHNOVA IT HELPDESK ASSISTANT")
    print("=" * 50)

    print("\nAvailable capabilities:")
    print("1. IT Troubleshooting")
    print("2. Support Ticket Classification")
    print("3. IT Knowledge Base Search")

    print("\nType 'exit' to stop the assistant.")

    while True:

        question = input(
            "\nEnter your question: "
        ).strip()

        if question.lower() == "exit":

            print(
                "\nThank you for using "
                "TechNova IT Helpdesk Assistant!"
            )

            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            run_agent(question)

        except Exception as error:

            print("\nAn error occurred:")
            print(error)
            print("\nPlease try again.")
