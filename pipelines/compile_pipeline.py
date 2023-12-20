import os
import kfp
from kfp import dsl
from kfp.compiler import Compiler
import kfp.components as comp

# Define your component as a Python function
@dsl.component(base_image='python:3.8')
def hello_world(message: str) -> str:
    print(message)
    return message

# Define your pipeline
PIPELINE_NAME = os.getenv('PIPELINE_NAME')
@dsl.pipeline(
    name=PIPELINE_NAME,
    description='A hello world pipeline.'
)
def my_pipeline(input_message: str):
    # Use the echo_op component and pass an input parameter to it
    echo_task = hello_world(message=input_message)
    # You can access the output of the component like this
    echo_task.output

def compile_pipeline():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Define the output filename
    output_file = os.path.join(script_dir, f"{PIPELINE_NAME}.yaml")

    # Compile the pipeline
    Compiler().compile(my_pipeline, output_file)

# Compile the pipeline
if __name__ == '__main__':
    pipeline_file = compile_pipeline()
    