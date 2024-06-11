from langgraph import LangGraph, Node, Edge
from langgraph.llms import OpenAI
from langgraph.prompts import PromptTemplate
from langgraph.memory import ConversationGraphMemory

# Define the prompt template node
prompt_node = Node(
    name="PromptTemplate",
    function=PromptTemplate(
        input_variables=["context", "question"],
        template="Context: {context}\nQuestion: {question}\nAnswer:",
    ),
)

# Define the LLM node
llm_node = Node(name="LLM", function=OpenAI(model="text-davinci-003"))

# Define the sentiment analysis node
sentiment_node = Node(
    name="SentimentAnalysis",
    function=lambda inputs: {
        "sentiment": "positive" if "good" in inputs["answer"] else "negative"
    },
)

# Create the graph and add nodes
graph = LangGraph()
graph.add_node(prompt_node)
graph.add_node(llm_node)
graph.add_node(sentiment_node)

# Define the edges (data flow) between nodes
graph.add_edge(
    Edge(
        source=prompt_node,
        target=llm_node,
        input_mapping={"context": "context", "question": "question"},
    )
)
graph.add_edge(
    Edge(source=llm_node, target=sentiment_node, input_mapping={"answer": "text"})
)

# Initialize memory
memory = ConversationGraphMemory()

# Example input
context = "LangChain is a framework that simplifies the creation of applications using language models."
question = "How does LangChain help developers?"

# Run the graph
output = graph.run({"context": context, "question": question}, memory=memory)

print(output)
