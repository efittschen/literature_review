import os
import os.path
import inspect
import sys

import json
from steamroller import Environment
import glob
import yaml

vars = Variables("custom.py")
vars.AddVariables(
    ("PDF_DIR", "", "paper_pdfs"),
    ("EDIT_DIR", "", "paper_files"),
    ("SCRIPTS_DIR", "", "src/scripts"),
    ("DATA_DIR", "", "src/data"),
    ("EDIT_TEMPLATE", "", "${DATA_DIR}/edit_template.md"),
    ("PRESENTATION_DIR", "", "src/presentation_files"),
    ("PRESENTATION_TEMPLATE", "", "${DATA_DIR}/presentation_template.md"),
    ("SEGMENT_OVERVIEW_TEMPLATE", "", "${DATA_DIR}/segment_overview_template.md"),
    ("OVERVIEW_TEMPLATE", "", "${DATA_DIR}/overview_template.md"),
    ("PROJECT_INFORMATION", "", "project.yaml"),

    ("TOPIC_DIR", "", "topics"),
    ("TOPIC_OVERVIEW_TEMPLATE", "", "${DATA_DIR}/topic_overview_template.md"),
)

env = Environment(
    variables=vars,
    BUILDERS={
        "GENERATE_EDIT_FILE": Builder(
            action = (
                "python src/scripts/generate_edit_file.py "
                "--pdf_path ${PDF_PATH} "
                "--output_path ${TARGET} "
                "--template_path ${TEMPLATE_PATH}"
            )
        ),
        "GENERATE_PRESENTATION_FILE": Builder(
            action = (
                "python src/scripts/generate_presentation_file.py "
                "--paper_info_path ${PAPER_INFO_PATH} "
                "--output_path ${TARGET} "
                "--template_path ${TEMPLATE_PATH}"
            )
        ),
        "GENERATE_OVERVIEW_FILE": Builder(
            action = (
                "python src/scripts/generate_overview.py "
                "--info_paths ${EDIT_FILES} "
                "--presentation_paths ${PRESENTATION_FILES} "
                "--output_path ${TARGET} "
                "--overview_template_path ${OVERVIEW_TEMPLATE} "
                "--overview_snippet_template_path ${SEGMENT_OVERVIEW_TEMPLATE} "
                "--project_information_path ${PROJECT_INFORMATION}"
            )
        ),


    },
)



pdf_files = glob.glob(os.path.join(f"{env['PDF_DIR']}", "*.pdf"))
topics = os.listdir(f"{env['TOPIC_DIR']}")

all_edit_files = []
all_presentation_files = []
all_topics = {topic : list() for topic in topics}

for pdf_file in pdf_files:
    pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
    edit_file = f"{env['EDIT_DIR']}/{pdf_name}.md"
    presentation_file = f"{env['PRESENTATION_DIR']}/{pdf_name}.md"

    edit_file = env.GENERATE_EDIT_FILE(
        target = edit_file,
        source = [pdf_file, "${EDIT_TEMPLATE}"],
        PDF_PATH = pdf_file,
        TEMPLATE_PATH = "${EDIT_TEMPLATE}",
    )
    env.Precious(edit_file)
    env.NoClean(edit_file)

    presentation_file = env.GENERATE_PRESENTATION_FILE(
        target = presentation_file,
        source = [edit_file, "${PRESENTATION_TEMPLATE}"],
        PAPER_INFO_PATH = edit_file,
        TEMPLATE_PATH = "${PRESENTATION_TEMPLATE}",
    )

    if os.path.exists(str(edit_file[0])):
        with open(str(edit_file[0]), "r") as fin:
            splits = fin.read().split("---", 3)
        try:
            paper_info = yaml.safe_load(splits[1])
        except Exception as e:
            print(e)
            print(str(edit_file[0]))

        for topic_name in paper_info["topics"]:
            if topic_name not in all_topics:
                continue
            all_topics[topic_name].append((edit_file, presentation_file))
    all_edit_files.append(edit_file)
    all_presentation_files.append(presentation_file)

for topic_path in all_topics:
    if len(all_topics[topic_path]) < 1:
        all_topic_edit_files, all_topic_presentation_files = [], []
    else:
        all_topic_edit_files, all_topic_presentation_files = zip(*all_topics[topic_path])
    topic_overview_file = env.GENERATE_OVERVIEW_FILE(
        target = f"{env['TOPIC_DIR']}/{topic_path}/README.md",
        source = [all_topic_edit_files,all_topic_presentation_files, "${TOPIC_OVERVIEW_TEMPLATE}", "${SEGMENT_OVERVIEW_TEMPLATE}", "$PROJECT_INFORMATION"],
        EDIT_FILES = all_topic_edit_files,
        PRESENTATION_FILES = all_topic_presentation_files,
        PROJECT_INFORMATION = f"{env['TOPIC_DIR']}/{topic_path}/topic.yaml",
        OVERVIEW_TEMPLATE = env["TOPIC_OVERVIEW_TEMPLATE"]
    )

overview_file = env.GENERATE_OVERVIEW_FILE(
    target = "README.md",
    source = [all_edit_files,all_presentation_files, "${OVERVIEW_TEMPLATE}", "${SEGMENT_OVERVIEW_TEMPLATE}", "${PROJECT_INFORMATION}"],
    EDIT_FILES = all_edit_files,
    PRESENTATION_FILES = all_presentation_files,
)