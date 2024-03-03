import os
from kfp import dsl

PIPELINE_NAME = os.getenv('PIPELINE_NAME')
PIPELINE_IMAGE_NAME = os.getenv('PIPELINE_IMAGE_NAME')
print(f"PIPELINE_IMAGE_NAME: {PIPELINE_IMAGE_NAME}")


@dsl.container_component
def preprocess_op():
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'preprocess.py'],
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


@dsl.pipeline(name=PIPELINE_NAME,
              description='A Logistic Regression pipeline.')
def pipeline():

    preprocess_task = preprocess_op()

    training_task = training_op()
    training_task.after(preprocess_task)

    evaluation_task = evaluation_op()
    evaluation_task.after(training_task)
