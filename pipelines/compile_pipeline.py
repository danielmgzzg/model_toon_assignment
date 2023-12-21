import os
import kfp
from kfp import dsl
from kfp.compiler import Compiler
from model_toon_pipeline import pipeline
# Define your pipeline
PIPELINE_NAME = os.getenv('PIPELINE_NAME')

def compile_pipeline():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Define the output filename
    output_file = os.path.join(script_dir, f"{PIPELINE_NAME}.yaml")

    # Compile the pipeline
    Compiler().compile(pipeline, output_file)

# Compile the pipeline
if __name__ == '__main__':
    pipeline_file = compile_pipeline()
    