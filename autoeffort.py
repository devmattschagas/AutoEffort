"""
# AutoEffort
## "Why there is automatic cars that automatically change your gears for more efficience and speed but there isn't any for tokens?" - Matheus das Chagas Santos(Undergraduate in Electrical Engineering at UFES, 2026).

AutoEffort has born with the current premise:
- Hard Tasks require Higher Effort, otherwise, you are wasting tokens.
- Easy tasks, compliments, rubbish, and etc. requires lower reasoning effort, otherwise, you are wasting tokens.
- Changing from one to the other everytime its boring, and your AI should do it everytime.
- Why not building a tool that your framework will call everytime so it could get the better cost-efficienct reasoning to do a task?

I did it.

Implement it in your programs and coding and see the results.

*Note: It actually needs an OpenRouter api key to work at the moment.*

Implementation Tip:
- As context use: {messages:[messages], goal:"Current Goal"}, and so on.

Version: 1.0 - 02/10/2026
"""

import os
from typing import Tuple, Final
from typesafe_sdk import TypeSafeClient, Choice, TypeSafeError

API_URL:Final = "https://openrouter.ai/api"

__all__ = ['AutoEffort']

def _isOpenRouterCONFIGURED() -> Tuple:
    """Verify if OpenRouter API key is configured"""
    try:
        api_key:str = os.environ['OPENROUTER_API_KEY']
    except:
        return (None, "There is no API Key configured")
    return (api_key, "API Key is configured")

def AutoEffort(
        reasoning_types:dict={
            "low":"For silly talk and short conversations", "medium": "For simple tasks and short to long conversations", 
            "high": "For tasks who needs reasoning"
            }, 
        **context
    ) -> dict:
    
    """
    ## Auto select one reasoning-type from reasonings based on context and how hard is the actual task.
    
    ### INPUTS:
    - reasoning_types(dict): The reasoning/efforts the model handles + the matching criteria for when you want it to be active.
    - context(dict): Messages, Goals, Task the Jev needs to know.
    
    ### OUTPUT:
    - Success: {"status": "success", "reasoning": selected_effort}.
    - Failure: {"status": "error", "message": error_description}.
    
    """
    try:
        isConfigured:Tuple = _isOpenRouterCONFIGURED()
        if isConfigured[0] == None:
            raise EnvironmentError(isConfigured[-1])
        API_KEY:str = isConfigured[0]
        client = TypeSafeClient(api_key=API_KEY, base_url=API_URL, model="~typesafe/jev-latest")
        answer = client.system_one(
            state=context,
            
            questions={
                "reasoning": Choice(
                    instructions="How much effort does my Large Language Model needs to execute the last message given the context?",
                    
                    criteria=reasoning_types
                )
            }
        )
        
        return {"status": "success", "reasoning": answer.answers["reasoning"].choice}
        
    except EnvironmentError as e:
        return {"status": "error", "message": str(e)}
        
    except TypeSafeError as e:
        return {"status": "error", "message": f"TypeSafe SDK ({type(e).__name__}): {e}"}

if __name__ == "__main__":
    mensagens = [
        "Olá, como vai?"
    ]
    
    resposta = AutoEffort(context=mensagens)
    
    print(f'{resposta}')
