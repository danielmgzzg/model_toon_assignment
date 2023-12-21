# Assuming you have environment variables PIPELINE_NAME and KUBEFLOW_HOST set
pipeline_name = os.getenv('PIPELINE_NAME')
kubeflow_host = os.getenv('KUBEFLOW_HOST')
pipeline_version = os.getenv('PIPELINE_VERSION', '2.0.5')
git_repo_url = os.getenv('GIT_REPO_URL')
git_token = os.getenv('GIT_TOKEN')
azure_client_id = os.getenv('AZURE_CLIENT_ID')
azure_client_secret = os.getenv('AZURE_CLIENT_SECRET')
azure_tenant_id = os.getenv('AZURE_TENANT_ID')

# Load Kubeflow Kubernetes deployment YAMLs
k8s_yaml([
    'deployments/kubeflow/namespace.yaml',
    'deployments/kubeflow/pipelines.yaml',
    # To avoid unused image warnings, we need to load a Kubernetes YAML using it in a job
    'deployments/kubeflow/model-toon-init.yaml',
    # To debug in the container
    'deployments/kubeflow/model-toon-debug.yaml',

])

# Define Docker image to build from Dockerfile
docker_build(
    'model_toon_pipeline', 
    '.', 
    dockerfile='Dockerfile',
    build_args={
    'git_repo_url': git_repo_url, 
    'git_token': git_token,
    'azure_client_id': azure_client_id,
    'azure_client_secret': azure_client_secret,
    'azure_tenant_id': azure_tenant_id  
        }
    )

# Watch for changes in the pipeline directory
watch_file('pipelines/*.py')


# Get the image name from Kubernetes
image_name_cmd = "kubectl get job model-toon-pipeline-init-job -o=jsonpath='{.spec.template.spec.containers[?(@.name==\"model-toon-pipeline-container\")].image}'"
# Set this image name as an environment variable
os.environ['PIPELINE_IMAGE_NAME'] = local(image_name_cmd, quiet=False)


# On changes in the pipeline directory, run the pipeline update script
local_resource(
    'build-pipeline',
    'make build-pipeline',
    ['./pipelines/compile_pipeline.py', './pipelines/model_toon_pipeline.py']
)

# Define services
k8s_resource(
    'ml-pipeline-ui', 
    port_forwards='3000:3000'
)

# Set up a local resource to deploy the pipeline
local_resource(
    'deploy-pipeline',
    'make deploy-pipeline',
    ['./pipelines/{}.yaml'.format(pipeline_name), './pipelines/model_toon_pipeline.py'],
    resource_deps=['ml-pipeline-ui']  # Ensure this runs after ml-pipeline-ui is ready
)

