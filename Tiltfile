# Assuming you have environment variables PIPELINE_NAME and KUBEFLOW_HOST set
pipeline_name = os.getenv('PIPELINE_NAME')
kubeflow_host = os.getenv('KUBEFLOW_HOST')
pipeline_version = os.getenv('PIPELINE_VERSION', '2.0.5')
git_repo_url = os.getenv('GIT_REPO_URL')
azure_client_id = os.getenv('AZURE_CLIENT_ID')
azure_client_secret = os.getenv('AZURE_CLIENT_SECRET')
azure_tenant_id = os.getenv('AZURE_TENANT_ID')
azure_storage_container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
azure_storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')

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
    'azure_client_id': azure_client_id,
    'azure_client_secret': azure_client_secret,
    'azure_tenant_id': azure_tenant_id,
    'azure_storage_container_name': azure_storage_container_name,
    'azure_storage_account_name': azure_storage_account_name
        }
    )

# Watch for changes in the pipeline directory
watch_file('pipelines/*.py')


registry = "localhost:35147/"
repo_name = 'model_toon_pipeline'
image_tag_cmd = "docker images | grep %s | awk '{print $2}' | head -n 1" % repo_name
tag = local(image_tag_cmd, quiet=False)
# # Set this image name as an environment variable
os.environ['PIPELINE_IMAGE_NAME'] = registry + repo_name + ":" + str(tag)

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

