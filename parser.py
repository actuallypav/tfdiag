import tfparse
from model import TerraformResource

def parse_tf(path):
    cfg = tfparse.Config()
    cfg.load_module(path)

    resource_map = {}
    resources = []

    for res in cfg.resources:
        full_id = f'{res["type"]}.{res["name"]}'
        r = TerraformResource(
            type=res["type"],
            name=res["name"],
            properties=res.get("values", {}),
        )
        resource_map[full_id] = r
        resources.append(r)

    for res in cfg.resources:
        full_id = f'{res["type"]}.{res["name"]}'
        ref_ids = res.get("references", [])
        for ref_id in ref_ids:
            dep = resource_map.get(ref_id)
            if dep:
                resource_map[full_id].depends_on.append(dep)
    return resources