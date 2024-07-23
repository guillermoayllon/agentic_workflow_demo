# Agentic Workflow Demo

This project aims to investigate multi-agent workflows using large language models (LLMs) for resolving complex tasks. For example, it involves creating detailed documents by leveraging information from the internet and databases.

For this puprpose, we use Microsoft's AutoGen. AutoGen is an open-source programming framework for building AI agents and facilitating cooperation among multiple agents to solve tasks. AutoGen aims to provide an easy-to-use and flexible framework for accelerating development and research on agentic AI, like PyTorch for Deep Learning. It offers features such as agents that can converse with other agents, LLM and tool use support, autonomous and human-in-the-loop workflows, and multi-agent conversation patterns.

* AutoGen's documentation: [https://microsoft.github.io/autogen/docs/Getting-Started/](https://microsoft.github.io/autogen/docs/Getting-Started/).

## Structure of the project

- [modules/](./modules/)
    - [agents.py](./modules/agents.py): Agents' definitions and configurations.
    - [common_utils.py](./modules/common_utils.py): Useful functions.
    - [configuration.py](./modules/configuration.py): Configuration dictionaries to connect with LLMs.
    - [speaker_policy.py](./modules/speaker_policy.py): Definition of allowed agent transitions. It is not being used at the moment.

- [tmp/](./tmp/)
    - [chat_history.yml](./tmp/chat_history.yml): YAML file containing the agents' chat history. It is overwritten in every exeuction.
    - [final_document.md](./tmp/final_document.md): Final output of the system. Producing a high-quality final markdown document from a simple user query is the whole goal of this demo.

- [Dockerfile](./Dockerfile): Dockerfile to create the Docker image where the app runs LLM generated code.

- [coding/](./coding/): The Docker container executes code within this folder, resulting in any output (such as images, Python and Bash scripts, tables, etc.) being written to the same location.
- [app.py](./app.py): Main script of the app.

# How to run

1. You need a running LLM. Gemma-2-27b should be already running in the CTC [http://10.10.78.12:8080/v1/](http://10.10.78.12:8080/v1/) so you shouldn't need to worry.
If you want to use a different LLM:
    - The more powerful, the better.
    - The bigger context window, the better.
    - We are now using [google/gemma-2-27b](https://huggingface.co/google/gemma-2-27b?_sm_vck=HJrtFMWb4TW4sbVMMfqjq0W4RtjLDjM45HTfVGtnrZLFMnLTqKZM) served on TGI 2.1.1 and it works great!
    - AutoGen uses the OpenAI's API under the hood. TGI > 2.0.0 is compatible with OpenAI's API.
    - Define your LLM configuration in [./modules/configuration.py](./modules/configuration.py)

2. Install PyAutoGen.

    ```bash
    pip install pyautogen==0.2.32
    ```

    Be cautious! There are two packages: ```pyautogen``` and another one called ```autogen```. The latter is associated with Microsoft’s AutoGen Studio, a more user-friendly version of the framework, but it’s not relevant for our purposes. Make sure to install ```pyautogen```; it contains everything you need.

3. Prepare a Docker image.

    Whenever an agent needs to run code, it does so inside a Docker container. To achieve this, we prepare a Docker image with the most common Data Science libraries, and each time the agent requires code execution, it launches a new instance of that image. While it’s technically possible for agents to execute code directly on bare-metal, it’s not recommended because agents might independently install libraries or run bash scripts.

    Run this command on the root folder of this project to build a Docker image from the Dockerfile:

    ```bash
    docker build -t autogen_execution_environment:latest .
    ```

4. Launch the app!

    ```bash
    python app.py
    ```