import autogen
import autogen.graph_utils

from modules.agents import (
    code_reviewer,
    coder,
    critic,
    debugger,
    dummy,
    executor,
    integrator,
    writer,
)
from modules.common_utils import delete_files_in_directory, save_dict_to_yaml, save_to_markdown

delete_files_in_directory("coding/")
delete_files_in_directory("observability/")

task = "Write statistics for data science"


def second_to_last_message(
    sender: autogen.ConversableAgent,
    recipient: autogen.ConversableAgent,
    summary_args: dict,
):

    return recipient.chat_messages_for_summary(sender)[-2]["content"]


def dummy_summary(
    sender: autogen.ConversableAgent,
    recipient: autogen.ConversableAgent,
    summary_args: dict,
):

    # return recipient.chat_messages_for_summary(sender)[-10]["content"]
    return "dummy summary"


chat_results = autogen.agentchat.initiate_chats(
    [
        {
            "summary_metod": dummy_summary,
            "sender": dummy,
            "recipient": dummy,
            "message": "",
        },
        {
            "summary_metod": dummy_summary,
            "sender": critic,
            "recipient": writer,
            "message": task,
        },
        {
            "summary_method": dummy_summary,
            "sender": code_reviewer,
            "recipient": coder,
            "message": """Based on the provided markdown document, suggest plots to illustrate the document. Write Python code to generate plots , execute it and save the output.
            """,
            "max_turns": 5,
        },
        {
            "summary_method": dummy_summary,
            "sender": debugger,
            "recipient": executor,
            "message": """Execute the provided code.
            """,
        },
        {
            "summary_method": "last_msg",
            "sender": integrator,
            "recipient": integrator,
            "message": """Based on the context, integrate the generated plots into the markdown document.
            """,
            "max_turns": 1,
        },
    ]
)

# autogen.graph_utils.visualize_speaker_transitions_dict(
#     SPEAKER_TRANSITIONS_DICT,
#     SPEAKER_LIST,
#     export_path="observability/speaker_transitions_dict.png",
# )

save_to_markdown(chat_results[-1].summary, "observability/final_document")
save_dict_to_yaml(chat_results, "observability/chat_history.yml")
