# gptoolbox
Python Interface for OpenAI API's like ChatGPT 3.5 or 4

This is a first iteration of a python application to connect to and interface with ChatGPT 3.5, and eventually other chat models like GPT 4, Dall-E, and Whisper.

First major feature is that any code-snippets output by GPT will be buffered and collated.  When the output is complete, the user can save the codebox snippet using the commands as per below;

Current state connects to gpt-3.5-turbo-16k by default.
- switch:<gpt-model> typed from the chat interface will switch to the specified model.
- save:filename.txt will save the most recent code-box as the specified file.
- exit: will exit the chat, also works direct from API using just 'exit', placeholder command with : for future intentions.
- selection screen uses common endpoints on common path, then probes each endpoint for error or valid api response.  
- **NOTE** the above means that api calls are being used to valid endpoint status.  This could be improved upon.
