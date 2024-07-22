import autogen

from modules.configuration import LLM_CONFIG

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=LLM_CONFIG,
    system_message="""You are an expert text writer.
    Write text in markdown format based on the task.
    Don't engage in a polite conversation beyond concisely making the necessary changes. 
    Don't thank the other speaker.
    Respond only with the content of the text.
    """,
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=LLM_CONFIG,
    system_message="""You are an expert text critic.
    Provide constructive and concise feedback on the text written.
    Don't engage in a polite conversation beyond concisely making the necessary changes. 
    Don't thank the other speaker.
    Assure that your feedback is included in the text.
    As soon as you are satisfied with the text respond "TERMINATE". 
    """,
    human_input_mode="NEVER",
)


coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=LLM_CONFIG,
    system_message="""You are an expert Python programmer and you write code to execute.  
    *Don't retrieve data from the internet or from APIs.
    *Don't assume that there is data available to read from disk. For instance, pd.read_csv('./gdp_data.csv')
    *All plots MUST be saved to disk. For instance, 'plt.savefig('figure.png')'.""",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

code_reviewer = autogen.AssistantAgent(
    name="Code_Reviwer",
    llm_config=LLM_CONFIG,
    system_message="""You are an expert Python reviewer and debugger. 
    In particular, assure that:
    *Code doesn't retrieve data from the internet or from APIs.
    *Code doesn't assume that there is data available to read from disk. For instance, pd.read_csv('./gdp_data.csv')
    *All plots MUST be saved to disk. For instance, 'plt.savefig('figure.png')'.
    *All necessary libraries are imported.
    Provide concise instructions to fix the code.
    If you find no bugs, respond only "TERMINATE".
    If the conversation deviates from the task, respond "TERMINATE".
    """,
    human_input_mode="NEVER",
)


debugger = autogen.AssistantAgent(
    name="Debugger",
    llm_config=LLM_CONFIG,
    system_message="""You are an expert Python reviewer and debugger.
    You respond to the result of an execution. 
    If the execution is not successful (exitcode: 1), implement fixes in the original code and pass the revised version. The revise version must contain the whole code, not only the fix.
    If  the execution is successful (exitcode: 0), respond with a list of the produced plots, their paths and a short description of each.
    If you find no bugs, respond only "TERMINATE".
    """,
    is_termination_msg=lambda msg: msg["content"] == "",
    human_input_mode="NEVER",
)

executor = autogen.ConversableAgent(
    name="Executor",
    system_message="""Execute the provided code and report the result.
    """,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "coding",
        "use_docker": "autogen_execution_environment:latest",
    },
)

integrator = autogen.AssistantAgent(
    name="Integrator",
    llm_config=LLM_CONFIG,
    system_message="""Your task is provide the final document in markdown format.
    The context contains:
    1. The document.
    2. The list of generated plots names and a short description of them.
    Include the names of the plots in the relevant sections in the document in markdown format. 
    For example, if the context refers to a plot called "my_plot.png" include it in the document as ![my_plot](../coding/my_plot.png).
    All plots are in the '../coding' directory.
    Return the final document in markdown format without further comments.
    """,
)


dummy = autogen.AssistantAgent(
    name="Dummy",
    llm_config=LLM_CONFIG,
    system_message="""Responde "TERMINATE""",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
)
