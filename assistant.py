import ollama

print("Local Assistant (phi3:mini)")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Assistant: Bye 👋")
        break

    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {"role": "system", "content": "You are a helpful, concise assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    print("Assistant:", response["message"]["content"])
