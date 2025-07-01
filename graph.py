from diagrams import Diagram
from diagrams.aws.compute import Lambda #TODO: replace this with an automated/flexible way of importing specific icons for the use case

def render_diagram(resources):
    with Diagram("Terraform Infra", show=True):
        nodes = {}

        #Create diagram nodes
        for res in resources:
            nodes[res] = Lambda(f"{res.type}\n{res.name}") #TODO: swap in better mapping

        #Draw edges based on dependencies
        for res in resources:
            for dep in res.depends_on:
                nodes[dep] >> nodes[res]
