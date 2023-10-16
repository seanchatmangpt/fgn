import ast
import time

import openai
import asyncio

class CodeOptimizationSystem:
    """
    This system aims to reduce the need for higher quality models by experimenting
    with lesser GPT models to produce usable lines of code.

    The general idea is to:
    1. Query a lower quality model for code.
    2. Validate the code.
    3. If the code is not satisfactory, progressively try higher quality models until
       a suitable code snippet is obtained or all models are exhausted.
    """

    def __init__(self, models):
        self.models = models

    async def generate_code(self, prompt, max_attempts=None, parallel_calls=2):
        """
        Generate code using the list of models in parallel and measure execution time.
        """
        tasks = []
        start_time = time.time()  # Start measuring total execution time

        for model in self.models:
            for _ in range(parallel_calls):
                tasks.append(self._chat_with_model(prompt, model))

        responses = await asyncio.gather(*tasks)

        total_execution_time = time.time() - start_time
        print(f"Total execution time for {len(self.models) * parallel_calls} API calls: {total_execution_time:.2f} seconds")

        for response, model in zip(responses, self.models):
            if self._is_code_valid(response):
                individual_execution_time = time.time() - start_time
                print(f"Generated code using model {model} in {individual_execution_time:.2f} seconds")
                return response

        return None

    async def _chat_with_model(self, prompt, model):
        """
        An async wrapper function for openai API calls.
        """
        response = await openai.Completion.acreate(
            model=model,
            prompt=prompt,
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text.strip()

    def _is_code_valid(self, code):
        """
        Validate the generated code. This method performs syntax checking
        and other quality checks on the generated code.
        """
        # Check for placeholder
        if "Placeholder" in code:
            return False

        try:
            # Attempt to parse the code to check for syntax errors
            ast.parse(code)
        except SyntaxError:
            print(f"Syntax error in generated code: {code}")
            return False

        # You can add more code quality checks here, such as complexity checks,
        # naming conventions, or specific error patterns you want to detect.

        # If none of the checks failed, consider the code valid.
        return True

models = [
    "ada-code-search-code",
    "ada-code-search-text",
    "ada-search-document",
    "ada-search-query",
    "babbage-code-search-code",
    "babbage-code-search-text",
    "babbage-search-document",
    "babbage-search-query",
    "davinci-instruct-beta",
    "curie-instruct-beta"
]

async def main():
    optimizer = CodeOptimizationSystem(models)
    code_snippet = await optimizer.generate_code('You are a Python Code writing AGI simulation AI. '
                                                 'Write a function to start a Flask server in Python.')

    print(code_snippet)

if __name__ == '__main__':
    asyncio.run(main())  # Run the async main function
