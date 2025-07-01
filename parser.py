from tfparse import load_from_path
from model import TerraformResource

def parse_tf(path):
    parsed = load_from_path(path)

    resource_map = {}
    resources = []

    # First pass
    for res_type, res_list in parsed.items():
        if not isinstance(res_list, list):
            continue

        for res in res_list:
            meta = res.get("__tfmeta", {})
            name = meta.get("name") or meta.get("label")
            full_id = f"{res_type}.{name}"
            references = meta.get("references", [])

            resource = TerraformResource(
                type=res_type,
                name=name,
                properties={k: v for k, v in res.items() if k != "__tfmeta"},
                references=references,
            )

            resource_map[full_id] = resource
            resources.append(resource)

    # Second pass
    for res_type, res_list in parsed.items():
        for res in res_list:
            meta = res.get("__tfmeta", {})
            name = meta.get("name") or meta.get("label")
            full_id = f"{res_type}.{name}"

            references = meta.get("references", [])
            for ref in references:
                ref_id = f"{ref['label']}.{ref['name']}"
                if ref_id in resource_map:
                    resource_map[full_id].depends_on.append(resource_map[ref_id])

    #     # Debug print all parsed resources and their dependencies
    # print("\n--- Parsed Resources ---")
    # for r in resources:
    #     print(f"{r.full_id()}")
    #     print(f"  depends_on: {[d.full_id() for d in r.depends_on]}")
    #     print(f"  references: {r.references if hasattr(r, 'references') else 'N/A'}")
    # print("--- End Parsed ---\n")


    return resources
