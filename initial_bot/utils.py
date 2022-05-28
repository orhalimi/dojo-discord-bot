import yaml


def read_yaml_file(path):
    """
    Read yaml files

    input:
        path:               Path to the yaml file, from the root project

    output:
        content:            The file content, converted to dist.
    """
    with open(path) as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
        return content
