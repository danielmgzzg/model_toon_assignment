import os
from kfp import dsl
from kfp.dsl import Input, Output
from kfp.dsl import Dataset

PIPELINE_NAME = os.getenv('PIPELINE_NAME')
PIPELINE_IMAGE_NAME = os.getenv('PIPELINE_IMAGE_NAME')


@dsl.container_component
def loading_op(
    x_train_pickle: Output[Dataset],
    y_train_pickle: Output[Dataset],
    x_test_pickle: Output[Dataset],
    y_test_pickle: Output[Dataset],
    x_vaL: str = "x",
):
    # Executes the extraction.py script
    return dsl.ContainerSpec(
        image=PIPELINE_IMAGE_NAME,
        command=['python', 'loading.py'],
    )


@dsl.container_component
def preprocess_op(
    x_train_pickle: Input[Dataset],
    y_train_pickle: Input[Dataset],
    x_test_pickle: Input[Dataset],
    y_test_pickle: Input[Dataset],
    x_train_prep: Output[Dataset],
    y_train_prep: Output[Dataset],
    x_test_prep: Output[Dataset],
    y_test_prep: Output[Dataset],
):
    # Executes the extraction.py script
    return dsl.ContainerSpec(image=PIPELINE_IMAGE_NAME,
                             command=['python', 'preprocess.py'],
                             args=[
                                 '--x_train_prep',
                                 f"{x_train_prep.path}",
                                 '--y_train_prep',
                                 f"{y_train_prep.path}",
                                 '--x_test_prep',
                                 f"{x_test_prep.path}",
                                 '--y_test_prep',
                                 f"{y_test_prep.path}",
                             ])


@dsl.container_component
def training_op(input_data: dsl.Input[dsl.Dataset]):
    # Executes the extraction.py script
    return dsl.ContainerSpec(image=PIPELINE_IMAGE_NAME,
                             command=['python', 'training.py'],
                             args=[
                                 '--input_data',
                                 f"{input_data.path}",
                             ])


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

    loading_task = loading_op()
    preprocess_task = preprocess_op(
        x_train_pickle=loading_task.outputs["x_train_pickle"],
        y_train_pickle=loading_task.outputs["y_train_pickle"],
        x_test_pickle=loading_task.outputs["x_test_pickle"],
        y_test_pickle=loading_task.outputs["y_test_pickle"],
    )
    preprocess_task.after(loading_task)

    training_task = training_op(
        input_data=preprocess_task.outputs['x_train_prep'])
    training_task.after(preprocess_task)

    evaluation_task = evaluation_op()
    evaluation_task.after(training_task)
