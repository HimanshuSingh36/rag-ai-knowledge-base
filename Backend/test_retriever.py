from retriever import retrieve_documents


query = "What AI experience does Himanshu have?"

results = retrieve_documents(query, k=3)

print("\nRetrieved chunks:\n")

for i, document in enumerate(results, start=1):

    print(f"========== CHUNK {i} ==========")

    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)

    print()