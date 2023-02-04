import json
from src.project.app import aws
from botocore.exceptions import ClientError


def send_email(name: str, address: str, subject: str, body: str):
    print("Sending email to {name} ({address})")
    print("==================================-")
    print(f"Subject: {subject}")
    print(body)


class EmailService:
    def __init__(self, to_address: str, subject: str):
        self._to = []
        self._cc = []
        self._bcc = []

        self._to.append(to_address)
        self._subject = subject
        self._html = None
        self._text = None

        self._from_address = "Morfi <no-reply@morfi.pro>"
        self._reply_address = "no-reply@morfi.pro"
        self._return_path = "no-reply@morfi.pro"

    def add_to(self, email: str):
        self._to.append(email)

    def add_cc(self, email: str):
        self._cc.append(email)

    def add_bcc(self, email: str):
        self._bcc.append(email)

    def subject(self, subject: str):
        self._subject = subject

    def body(self, html: str, plain: str):
        self._html = html
        self._text = plain

    def template(self, filename: str, context: dict):
        self._html = self._render(filename, context)

    def reset(self):
        self._subject = None
        self._to = []
        self._cc = []
        self._bcc = []
        self._html = None
        self._text = None

    def send(self):

        ses = aws.get_client("ses")

        response = None

        try:

            response = ses.send_email(
                Destination={
                    "BccAddresses": self._bcc,
                    "CcAddresses": self._cc,
                    "ToAddresses": self._to,
                },
                Message={
                    "Body": {
                        "Html": {"Charset": "UTF-8", "Data": self._html},
                        "Text": {"Charset": "UTF-8", "Data": self._text},
                    },
                    "Subject": {"Charset": "UTF-8", "Data": self._subject},
                },
                Source=self._from_address,
            )

        except ses.exceptions.MessageRejected as error:
            print(error)
        except ClientError as error:
            print(error)
        finally:
            self.reset()

        return response

    def send_ses_template(self, template_name: str, context: dict):

        ses = aws.get_client("ses")
        response = None

        try:
            response = ses.send_templated_email(
                Source=self._from_address,
                Destination={"ToAddresses": self._to},
                ReplyToAddresses=[self._reply_address],
                Template=template_name,
                TemplateData=json.dumps(context),
            )
        except ses.exceptions.MessageRejected as error:
            print(error)
        except ses.exceptions.TemplateDoesNotExistException as error:
            print(error)
        except ClientError as error:
            print(error)
        finally:
            self.reset()

        return response


class SesTemplates:
    """
    Handles Amazon Simple Email Service Templates.
    """

    @classmethod
    def get_templates(cls):
        ses = aws.get_client("ses")
        return ses.list_templates()
