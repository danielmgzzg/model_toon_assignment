# Assuming you have environment variables PIPELINE_NAME and KUBEFLOW_HOST set
pipeline_name = os.getenv('PIPELINE_NAME')
kubeflow_host = os.getenv('KUBEFLOW_HOST')
pipeline_version = os.getenv('PIPELINE_VERSION', '2.0.5')

# Load Kubeflow Kubernetes deployment YAMLs
k8s_yaml([
    'deployments/kubeflow/namespace.yaml',
    'deployments/kubeflow/pipelines.yaml',
])

# Define Docker image to build from Dockerfile
docker_build('model_toon_pipeline', '.', dockerfile='Dockerfile')
# Ignore warnings about unused images because is not used in the Kubernetes YAML
update_settings(suppress_unused_image_warnings=["model_toon_pipeline"])

# Watch for changes in the pipeline directory
watch_file('pipelines/*.py')

# On changes in the pipeline directory, run the pipeline update script
local_resource(
    'build-pipeline',
    'make build-pipeline',
    './pipelines/compile_pipeline.py'
)

# Set up a local resource to deploy the pipeline
local_resource(
    'deploy-pipeline',
    'make deploy-pipeline',
    './pipelines/{}.yaml'.format(pipeline_name)
)

# Define services
k8s_resource('ml-pipeline-ui', port_forwards='3000:3000')