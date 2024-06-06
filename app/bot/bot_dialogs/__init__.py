from .dialogs import email_dialogs, settings, mailing_dialogs, scheduled_mailings_dialogs


dialogs = [
    email_dialogs.email_main_dialog,
    email_dialogs.email_adding_dialog,
    settings.settings_main_dialog,
    mailing_dialogs.mailing_dialog,
    scheduled_mailings_dialogs.scheduled_mailings_dialog,
]


__all__ = [
    'dialogs'
]


