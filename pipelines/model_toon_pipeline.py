import os
from kfp import dsl

PIPELINE_NAME = os.getenv('PIPELINE_NAME')
PIPELINE_IMAGE_NAME = os.getenv('PIPELINE_IMAGE_NAME')


@dsl.container_component
def preprocess_op(output_data: dsl.Output[dsl.Dataset],
                  # output_data_path: dsl.OutputPath(str)
                  ):
    # Executes the extraction.py script
    return dsl.ContainerSpec(image=PIPELINE_IMAGE_NAME,
                             command=['python', 'preprocess.py'],
                             args=[
                                 '--output_data',
                                 f"{output_data.path}",
                             ])


@dsl.container_component
def training_op(input_data: dsl.Input[dsl.Dataset]):
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'training.py'],
        args=[
            '--input_data',
            f"{input_data.path}",
        ]
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

    training_task = training_op(
        input_data=preprocess_task.outputs['output_data'])
    training_task.after(preprocess_task)

    evaluation_task = evaluation_op()
    evaluation_task.after(training_task)
