from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.general import General

API_GATEWAY_TYPES = {
    "aws_api_gateway_rest_api",
    "aws_api_gateway_resource",
    "aws_api_gateway_method",
}

SKIP_RENDER_TYPES = {
    "aws_lambda_permission",
    "aws_iam_role",
    "provider",
}

TYPE_MAP = {
    "aws_lambda_function": Lambda,
    "api_gateway": APIGateway,
}

def get_node_key(res):
    if res is None:
        return None
    if res.type in API_GATEWAY_TYPES:
        return "api_gateway"
    return f"{res.type}.{res.name}"

def get_node_label(res):
    if res.type in API_GATEWAY_TYPES:
        return "API Gateway"
    return res.name

def find_resource(resources, label, name):
    for res in resources:
        if res.type == label and res.name == name:
            return res
    return None

def render_diagram(resources):
    with Diagram("Terraform Infra", show=True, direction="TB"):
        nodes = {}

        # Create node objects
        for res in resources:
            if res.type in SKIP_RENDER_TYPES:
                continue
            key = get_node_key(res)
            if key not in nodes:
                icon = TYPE_MAP.get(res.type, General)
                label = get_node_label(res)
                nodes[key] = icon(label)

        # Draw edges for direct dependencies
        for res in resources:
            if res.type in SKIP_RENDER_TYPES:
                continue
            src_key = get_node_key(res)
            for dep in res.depends_on:
                dst_key = get_node_key(dep)
                if src_key and dst_key and src_key in nodes and dst_key in nodes:
                    nodes[dst_key] >> nodes[src_key]

        # Handle aws_lambda_permission as glue from API Gateway → Lambda
        for res in resources:
            if res.type != "aws_lambda_permission":
                continue

            refs = res.properties.get("__tfmeta", {}).get("references", [])
            lambda_node = None
            api_node = None

            for ref in refs:
                ref_res = find_resource(resources, ref["label"], ref["name"])
                if not ref_res:
                    continue
                if ref_res.type == "aws_lambda_function":
                    lambda_node = get_node_key(ref_res)
                elif ref_res.type.startswith("aws_api_gateway"):
                    api_node = "api_gateway"

            if lambda_node and api_node and lambda_node in nodes and api_node in nodes:
                nodes[api_node] >> nodes[lambda_node]
