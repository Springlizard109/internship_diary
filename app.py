from graph import build_graph

graph = build_graph()

question = input("Ask something: ")

result = graph.invoke({"question": question})

print(result["answer"])

while True:
    
    question = input("\nAsk something: ")

    if question.lower() == "exit":
        break

    result = graph.invoke({"question": question})

    print("\nAnswer:\n")
    print(result["answer"])