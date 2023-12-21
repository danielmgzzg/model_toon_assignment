import os
import kfp
from kfp import dsl
PIPELINE_NAME = os.getenv('PIPELINE_NAME')
PIPELINE_IMAGE_NAME = os.getenv('PIPELINE_IMAGE_NAME')

# Defining components as a Python functions
@dsl.container_component
def extract_op():
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'extraction.py'],
    )

@dsl.container_component
def validation_op():
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'validation.py'],
    )

@dsl.container_component
def preparation_op():
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'preparation.py'],
    )

@dsl.container_component
def training_op():
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'training.py'],
    )

@dsl.container_component
def evaluation_op():
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'evaluation.py'],
    )
    

@dsl.pipeline(
    name=PIPELINE_NAME,
    description='A Logistic Regression pipeline.'
)
def pipeline():
    # Use the echo_op component and pass an input parameter to it
    extract_task = extract_op()
    
    validation_task = validation_op()
    # The output of one task can be used as input to another, creating a dependency chain
    validation_task.after(extract_task)

    perparation_task = preparation_op()
    perparation_task.after(validation_task)
    
    training_task = training_op()
    training_task.after(perparation_task)
    
    evaluation_task = evaluation_op()
    evaluation_task.after(training_task)