import sys
import re
import logging

from django.core import mail


class SafeAdminEmailHandler(logging.Handler):
    """An exception log handler that emails log entries to site admins

    If the request is passed as the first argument to the log record,
    request data will be provided in the
    """
    def emit(self, record):
        import traceback
        from admin_emails.conf import settings
        from django.views.debug import ExceptionReporter

        try:
            if sys.version_info < (2,5):
                # A nasty workaround required because Python 2.4's logging
                # module doesn't support passing in extra context.
                # For this handler, the only extra data we need is the
                # request, and that's in the top stack frame.
                request = record.exc_info[2].tb_frame.f_locals['request']
            else:
                request = record.request

            subject = '%s (%s IP): %s' % (
                record.levelname,
                (request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'),
                record.msg
            )
            request_repr = repr(request)
        except:
            subject = 'Error: Unknown URL'
            request = None
            request_repr = "Request repr() unavailable"

        if record.exc_info:
            exc_info = record.exc_info
            stack_trace = '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            exc_info = (None, record.msg, None)
            stack_trace = 'No stack trace available'

        message = "%s\n\n%s" % (stack_trace, request_repr)
        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        html_message = reporter.get_traceback_html()

        for pattern, repl in settings.ADMIN_EMAIL_MASK_PATTERNS:
        	html_message = re.sub(pattern, repl, html_message)
            
        mail.mail_admins(subject, message, fail_silently=True,
                         html_message=html_message)
