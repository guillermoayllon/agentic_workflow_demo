import autogen

from modules.agents import coder, critic, debugger, executor, integrator, user_proxy, writer

SPEAKER_LIST = [user_proxy, coder, writer, executor, debugger, critic, integrator]


SPEAKER_TRANSITIONS_DICT = {
    writer: [critic, integrator],
    critic: [writer, coder],
    coder: [executor],
    executor: [debugger, coder, integrator],
    debugger: [coder],
    user_proxy: [coder, integrator, writer],
    integrator: [coder, user_proxy],
}


def custom_speaker_selection_func(last_speaker: autogen.Agent, groupchat: autogen.GroupChat):
    """Define a customized speaker selection function.
    A recommended way is to define a transition for each speaker in the groupchat.

    Returns:
        Return an `Agent` class or a string from ['auto', 'manual', 'random', 'round_robin'] to select a default method to use.
    """
    messages = groupchat.messages

    if len(messages) <= 1:
        return writer

    elif last_speaker is integrator:
        return "auto"

    elif last_speaker is writer:
        return "auto"

    elif last_speaker is critic:
        return "auto"

    elif last_speaker is coder:
        return executor

    elif last_speaker is executor:

        if "exitcode: 1" in messages[-1]["content"]:
            # If the last message indicates an error, let the engineer to improve the code
            return debugger

        elif "exitcode: 0 (execution succeeded)" in messages[-1]["content"]:
            return integrator

        else:
            # Otherwise, let the writer to speak
            return coder

    elif last_speaker is debugger:
        return coder

    elif last_speaker is user_proxy:
        return None

    else:
        return "random"
