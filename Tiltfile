# Assuming you have environment variables PIPELINE_NAME and KUBEFLOW_HOST set
pipeline_name = os.getenv('PIPELINE_NAME')
kubeflow_host = os.getenv('KUBEFLOW_HOST')
pipeline_version = os.getenv('PIPELINE_VERSION', '2.0.5')

# Get the image name from Kubernetes
image_name_cmd = "kubectl get job model-toon-pipeline-init-job -o=jsonpath='{.spec.template.spec.containers[?(@.name==\"model-toon-pipeline-container\")].image}'"
# Set this image name as an environment variable
os.environ['PIPELINE_IMAGE_NAME'] = local(image_name_cmd, quiet=True)

# Load Kubeflow Kubernetes deployment YAMLs
k8s_yaml([
    'deployments/kubeflow/namespace.yaml',
    'deployments/kubeflow/pipelines.yaml',
    # To avoid unused image warnings, we need to load a Kubernetes YAML using it in a job
    'deployments/kubeflow/model-toon-init.yaml',
])

# Define Docker image to build from Dockerfile
docker_build('model_toon_pipeline', '.', dockerfile='Dockerfile')

# Watch for changes in the pipeline directory
watch_file('pipelines/*.py')

# On changes in the pipeline directory, run the pipeline update script
local_resource(
    'build-pipeline',
    'make build-pipeline',
    ['./pipelines/compile_pipeline.py', './pipelines/model_toon_pipeline.py']
)

# Set up a local resource to deploy the pipeline
local_resource(
    'deploy-pipeline',
    'make deploy-pipeline',
    ['./pipelines/{}.yaml'.format(pipeline_name), './pipelines/model_toon_pipeline.py']
)

# Define services
k8s_resource('ml-pipeline-ui', port_forwards='3000:3000')