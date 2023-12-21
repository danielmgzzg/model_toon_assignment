import os
import kfp
from kfp import dsl
PIPELINE_NAME = os.getenv('PIPELINE_NAME')
PIPELINE_IMAGE_NAME = os.getenv('PIPELINE_IMAGE_NAME')

# Define your component as a Python function
@dsl.container_component
def extract():
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'extraction.py'],
    )

@dsl.pipeline(
    name=PIPELINE_NAME,
    description='A Logistic Regression pipeline.'
)
def pipeline():
    # Use the echo_op component and pass an input parameter to it
    echo_task = extract()
    