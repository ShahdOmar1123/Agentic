from agent import run_agent


def main():
    question = input("Ask a question: ")

    answer = run_agent(question)

    print("\nFinal Answer:")
    print(answer)


if __name__ == "__main__":
    main()