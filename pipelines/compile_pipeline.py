import os
from kfp.compiler import Compiler
from model_toon_pipeline import pipeline

PIPELINE_NAME = os.getenv('PIPELINE_NAME')


def compile_pipeline():

    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Define the output filename
    output_file = os.path.join(script_dir, f"{PIPELINE_NAME}.yaml")

    Compiler().compile(pipeline, package_path=output_file)

    print(f"Pre-compiled pipeline YAML path: {output_file}")

    os.remove(output_file)

if __name__ == '__main__':
    pipeline_file = compile_pipeline()
