# chat.py (omitting imports for brevity)
# ...
from fgn.completion.chat import chat


# Import the get_current_weather function from weather.py
# from weather import get_current_weather


    # response_message = response["choices"][0]["message"]
    #
    # # Step 2: check if GPT wanted to call a function
    # if response_message.get("function_call"):
    #     # Step 3: call the function
    #     # Note: the JSON response may not always be valid; be sure to handle errors
    #     available_functions = {
    #         "get_current_weather": get_current_weather,
    #     }  # only one function in this example, but you can have multiple
    #     function_name = response_message["function_call"]["name"]
    #     fuction_to_call = available_functions[function_name]
    #     function_args = json.loads(response_message["function_call"]["arguments"])
    #     function_response = fuction_to_call(
    #         location=function_args.get("location"),
    #         unit=function_args.get("unit"),
    #     )
    #
    #     # Step 4: send the info on the function call and function response to GPT
    #     messages.append(response_message)  # extend conversation with assistant's reply
    #     messages.append(
    #         {
    #             "role": "function",
    #             "name": function_name,
    #             "content": function_response,
    #         }
    #     )  # extend conversation with function response
    #     second_response = chat(
    #         prompt="",
    #         sys_msg="A LLM 7 AGI Hive-Mind simulator",
    #         msgs=messages,
    #         model="gpt-3.5-turbo-0613",
    #         max_retry=1,
    #         backoff_factor=2,
    #         initial_wait=0.25,
    #     )  # get a new response from GPT where it can see the function response
    #     return second_response
    #
print(run_weather_conversation())
