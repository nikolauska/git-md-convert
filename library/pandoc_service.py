import pypandoc

class BasePandocService(object):
    """
    Base class for converting provided HTML to a doc or docx
    """
    file_object = None

    def __init__(self):
        self.service = self.get_service()

    def get_service(self):
        return pypandoc

    def generate(self, **kwargs):
        raise NotImplementedError


class PandocPDFService(BasePandocService):
    """
    Generate markdown to pdf format
    """
    def generate(self, markdown, **kwargs):
        """
        generate the pdf but needs to be set as tex so pandoc handles it
        correctly see docs: http://johnmacfarlane.net/pandoc/ #search pdf
        """
        to_file = kwargs.get('to_file', '')

        extra_args = (
            '--smart',
            '--standalone'
        )
        try:
            # generate it using pandoc
            self.service.convert_file(markdown, 'tex', format='md',
                    outputfile=to_file, extra_args=extra_args)
        except:
            print("Failed to generate file!")


class PandocHTMLService(BasePandocService):
    """
    Generate markdown to html format
    """
    def generate(self, markdown, **kwargs):
        to_file = kwargs.get('to_file', '')

        extra_args = (
            '--smart',
            '--standalone'
        )
        try:
            # generate it using pandoc
            self.service.convert_file(markdown, 'html', format='md',
                    outputfile=to_file, extra_args=extra_args)
        except:
            print("Failed to generate file!")
