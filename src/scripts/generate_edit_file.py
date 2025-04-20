from PyPDF2 import PdfReader
import argparse
import os
from jinja2 import Template
import yaml
import arxiv
import sys

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Generate a paper file from a PDF.")
    argparser.add_argument(
        "--pdf_path", type=str, required=True, help="Path to the PDF file."
    )
    argparser.add_argument(
        "--output_path", type=str, required=True, help="Path to the output directory."
    )
    argparser.add_argument(
        "--template_path", type=str, required=True, help="Path to the template file."
    )
    args = argparser.parse_args()

    pdf_path = args.pdf_path
    output_path = args.output_path
    template_path = args.template_path

    if os.path.exists(output_path):
        print(f"File {output_path} already exists. Skipping.")
        sys.exit()

    paper_id = os.path.basename(pdf_path).replace(".pdf", "")
    client = arxiv.Client()
    try:
        search = arxiv.Search(id_list=[paper_id])
        paper = next(client.results(search))
        title = paper.title
        author = [a.name for a in paper.authors]
        abstract = paper.summary
    except Exception:
        print(f"Could not load arxiv for {paper_id}")
        abstract = "todo"
        reader = PdfReader(pdf_path)
        info   = reader.metadata
        try:
            title  = info.title or info.get("/Title")
            if len(title) == 0:
                raise ValueError("Title is empty!")
        except Exception as e:
            print(f"Error reading metadata: {e}")
            title = "Unknown Title"

        try:
            author  = info.title or info.get("/Author")
            if len(author) == 0:
                raise ValueError("Author is empty!")
        except Exception as e:
            print(f"Error reading metadata: {e}")
            author = ["Unknown Author"]

    with open(template_path, "r") as fin:
        template = Template(fin.read())
    rendered = template.render(title=title, author=yaml.dump(author), pdf_path=pdf_path, abstract=abstract)

    if os.path.exists(output_path):
        print(f"File {output_path} already exists. Skipping.")
    else:
        with open(output_path, "w") as fout:
            fout.write(rendered)
        print(f"File {output_path} created.")
    print(os.path.exists(output_path))



    
