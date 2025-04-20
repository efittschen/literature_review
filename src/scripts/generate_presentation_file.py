from PyPDF2 import PdfReader
import argparse
import os
from jinja2 import Template
import yaml

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Generate a paper file from a PDF.")
    argparser.add_argument(
        "--paper_info_path", type=str, required=True, help="Path to the paper information."
    )
    argparser.add_argument(
        "--output_path", type=str, required=True, help="Path to the output directory."
    )
    argparser.add_argument(
        "--template_path", type=str, required=True, help="Path to the template file."
    )
    args = argparser.parse_args()

    info_path = args.paper_info_path
    output_path = args.output_path
    template_path = args.template_path

    with open(info_path, "r") as fin:
        splits = fin.read().split("---", 3)
    paper_info = yaml.safe_load(splits[1])
    paper_details = splits[3]
    paper_info["details"] = paper_details

    with open(template_path, "r") as fin:
        template = Template(fin.read())
    rendered = template.render(paper_info)

    if os.path.exists(output_path):
        with open(output_path, "w") as fout:
            fout.write(rendered)
        print(f"File {output_path} updated.")
    else:
        with open(output_path, "w") as fout:
            fout.write(rendered)
        print(f"File {output_path} created.")



    
