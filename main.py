from groq import Groq

# ── CONFIGURATION ──────────────────────────────────────────────────
GROQ_API_KEY = "paste_your_groq_api_key_here"

client = Groq(api_key=GROQ_API_KEY)

BUSINESS_INFO = """
Business Name: TechShop Sofia
Type: Online Electronics Store
Location: Sofia, Bulgaria

PRODUCTS:
- iPhone 15 Pro: €1,200
- Samsung Galaxy S24: €900
- MacBook Air M3: €1,500
- AirPods Pro: €250
- Samsung 4K TV 55inch: €800

SHIPPING:
- Sofia: Free delivery, 1-2 days
- Bulgaria: €5, 2-3 days
- Europe: €15, 5-7 days

RETURNS:
- 30 day return policy
- Product must be unopened
- Refund within 5 business days

PAYMENT:
- Credit/Debit card
- Bank transfer
- Cash on delivery (Bulgaria only)

CONTACT:
- Email: support@techshop.bg
- Phone: +359 888 123 456
- Working hours: Mon-Fri 9am-6pm
"""

def chat(user_message: str, history: list) -> str:
    messages = [
        {
            "role": "system",
            "content": f"""You are a helpful customer service assistant for TechShop Sofia.
Only answer questions based on the business information provided below.
If you don't know something, say "I don't have that information, please contact us at support@techshop.bg"
Be friendly, professional and concise.

BUSINESS INFORMATION:
{BUSINESS_INFO}"""
        }
    ]

    for msg in history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I'm having technical difficulties. Please contact support@techshop.bg. Error: {str(e)}"

def main():
    print("\n🤖 TechShop Sofia - AI Customer Assistant")
    print("=" * 50)
    print("Type your question or 'quit' to exit\n")

    history = []

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit", "q"]:
            print("\nAssistant: Thank you for contacting TechShop Sofia. Goodbye!")
            break

        response = chat(user_input, history)
        print(f"\nAssistant: {response}\n")

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
