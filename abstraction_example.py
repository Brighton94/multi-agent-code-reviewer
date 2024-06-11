from langchain import LangChain
from langchain.chains import SequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Define the prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="Context: {context}\nQuestion: {question}\nAnswer:",
)

# Initialize the language model
llm = OpenAI(model="text-davinci-003")

# Define the chain of operations
chain = SequentialChain(
    chains=[
        {
            "name": "QuestionAnswering",
            "llm": llm,
            "prompt": prompt,
            "input_variables": ["context", "question"],
            "output_key": "answer",
        },
        {
            "name": "SentimentAnalysis",
            "function": lambda inputs: {
                "sentiment": "positive" if "good" in inputs["answer"] else "negative"
            },
            "input_variables": ["answer"],
            "output_key": "sentiment",
        },
    ],
    memory=ConversationBufferMemory(),
)

# Example input
context = "LangChain is a framework that simplifies the creation of applications using language models."
question = "How does LangChain help developers?"

# Run the chain
output = chain.run({"context": context, "question": question})

print(output)
