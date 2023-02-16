import logging

from celery import shared_task
from imap_tools import MailBox
from paperless_mail.mail import BaseMailAction
from paperless_mail.mail import MailAccountHandler
from paperless_mail.mail import MailError
from paperless_mail.models import MailAccount

logger = logging.getLogger("paperless.mail.tasks")


@shared_task
def apply_mail_action(
    result: str,
    M: MailBox,
    action: BaseMailAction,
    message_uid: str,
    parameter: str,
):
    action.post_consume(M, message_uid, parameter)


@shared_task
def process_mail_accounts():
    total_new_documents = 0
    for account in MailAccount.objects.all():
        try:
            total_new_documents += MailAccountHandler().handl2e_mail_account(account)
        except MailError:
            logger.exception(f"Error while processing mail account {account}")

    if total_new_documents > 0:
        return f"Added {total_new_documents} document(s)."
    else:
        return "No new documents were added."
