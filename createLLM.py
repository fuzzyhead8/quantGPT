from openai import OpenAI

def create_assistant(api_key):
    try:
        # Initialize the client with the provided API key
        client = OpenAI(api_key=api_key)
        
        # Upload example strategy and backtrader documentation files (optional based on the API's support)
        example_strategy = client.files.create(
            file=open("./assistant_files/ExampleStrategy.py", "rb"),
            purpose='assistants'
        )

        backtrader_doc = client.files.create(
            file=open("./assistant_files/Backtrader_doc.md", "rb"),
            purpose='assistants'
        )

        # Create the assistant with the correct tool type
        assistant = client.beta.assistants.create(
            name="Quant Strategist",
            instructions="""You will implement a trading strategy based on signals of your choice. Your strategy class must follow the exact same template as the ExampleStrategy class you are given, with the three main methods: __init__(), next(), and get_optimisation_range() (which is a static method). Also don't forget the params of the class for your indicators, as written in ExampleStrategy. You will be able to call the params by self.params.param_name.
Regardless of the strategy, the class should be named GeneratedStrategy and inherits from LoggedStrategy, which is a wrapper around bt.Strategy that logs everything, present in the file you have. So your strategy will be called: class GeneratedStrategy(LoggedStrategy) and you will start the code with: 
  from LoggedStrategy import *
  import backtrader as bt 

  Also, you can't enter in a position if you already are in one, and you can only sell opened positions, which can be checked with the if self.position condition.
  You are free but not forced to use the backtrader library, with documentation provided in BacktraderDoc.md . You will follow exactly the user strategy using his logic. If the user wants a new strategy, you will give him an original one. If the message doesn't seem to be a strategy, or impossible to implement,
  you will apologize but don't return something else. Your response will always be structured as follows and only contains the two following parts: Brief strategy explanation, Strategy implementation. If you use backtrader indicators, ensure that you correctly use them with the right name and the right parameters, from the Backtrader documentation you are provided with.
Don't write anything after the strategy implementation code so I can parse your answer easily.""",
            tools=[{"type": "file_search"}],  # Adjusting to use 'file_search' for file-based tools
            model="gpt-4o-mini",
        )

        # Return the assistant ID if successfully created
        return assistant.id

    except Exception as e:
        # Print error message and return None if there’s an issue
        print("Error creating assistant:", e)
        return None
