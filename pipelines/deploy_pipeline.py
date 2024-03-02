import os
import kfp
import uuid

# Upload and deploy the pipeline to Kubeflow
# Define your pipeline
PIPELINE_NAME = os.getenv('PIPELINE_NAME')
KUBEFLOW_HOST = os.getenv('KUBEFLOW_HOST', 'http://localhost:3000/pipeline')


def deploy_pipeline():

    # Connect to the Kubeflow Pipelines server
    client = kfp.Client(host=KUBEFLOW_HOST)

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Define the output filename
    output_file = os.path.join(script_dir, f"{PIPELINE_NAME}.yaml")

    # Check if the pipeline already exists
    existing_pipelines = client.list_pipelines().pipelines
    existing_pipeline = next(
        (p for p in existing_pipelines if p.display_name == PIPELINE_NAME),
        None)

    if existing_pipeline:
        # Update the existing pipeline
        updated_pipeline = client.upload_pipeline_version(
            pipeline_package_path=output_file,
            pipeline_version_name=f"{PIPELINE_NAME}_{uuid.uuid4().hex[:6]}",
            pipeline_id=existing_pipeline.pipeline_id)
        print(
            f"Pipeline {PIPELINE_NAME} updated successfully: {updated_pipeline.display_name}"
        )
    else:
        # Create a new pipeline
        client.upload_pipeline(pipeline_package_path=output_file,
                               pipeline_name=PIPELINE_NAME)
        print(
            f"Pipeline {PIPELINE_NAME} created successfully: {updated_pipeline.display_name}"
        )


if __name__ == '__main__':
    deploy_pipeline()
