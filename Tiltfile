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
    # To avoid unused image warnings, we need to load a Kubernetes YAML use it
    # To debug in the container
    'deployments/model-toon-pod.yaml',

])

# Define Docker image to build from Dockerfile
docker_build(
    'model_toon_pipeline',
    '.',
    dockerfile='docker/Dockerfile.pipeline',
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


local_resource(
    'build-pipeline',
    'make build-pipeline',
    ['./pipelines/compile_pipeline.py',
     './pipelines/model_toon_pipeline.py',
     './src'
     ],
     labels=['model-toon-pipeline'],

)

# Define services
k8s_resource(
    'ml-pipeline-ui',
    port_forwards='3000:3000'
)

k8s_resource(
    'model-toon-pipeline-pod',
    labels=['model-toon-pipeline']
)

# Set up a local resource to deploy the pipeline
local_resource(
    'deploy-pipeline',
    'make deploy-pipeline',
    ['./pipelines/{}.yaml'.format(pipeline_name),
     './pipelines/model_toon_pipeline.py',
    #  './src',
     'build-pipeline',
     ],
     resource_deps=['ml-pipeline-ui',
     'model_toon_pipeline'],
     labels=['model-toon-pipeline']
)

