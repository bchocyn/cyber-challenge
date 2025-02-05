import asyncio
import boto3
from botocore.config import Config
import json
from joint import env, util
from joint.templates import templates_ai_msg

config = Config(max_pool_connections=env.MAX_POOL_SIZE, retries = {
    "max_attempts": 100,
    "mode": "standard"
})
client = boto3.client("bedrock-runtime", region_name=env.AWS_REGION, config=config)
model_id = "meta.llama3-70b-instruct-v1:0"

async def get_completion(msg: str) -> str:
    request = {
            "prompt": templates_ai_msg.render(prompt=msg),
            "max_gen_len": 4000,
            "temperature": 0.5
    }
    response = await util.run_blocking(client.invoke_model, modelId=model_id, body=json.dumps(request))
    body = await util.run_blocking(response["body"].read)
    print(json.loads(body))
    exit()
    return json.loads(body)["generation"]
