from PyPDF2 import PdfReader
import argparse
import os
from jinja2 import Template
import yaml

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

    reader = PdfReader("paper_pdfs/learning_and_unlearning_fabricated_knowledge_in_large_language_models.pdf")
    info   = reader.metadata
    try:
        title  = info.title or info.get("/Title")
        author = info.author or info.get("/Author")
    except Exception as e:
        print(f"Error reading metadata: {e}")
        title = "Unknown Title"
        author = "Unknown Author"

    with open(template_path, "r") as fin:
        template = Template(fin.read())
    rendered = template.render(title=title, author=author, pdf_path=pdf_path)
    print("-" *50 + "Edit:")
    print(output_path)
    print(os.path.exists(output_path))
    if os.path.exists(output_path):
        print(f"File {output_path} already exists. Skipping.")
    else:
        with open(output_path, "w") as fout:
            fout.write(rendered)
        print(f"File {output_path} created.")
    print(os.path.exists(output_path))



    
