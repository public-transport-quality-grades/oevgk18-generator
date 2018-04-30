from typing import Dict
import logging

logger = logging.getLogger(__name__)


def parse_params(params: Dict):
    logger.debug(f"parsing parameters {params}")
