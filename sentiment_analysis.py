from langchain import Chain, PromptTemplate, LanguageModel

# Define the prompt template
prompt_template = PromptTemplate(
    template="Analyze the sentiment of the following text: {text}"
)

# Create the chain
sentiment_chain = Chain(
    [
        ("preprocessing", TextPreprocessor()),
        ("model_inference", LanguageModel(model_name="sentiment-analysis")),
        ("post_processing", SentimentInterpreter()),
    ]
)

# Run the chain
result = sentiment_chain.run(
    prompt_template.format(text="LangChain makes NLP easier to work with!")
)
sentiment = result["sentiment"]
