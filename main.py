from parser import parse_tf
from graph import render_diagram

def main():
    tf_path = ""
    resources = parse_tf(tf_path)
    render_diagram(resources)


if __name__ == "__main__":
    main()