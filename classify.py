
import json
import pandas as pd
from llm import ask_llm


# ==========================================
# 1. LOAD TICKET DATASET
# ==========================================

df = pd.read_csv("data/tickets.csv")


# ==========================================
# 2. HELPER FUNCTION TO EXTRACT JSON
# ==========================================

def parse_json_response(response):

    # Remove Markdown code fences if present
    response = response.strip()
    response = response.replace("```json", "")
    response = response.replace("```", "")

    return json.loads(response.strip())


# ==========================================
# 3. ZERO-SHOT PROMPTING
# ==========================================

def zero_shot_classify(description):

    prompt = f"""
You are an IT Helpdesk ticket classification assistant.

Classify the given IT issue.

Categories:
- Password
- VPN
- Email
- Unknown

Priorities:
- Low
- Medium
- High

Rules:
- High: Security incidents, account lockouts,
  or serious service failures.
- Medium: Login problems or normal technical issues.
- Low: Minor issues.
- Unknown: When there is insufficient information.

Return ONLY valid JSON:
{{
    "category": "VPN",
    "priority": "High"
}}

Ticket:
{description}
"""

    response = ask_llm(prompt)

    return parse_json_response(response)


# ==========================================
# 4. FEW-SHOT PROMPTING
# ==========================================

def few_shot_classify(description):

    prompt = f"""
You are an expert IT Helpdesk ticket classifier.

Classify the given ticket using the examples.

Categories:
Password, VPN, Email, Unknown

Priorities:
Low, Medium, High

Examples:

Ticket: I forgot my company password.
Output: {{"category":"Password","priority":"Medium"}}

Ticket: VPN connection timed out.
Output: {{"category":"VPN","priority":"High"}}

Ticket: Outlook is not opening.
Output: {{"category":"Email","priority":"Medium"}}

Ticket: Emails are not being delivered.
Output: {{"category":"Email","priority":"Medium"}}

Ticket: My account is locked after multiple
incorrect login attempts.
Output: {{"category":"Password","priority":"High"}}

Ticket: My VPN keeps disconnecting every
few minutes.
Output: {{"category":"VPN","priority":"High"}}

Ticket: I clicked a suspicious email link.
Output: {{"category":"Email","priority":"High"}}

Ticket: My system is not working properly.
Output: {{"category":"Unknown","priority":"Medium"}}

Rules:
- Use the closest matching category.
- Security incidents and account lockouts are High.
- Normal technical issues are Medium.
- Minor issues are Low.
- Use Unknown when information is insufficient.

Return ONLY valid JSON:
{{"category":"VPN","priority":"High"}}

Ticket:
{description}
"""

    response = ask_llm(prompt)

    return parse_json_response(response)


# ==========================================
# 5. TOOL 1: FINAL TICKET CLASSIFICATION
# ==========================================

def classify_ticket(description):

    # Using the selected few-shot prompt
    return few_shot_classify(description)


# ==========================================
# 6. COMPARE ZERO-SHOT AND FEW-SHOT
# ==========================================

def compare_prompts():

    sample = df.head(5)

    zero_correct = 0
    few_correct = 0

    print("\n======================================")
    print(" ZERO-SHOT VS FEW-SHOT COMPARISON")
    print("======================================")

    for _, row in sample.iterrows():

        description = row["issue_description"]

        actual_category = row["category"]
        actual_priority = row["priority"]

        print("\nTicket:", row["ticket_id"])
        print("Description:", description)

        # Zero-shot prediction
        zero_result = zero_shot_classify(description)

        # Few-shot prediction
        few_result = few_shot_classify(description)

        actual = {
            "category": actual_category,
            "priority": actual_priority
        }

        print("\nActual:", actual)
        print("Zero-shot:", zero_result)
        print("Few-shot:", few_result)

        # Compare zero-shot
        if (
            zero_result.get("category") == actual_category
            and zero_result.get("priority") == actual_priority
        ):
            zero_correct += 1

        # Compare few-shot
        if (
            few_result.get("category") == actual_category
            and few_result.get("priority") == actual_priority
        ):
            few_correct += 1

    total = len(sample)

    zero_accuracy = (zero_correct / total) * 100
    few_accuracy = (few_correct / total) * 100

    print("\n======================================")
    print(" FINAL COMPARISON RESULTS")
    print("======================================")

    print(f"Zero-shot correct: {zero_correct}/{total}")
    print(f"Zero-shot accuracy: {zero_accuracy:.2f}%")

    print(f"Few-shot correct: {few_correct}/{total}")
    print(f"Few-shot accuracy: {few_accuracy:.2f}%")

    if few_accuracy >= zero_accuracy:
        print("\nSelected Prompt: FEW-SHOT")
    else:
        print("\nSelected Prompt: ZERO-SHOT")


# ==========================================
# 7. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    # Run prompt comparison
    compare_prompts()

    # Test Tool 1
    print("\n======================================")
    print(" TOOL 1: CLASSIFY TICKET TEST")
    print("======================================")

    test_description = "My VPN keeps disconnecting every few minutes"

    result = classify_ticket(test_description)

    print("Ticket:", test_description)
    print("Classification:", result)
