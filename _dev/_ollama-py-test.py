from ollama_python.endpoints import ModelManagementAPI

api = ModelManagementAPI(base_url="http://localhost:11434/v1")
result = api.list_local_models()

print(result.models)