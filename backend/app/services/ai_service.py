import os
import json
from datetime import date
from groq import Groq
from dotenv import load_dotenv
from app.services.rag_service import search_knowledge_base
from app.services.ai_tools import AVAILABLE_TOOLS, execute_tool

load_dotenv()

def get_ai_response(user_message: str, history: list = None) -> str:
    """
    Unified AI Agent Pipeline:
    1. RAG Knowledge Retrieval: Fetches menu/policies from ChromaDB.
    2. Tool/Function Calling: Enables the AI to query DB or perform actions (e.g. check orders, book tables, place home delivery orders).
    3. Final Generation: Answers the customer with context or confirmed action details.
    """
    if not os.getenv("GROQ_API_KEY"):
        return "System: GROQ_API_KEY is missing in .env file."

    # 1. Retrieve RAG context from ChromaDB
    relevant_docs = search_knowledge_base(user_message, n_results=3)
    context_text = "\n\n".join(relevant_docs) if relevant_docs else "No specific context found."

    # Current date for booking context (so AI knows what "tomorrow" or "today" means)
    today_str = date.today().strftime("%Y-%m-%d")

    # 2. Build Agent System Prompt
    system_prompt = f"""You are a helpful, professional, and friendly AI customer support agent for 'Spice Garden' restaurant.
Today's date is {today_str}.

RESTAURANT KNOWLEDGE BASE (CONTEXT):
------------------------------------
{context_text}
------------------------------------

TOOLS & ACTIONS AVAILABLE:
1. `place_delivery_order`: Places a home delivery food order in our system.
2. `book_table`: Reserves a dine-in dining table at Spice Garden.
3. `get_order_status`: Tracks an existing order status using an order number (e.g. ORD-12345678).

CRITICAL INSTRUCTIONS FOR HOME DELIVERY ORDERS:
- If a customer requests to order food for home delivery (or asks to book an order):
  1. Check if they have provided ALL FOUR of the following required details:
     a) Food items and their specific quantities (e.g., 2 Chicken Biryani, 1 Butter Naan)
     b) Customer name
     c) 10-digit contact phone number
     d) Complete delivery address (with flat/house number, street or area)
  2. If ANY of these 4 details are missing, DO NOT call `place_delivery_order`!
     Instead, politely ask the customer for the missing details (e.g. "I'd be delighted to help you place that order! Could you please provide your name, phone number, and delivery address?").
  3. ONLY when ALL FOUR details are clearly provided by the user (either in the current message or earlier in the chat history), call the `place_delivery_order` tool.
  4. After the tool executes, provide a warm, clear order confirmation showing the Order Number, items ordered, total amount (with tax & delivery fee details), and the estimated delivery time (35-45 minutes).

CRITICAL INSTRUCTIONS FOR TABLE RESERVATIONS:
- Requires customer name, phone number, reservation date (YYYY-MM-DD), reservation time (HH:MM or 12hr), and party size (number of guests). If any are missing, ask the user first.

GENERAL GUIDELINES:
- For menu recommendations, prices, timings, and policies, answer accurately using the knowledge base.
- If something is out of scope and no tool applies, politely ask them to contact our staff at +917989053026.
- Keep responses friendly, courteous, and concise.
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Include recent conversation history if provided (so AI remembers past turns)
    if history and isinstance(history, list):
        for msg in history:
            role = "assistant" if msg.get("sender") == "bot" or msg.get("role") in ["assistant", "bot"] else "user"
            content = msg.get("text") or msg.get("content", "")
            if content and not content.startswith("⚠️ Sorry, I could not connect"):
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # First Call to LLM with Tools
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
            tools=AVAILABLE_TOOLS,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Check if the AI decided to call a Tool/Function
        if response_message.tool_calls:
            # Append AI's tool call intent to conversation history
            messages.append(response_message)

            # Process each tool call
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the actual Python tool against MySQL database
                tool_output = execute_tool(function_name, function_args)

                # Feed the tool result back to the LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output
                })

            # Second Call to LLM: Let AI read the tool result and produce a natural reply
            final_response = client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=messages
            )
            return final_response.choices[0].message.content

        # If no tool was needed, return the standard text reply
        return response_message.content

    except Exception as e:
        return f"Error in AI Agent: {str(e)}"
