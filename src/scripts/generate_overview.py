from PyPDF2 import PdfReader
import argparse
import os
from jinja2 import Template
import yaml

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Generate a paper file from a PDF.")
    argparser.add_argument(
        "--info_paths", type=str, nargs="*", default=[], help="Paths to the paper information."
    )
    argparser.add_argument(
        "--presentation_paths", type=str, nargs="*" , default=[], help="Paths to the presentation information."
    )
    argparser.add_argument(
        "--output_path", type=str, required=True, help="Path to the output file."
    )
    argparser.add_argument(
        "--overview_template_path", type=str, required=True, help="Path to the template file."
    )
    argparser.add_argument(
        "--overview_snippet_template_path", type=str, required=True, help="Path to the snippet file."
    )
    argparser.add_argument(
        "--project_information_path", type=str, required=True, help="Path to the project information."
    )
    args = argparser.parse_args()

    info_paths = args.info_paths
    output_path = args.output_path
    template_path = args.overview_template_path
    snippet_template_path = args.overview_snippet_template_path

    with open(snippet_template_path, "r") as fin:
        snippet_template = Template(fin.read())
    with open(template_path, "r") as fin:
        template = Template(fin.read())

    snippets_read = []
    snippets_unread = []
    for paper, presentation in zip(info_paths, args.presentation_paths):
        if not paper.endswith(".md"):
            continue
        with open(paper, "r") as fin:
            splits = fin.read().split("---", 3)
        paper_info = yaml.safe_load(splits[1])
        paper_details = splits[3]
        paper_info["details"] = paper_details
        paper_info["edit_path"] = paper
        paper_info["presentation_path"] = presentation
        rendered = snippet_template.render(paper_info)
        if paper_info["read"]:
            snippets_read.append(rendered)
        else:
            snippets_unread.append(rendered)
    
    read_section = "\n\n".join(snippets_read)
    unread_section = "\n\n".join(snippets_unread)

    project_information = yaml.safe_load(open(args.project_information_path, "r").read())

    project_information["read"] = read_section
    project_information["unread"] = unread_section
    rendered_template = template.render(project_information)

    if os.path.exists(output_path):
        with open(output_path, "w") as fout:
            fout.write(rendered_template)
        print(f"File {output_path} updated.")
    else:
        with open(output_path, "w") as fout:
            fout.write(rendered_template)
        print(f"File {output_path} created.")




    
