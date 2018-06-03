import datetime
import json
import logging
from os import path, makedirs
from typing import List

from .util import filename_parser

logger = logging.getLogger(__name__)


def write_metadata(output_config: dict, due_dates: List[dict]):
    metadata = {
        'generated-on': datetime.datetime.today().isoformat(),
        'generated-gradings': []
    }

    for index, due_date_config in enumerate(due_dates):
        due_date_properties = due_date_config.copy()
        due_date_properties['due-date'] = due_date_config['due-date'].isoformat()
        grading = {
            'id': index,
            'filename': filename_parser.get_filename_from_due_date_config(due_date_config)
        }
        grading.update(due_date_properties)
        metadata['generated-gradings'].append(grading)

    output_dir = output_config['output-directory']
    if not path.exists(output_dir):
        makedirs(output_dir)

    output_path = path.join(output_dir, output_config['metadata-filename'])
    with open(output_path, 'w') as fp:
        json.dump(metadata, fp)
