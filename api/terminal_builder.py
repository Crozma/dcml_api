from pdf_reader import parse_pdf

# Globals

terminal_mode = 'cmd'
terminal_status = True


class DcmlWriter:

    # interne Methoden
    def set_mode(self, mode: str = None):
        global terminal_mode

        if mode is None:
            if self.write_mode is True:
                self.write_mode = False
                self.cmd_mode = True
                terminal_mode = 'cmd'
            elif self.cmd_mode is True:
                self.cmd_mode = False
                self.write_mode = True
                terminal_mode = 'write'
            return

        if mode == 'cmd':
            self.write_mode = False
            self.cmd_mode = True
            terminal_mode = 'cmd'
        elif mode == 'write':
            self.cmd_mode = False
            self.write_mode = True
            terminal_mode = 'write'

    def __init__(self):
        # Variable die den Inhalt speichert, der am Ende ins Dokument geschrieben wird

        self.tag_arg = ''
        self.page = None
        self.page_num = 0
        self.document_content = str()

        # Zwei Terminal-Modi

        self.cmd_mode = True
        self.write_mode = False

        # Zwischenspeicher

        self.mem_document_content = str()
        self.mem_cmd = str()
        self.mem_paragraph = list()
        self.mem_list = list()
        self.mem_list_item = str()
        self.mem_pdf_index = 0
        self.mem_task = list()
        self.mem_an = list()
        self.mem_rm = list()
        self.mem_img = list()
        self.mem_fz = list()
        self.mem_task_num = 0

        # Booleanchecks

        self.first_page = True
        self.zp_check = False
        self.task_first_call = True

        # Konstanten

        self.cmds_lib = {'?': self.help, 'help': self.help, 'body': self.body, 'save': self.save,
                         'page': self.page_func, 'p': self.paragraph, 'h1': (self.heading, 1), 'h2': (self.heading, 2),
                         'h3': (self.heading, 3), 'h4': (self.heading, 4), 'task': self.task, 'lb': self.lb,
                         'task1': self.task1, 'list': self.list, 'numpage': self.num_page, 'zp': self.zeilentext,
                         'endpage': self.end_page, 'startzp': self.start_zeilentext, 'fz': self.fusszeile,
                         'numtask': self.num_task, 'undo': self.undo, 'setpage': self.set_page,
                         'an': self.anmerkung, 'bn': self.bn, 'rm': self.rahmen, 'img': self.bild,
                         }
        self.non_write_cmds = ('?', 'help', 'page', 'body', 'bn', 'zp', 'endpage', 'startzp', 'undo')

    def write(self, usr_input: str):
        self.mem_document_content = self.document_content
        if self.zp_check:
            self.zeilentext(usr_input)
            return
        if self.mem_cmd.startswith('h'):
            self.cmds_lib.get(self.mem_cmd)[0](usr_input, self.mem_cmd[1])
            self.set_mode('cmd')
            return
        if self.mem_cmd == 'list':
            if usr_input == 'x':
                self.cmds_lib.get('list')(end_list=True)
                self.set_mode()
                return
            if usr_input == 'n':
                self.cmds_lib.get('list')(end_list_item=True)
                return
            self.cmds_lib.get('list')(body=usr_input)
            return
        if self.mem_cmd in ('p', 'lb'):
            if usr_input == 'x':
                self.cmds_lib.get(self.mem_cmd)(end=True)
                self.set_mode()
                return
            self.cmds_lib.get(self.mem_cmd)(body=usr_input)
            return
        if self.mem_cmd == 'numpage':
            self.num_page(usr_input)
            self.set_mode()
            return
        if usr_input == 'x':
            self.cmds_lib.get(self.mem_cmd)(body=None, end=True)
            self.set_mode('cmd')
            return

        self.cmds_lib.get(self.mem_cmd)(body=usr_input)

    def insert(self, usr_input: str):
        global terminal_mode

        if usr_input == 'exit':
            self.exit()
            return

        if self.cmd_mode:
            if usr_input in self.non_write_cmds:
                if usr_input == 'zp':
                    self.zp_check = True
                    self.zeilentext()
                    self.set_mode()
                    terminal_mode = 'zp'
                    return
                self.cmds_lib.get(usr_input)()
            elif usr_input in self.cmds_lib.keys():
                self.mem_cmd = usr_input
                self.set_mode('write')
                return

        elif self.write_mode:
            self.write(usr_input)

    def help(self):
        print('console> help')

    def body(self):
        print(self.document_content)

    def set_page(self, body: str):
        self.page_num = int(body)
        self.set_mode()

    def page_func(self):
        self.document_content += '</page>\n'
        self.document_content += '<page>\n'
        self.page_num += 1

    def num_page(self, body: str):
        try:
            self.page_num = int(body)
        except ValueError:
            print('console> Ungültige Eingabe, bitte Zahl eingeben')
            return

        if self.first_page:
            self.document_content += f'<page num={self.page_num}>\n'
            self.first_page = False
            return
        self.document_content += '</page>\n'
        self.document_content += f'<page num={self.page_num}>\n'

    def end_page(self):
        self.document_content += '</page>\n'

    def paragraph(self, body: str = None, end: bool = False):
        if end:
            self.document_content += '<p>\n'
            for line in self.mem_paragraph:
                self.document_content += line + '\n'
            self.document_content += '</p>\n'
            self.mem_paragraph = list()
            return

        self.mem_paragraph.append(body)

    def lb(self, body: str = None, end: bool = False):
        if end:
            self.document_content += '<p lb>\n'
            for line in self.mem_paragraph:
                self.document_content += line + '\n'
            self.document_content += '</p>\n'
            self.mem_paragraph = list()
            return

        self.mem_paragraph.append(body)

    def heading(self, body: str, level: int):
        self.document_content += f'<h{level}>\n'
        self.document_content += body + '\n'
        self.document_content += f'</h{level}>\n'

    def task(self, body: str, end: bool = False):
        if end:
            self.document_content += '<task>\n'
            for line in self.mem_task:
                self.document_content += line + '\n'
            self.document_content += '</task>\n'
            self.mem_task = list()
            return

        self.mem_task.append(body)

    def task1(self, body: str, end: bool = False):
        if end:
            self.document_content += '<task num=1>\n'
            for line in self.mem_task:
                self.document_content += line + '\n'
            self.document_content += '</task>\n'
            self.mem_task = list()
            return

        self.mem_task.append(body)

    def num_task(self, body: str, end: bool = False):
        if self.task_first_call:
            self.mem_task_num = body
            self.task_first_call = False
            return
        elif end:
            self.document_content += f'<task num={self.mem_task_num}>\n'
            for line in self.mem_task:
                self.document_content += line + '\n'
            self.document_content += '</task>\n'
            self.mem_task = list()
            self.task_first_call = True
            return

        self.mem_task.append(body)

    def list(self, body: str = None, end_list: bool = False, end_list_item: bool = False):
        if end_list:
            self.mem_list.append(self.mem_list_item + '\n')
            self.document_content += '<l>\n'
            for list_item in self.mem_list:
                self.document_content += list_item
            self.document_content += '</l>\n'
            self.mem_list_item = str()
            self.mem_list = list()
            return
        if end_list_item:
            self.mem_list.append(self.mem_list_item + '\n')
            self.mem_list_item = str()
        else:
            if self.mem_list_item != '':
                self.mem_list_item += ' ' + body
                return
            self.mem_list_item += body

    def anmerkung(self, body: str, end: bool = False):
        if end:
            self.document_content += '<an>\n'
            for line in self.mem_an:
                self.document_content += line + '\n'
            self.document_content += '</an>\n'
            self.mem_an = list()
            return

        self.mem_an.append(body)

    def bn(self):
        self.document_content += '<bn></bn>\n'

    def rahmen(self, body: str, end: bool = False):
        if end:
            self.document_content += '<rm>\n'
            for line in self.mem_rm:
                self.document_content += line + '\n'
            self.document_content += '</rm>\n'
            self.mem_rm = list()
            return

        self.mem_rm.append(body)

    def zeilentext(self, args: str = None, start: bool = False):
        if args is None:
            self.tag_arg = ' type=start' if start else ''
            self.page: list[str] = parse_pdf(self.page_num)
            print(self.page[0])
            print('\nEnter b to go one part backwards. Enter n to see the next part. Enter k to select the part as '
                  'the text. Enter s to switch to manual mode')
        else:
            if args == 'n':
                if self.mem_pdf_index != len(self.page) - 1:
                    self.mem_pdf_index += 1
                    print(self.page[self.mem_pdf_index])
            elif args == 'b':
                if self.mem_pdf_index != 0:
                    self.mem_pdf_index -= 1
                    print(self.page[self.mem_pdf_index])

            elif args == 'k':
                if self.page[self.mem_pdf_index].strip().endswith(')'):
                    self.document_content += f'<zp{self.tag_arg}>\n'
                    self.document_content += self.page[self.mem_pdf_index].strip().removesuffix(
                        self.page[self.mem_pdf_index][-6:]
                    )
                    self.document_content += '</zp>\n'
                    self.document_content += f'<p>\n'
                    self.document_content += self.page[self.mem_pdf_index][-6:].strip() + '\n'
                    self.document_content += '</p>\n'
                    self.tag_arg = ''
                    return
                self.document_content += f'<zp{self.tag_arg}>\n'
                self.document_content += self.page[self.mem_pdf_index].strip() + '\n'
                self.document_content += '</zp>\n'
                self.tag_arg = ''
                self.mem_pdf_index += 1
                print(self.page[self.mem_pdf_index])
            elif args == 'r':
                self.mem_pdf_index = 0
            elif args == 'x':
                self.zp_check = False
                self.set_mode('cmd')
                self.tag_arg = ''
                self.mem_pdf_index = 0

    def fusszeile(self, body: str, end: bool = False):
        if end:
            self.document_content += '<fz>\n'
            for line in self.mem_fz:
                self.document_content += line + '\n'
            self.document_content += '</fz>\n'
            self.mem_fz = list()
            return

        self.mem_fz.append(body)

    def start_zeilentext(self):
        global terminal_mode

        self.zp_check = True
        self.zeilentext(start=True)
        self.set_mode()
        terminal_mode = 'zp'

    def bild(self, body: str, end: bool = False):
        if end:
            self.document_content += '<bild>\n'
            for line in self.mem_img:
                self.document_content += line + '\n'
            self.document_content += '</bild>\n'
            self.mem_img = list()
            return

        self.mem_img.append(body)

    def undo(self):
        self.document_content = self.mem_document_content

    def save(self, body: str):
        self.set_mode()
        print(self.document_content)
        self.document_content = self.document_content.replace('\t', ' ')

        if body == '-d':
            with open('input/pages.dcml', 'w', encoding='utf-8') as document_file:
                document_file.write(self.document_content)
                document_file.close()
            return
        elif body == '-a':
            with open('input/pages.dcml', 'a', encoding='utf-8') as document_file:
                document_file.write(self.document_content)
                document_file.close()
            self.document_content = ''
            return
        with open(f'input/{body}.dcml', 'w', encoding='utf-8') as document_file:
            document_file.write(self.document_content)
            document_file.close()

    def exit(self):
        global terminal_status
        terminal_status = False


def terminal():
    writer = DcmlWriter()
    while terminal_status:
        user_input = input(f'{terminal_mode}> ')
        writer.insert(user_input)


if __name__ == '__main__':
    terminal()
