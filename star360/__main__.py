import logging
from pathlib import Path
import sys

from .email import Star360MailMerge

BASE_DIR = Path(__file__).parent

logger = logging.getLogger(__name__)

mailer = Star360MailMerge(
    Path(Path(__file__).parent, 'out.csv'),
    debug=False,
)
try:
    with open(Path(BASE_DIR, 'sent.txt'), 'r') as txtf:
        sent = txtf.read()
        sent = [n.strip() for n in sent.split('\n')]
    mailer.skip = sent
    mailer.send_emails()
except Exception as e:
    logger.exception('exception')
    with open(Path(BASE_DIR, 'sent.txt'), 'a') as txtf:
        txtf.writelines([l + '\n' for l in mailer.sent_to])
    sys.exit()

with open(Path(BASE_DIR, 'sent.txt'), 'w') as txtf:
    txtf.write('')
