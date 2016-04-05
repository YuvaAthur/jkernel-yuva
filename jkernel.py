from __future__ import print_function

from ipykernel.kernelbase import Kernel

import base64
import os

from wrapper import JWrapper

# CUSTOMIZE HERE
# Viewmat creates a temporary picture file in order to display it.
# This is the path the kernel will use to find it.
j_viewmat_image_location = "~/j64-804-user/temp/viewmat.png"

class JKernel(Kernel):
    implementation = 'jkernel'
    implementation_version = '0.1'
    language_info = {
        'mimetype': 'text/plain',
        'name': 'J',
        'file_extension': 'ijs'
    }
    banner = "J language kernel"
    help_links = [
        {'text': 'Vocabulary', 'url': 'http://www.jsoftware.com/help/dictionary/vocabul.htm'},
        {'text': 'NuVoc', 'url': 'http://www.jsoftware.com/jwiki/NuVoc'}
    ]

    def __init__(self, *args, **kwargs):
        super(JKernel, self).__init__(*args, **kwargs)
        self.j = JWrapper()

        assert self.j.sendline("2+2") == "4\n" # make sure everything's working fine

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):

        lines = code.splitlines()

        generates_image = True if lines[-1].startswith("viewmat ") or lines[-1].startswith("viewrgb ") else False

        output = self.j.sendlines(lines)

        if not silent:

            def handle_text_response():
                if not output:
                    return
                stream_content = {'name': 'stdout', 'text': output}
                self.send_response(self.iopub_socket, 'stream', stream_content)

            def handle_image_response():
                image_path = os.path.expanduser(j_viewmat_image_location)
                with open(image_path, "rb") as file:
                    file = base64.b64encode(file.read()).decode()
                os.remove(image_path)

                stream_content = {
                    'source': 'meh',
                    'data': {'image/png': file},
                    'metadata': {'image/png': {'width': 300, 'height': 300}}
                }
                self.send_response(self.iopub_socket, 'display_data', stream_content)

            if not generates_image:
                handle_text_response()
            else:
                try:
                    handle_image_response()
                except:
                    handle_text_response()

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

    def do_shutdown(self, restart):
        self.j.close()

    def do_inspect(self, code, cursor_pos, detail_level=0):

        inspection = ""

        code += "\n"
        line = code[code.rfind("\n", 0, cursor_pos)+1 : code.find("\n", cursor_pos)]

        line_pos = cursor_pos - code.rfind("\n", 0, cursor_pos) - 2

        found = False

        if line[line_pos].isalnum():
            i, j = line_pos, line_pos
            while i > 0 and line[i-1].isalnum() or line[i-1] == "_":
                i -= 1
            while j < len(line)-1 and line[j+1].isalnum() or line[j+1] == "_":
                j += 1
            if line[i].isalpha():
                if j == len(line)-1 or line[j+1] not in ".:":
                    name = line[i:j+1]
                    inspection = self.j.sendline(name)
                    found = True

        return {
            'status': 'ok',
            'data': {'text/plain': inspection},
            'metadata': {},
            'found': found
        }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=JKernel)