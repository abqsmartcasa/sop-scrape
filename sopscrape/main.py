from dataclasses import dataclass
from io import StringIO
import os
import re
from typing import Dict

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


class FileTypeException(Exception):
    pass


@dataclass
class SOP:
    number: int = 0
    effective_date: str = ""
    expires_date: str = ""
    replaces_date: str = ""


def scrape(filepath: str) -> Dict:
    sop = SOP()
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec="utf-8", laparams=laparams)
    _, file_extension = os.path.splitext(filepath)
    if file_extension != ".pdf":
        raise FileTypeException
    with open(filepath, "rb") as f:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        page = next(
            PDFPage.get_pages(
                f, set(), maxpages=1, caching=False, check_extractable=True
            )
        )
        interpreter.process_page(page)
        text = retstr.getvalue()
        text = text.replace("\n", "")
        match = re.search(r"SOP\s(\d{1}\-\d+)", text)
        try:
            sop.number = match.group(1)
        except AttributeError:
            pass
        match = re.search(r"Effective\:\s(\d{1,2}\/\d{2}\/\d{2})", text)
        try:
            sop.effective_date = match.group(1)
        except AttributeError:
            pass
        match = re.search(r"(Review\sDue|Expires)\:\s(\d{1,2}\/\d{2}\/\d{2})", text)
        try:
            sop.expires_date = match.group(2)
        except AttributeError:
            pass
        match = re.search(r"Replaces\:\s(\d{1,2}\/\d{2}\/\d{2})", text)
        try:
            sop.replaces_date = match.group(1)
        except AttributeError:
            pass
        return sop.__dict__
