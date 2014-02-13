import time, datetime
import sys, os, shutil
from subprocess import Popen, PIPE, TimeoutExpired
sys.path.append('../../lib')
import judgelib as j
from judgelib import *

# j.TESTS_DIR = '../test_contest_1/tests'
# j.LANGUAGES_FILE = '../test_contest_1/languages.yml'
# j.DB_CONN_STRING = 'postgresql://test_contest_user:JBIkZ?xek04%5Z_k&J04@localhost:5432/test_contest'
j.TESTS_DIR = '../forritunarkeppni_framhaldsskolanna_2013/tests'
j.LANGUAGES_FILE = '../forritunarkeppni_framhaldsskolanna_2013/languages.yml'
j.DB_CONN_STRING = 'postgresql://test_contest_user:JBIkZ?xek04%5Z_k&J04@localhost:5432/test_contest'
TEMP_FOLDER = 'temp'

def process_submission(sub, check, time_limit, memory_limit, language, tests):
    verdicts = []
    tmp_sub_dir = os.path.join(TEMP_FOLDER, str(sub.id))
    judge_response = ""

    if os.path.exists(tmp_sub_dir):
        shutil.rmtree(tmp_sub_dir)

    os.makedirs(tmp_sub_dir)

    with open(os.path.join(tmp_sub_dir, language['filename']), 'w') as f:
        f.write(sub.file)

    # TODO: SafeExec
    if 'compile' in language:
        proc = Popen(language['compile'], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=tmp_sub_dir)
        comp_err = proc.communicate()[1]
        comp_err = '' if comp_err is None else comp_err.decode('utf-8')
        if proc.wait() != 0:
            sub.judge_response = """<h4>Compile error</h4><p><pre><code>%s</code></pre></p>""" % comp_err
            logger.debug('compile error:\n' + comp_err)
            return 'CE'

        logger.debug('compile successful')

    for test_no, test in enumerate(tests):
        logger.debug('running test %d' % test_no)

        # TODO: SafeExec
        proc = Popen(language['execute'], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=tmp_sub_dir)
        try:
            res = proc.communicate(test.input.encode('utf-8'), timeout=time_limit/1000.0)
            stdout = res[0].decode('utf-8')
            stderr = res[1].decode('utf-8')
        except TimeoutExpired:
            # TODO: kill program
            logger.debug('time limit exceeded')
            verdicts.append('TL')
        else:
            # TODO: check memory limit
            # TODO: check output limit
            # TODO: check presentation error
            if proc.returncode != 0:
                verdicts.append('RE')
                judge_response += """<h4>Runtime error on test %d</h4><p><pre><code>%s</code></pre></p>""" % (test_no+1, stderr)
                logger.debug('runtime error:\n' + stderr)
            else:
                try:
                    ok = check(expected=test.output, obtained=stdout)
                except Exception as e:
                    ok = False
                    logger.warning('exception occured in checker, treating as WA')
                    logger.exception(e)

                if ok:
                    verdicts.append('AC')
                    logger.debug('accepted')
                else:
                    verdicts.append('WA')
                    logger.debug('wrong answer')

    if judge_response:
        sub.judge_response = judge_response

    return verdicts

from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master.title('epsilon - judge')
        self.master.minsize(400, 350)
        self.pack(fill='both')

        # Menu
        self.main_menu = Menu(self)
        file_menu = Menu(self.main_menu, tearoff=0)
        file_menu.add_command(label='Exit', command=self.quit)
        self.main_menu.add_cascade(label='File', menu=file_menu)
        # self.main_menu.add_command(label='Refresh', command=self.refresh_data)
        self.main_menu.add_command(label='Queue', command=self.open_queue)
        self.main_menu.add_command(label='Judged', command=self.open_judged)
        self.master.config(menu=self.main_menu)

        self.body = Frame(self)
        self.body.pack()

        self.open_judged()

        # self.main_tabs = Notebook(self)

        # frm1 = Frame(self)

        # for i, sub in enumerate(j.get_all_submissions()):
        #     id_lb = Label(frm1, text=sub.id)
        #     id_lb.grid(row=i, column=0, stick='nsew', padx=10, pady=10)

        #     submitted_lb = Label(frm1, text=str(round(sub.submitted, 2)))
        #     submitted_lb.grid(row=i, column=1, stick='nsew', padx=10, pady=10)

        #     team_lb = Label(frm1, text=sub.team)
        #     team_lb.grid(row=i, column=2, stick='nsew', padx=10, pady=10)

        #     problem_lb = Label(frm1, text=sub.problem)
        #     problem_lb.grid(row=i, column=3, stick='nsew', padx=10, pady=10)

        #     verdict_lb = Label(frm1, text=sub.verdict)
        #     verdict_lb.grid(row=i, column=4, stick='nsew', padx=10, pady=10)

        # for column in range(5):
        #     frm1.grid_columnconfigure(column, weight=1)

        # frm1.pack(side='top', fill='both', padx=6, pady=12)
        # self.main_tabs.add(frm1, text='aecrh')

        # btn2 = Button(text='meow')
        # btn2.pack(side='top', fill='both', padx=6, pady=12)
        # self.main_tabs.add(btn2, text='meoooe')

        # self.main_tabs.pack(fill='both', expand=True)

    # def refresh_data(self):
    #     tkinter.messagebox.showinfo('Data refresh', 'Data being refreshed (not really)')

    def open_queue(self):
        self.body.pack_forget()
        self.body.destroy()
        self.body = Frame(self)
        self.body.pack()


    def open_judged(self):
        self.body.pack_forget()
        self.body.destroy()
        self.body = Frame(self)

        # yScroll = Scrollbar(self, orient=VERTICAL)
        # yScroll.grid(row=0, column=1, sticky='ns')
        # self.body = Frame(self, yscrollcommand=yScroll.set)
        # yScroll['command'] = self.body.yview

        Label(self.body, text='ID').grid(row=0, column=0, stick='nsew', padx=10, pady=10)
        Label(self.body, text='Submitted').grid(row=0, column=1, stick='nsew', padx=10, pady=10)
        Label(self.body, text='Team').grid(row=0, column=2, stick='nsew', padx=10, pady=10)
        Label(self.body, text='Problem').grid(row=0, column=3, stick='nsew', padx=10, pady=10)
        Label(self.body, text='Verdict').grid(row=0, column=4, stick='nsew', padx=10, pady=10)
        Label(self.body, text='Judge').grid(row=0, column=5, stick='nsew', padx=10, pady=10)

        for i, sub in enumerate(j.get_all_submissions() * 3):
            id_lb = Label(self.body, text=sub.id)
            id_lb.grid(row=i+1, column=0, stick='nsew', padx=10, pady=10)

            submitted_lb = Label(self.body, text=str(round(sub.submitted, 2)))
            submitted_lb.grid(row=i+1, column=1, stick='nsew', padx=10, pady=10)

            team_lb = Label(self.body, text=sub.team)
            team_lb.grid(row=i+1, column=2, stick='nsew', padx=10, pady=10)

            problem_lb = Label(self.body, text=sub.problem)
            problem_lb.grid(row=i+1, column=3, stick='nsew', padx=10, pady=10)

            verdict_lb = Label(self.body, text=sub.verdict)
            verdict_lb.grid(row=i+1, column=4, stick='nsew', padx=10, pady=10)

            verdict_btn = Button(self.body, text='Judge')
            verdict_btn.grid(row=i+1, column=5, stick='nsew', padx=10, pady=10)

        self.body.pack()


def main():
    app = Application()
    app.mainloop()

if __name__ == '__main__':
    main()


import tkinter.ttk as ttk
import tkinter as Tkinter

class Wizard(ttk.Notebook):
    def __init__(self, master=None, **kw):
        npages = kw.pop('npages', 3)
        kw['style'] = 'Wizard.TNotebook'
        ttk.Style(master).layout('Wizard.TNotebook.Tab', '')
        ttk.Notebook.__init__(self, master, **kw)

        self._children = {}

        for page in range(npages):
            self.add_empty_page()

        self.current = 0
        self._wizard_buttons()

    def _wizard_buttons(self):
        """Place wizard buttons in the pages."""
        for indx, child in self._children.items():
            btnframe = ttk.Frame(child)
            btnframe.pack(side='bottom', fill='x', padx=6, pady=12)

            nextbtn = ttk.Button(btnframe, text="Next", command=self.next_page)
            nextbtn.pack(side='right', anchor='e', padx=6)
            if indx != 0:
                prevbtn = ttk.Button(btnframe, text="Previous",
                    command=self.prev_page)
                prevbtn.pack(side='right', anchor='e', padx=6)

                if indx == len(self._children) - 1:
                    nextbtn.configure(text="Finish", command=self.close)

    def next_page(self):
        self.current += 1

    def prev_page(self):
        self.current -= 1

    def close(self):
        self.master.destroy()

    def add_empty_page(self):
        child = ttk.Frame(self)
        self._children[len(self._children)] = child
        self.add(child)

    def add_page_body(self, body):
        body.pack(side='top', fill='both', padx=6, pady=12)

    def page_container(self, page_num):
        if page_num in self._children:
            return self._children[page_num]
        else:
            raise KeyError("Invalid page: %s" % page_num)

    def _get_current(self):
        return self._current
    
    def _set_current(self, curr):
        if curr not in self._children:
            raise KeyError("Invalid page: %s" % curr)

        self._current = curr
        self.select(self._children[self._current])

    current = property(_get_current, _set_current)


# def demo():
#     root = Tkinter.Tk()
#     wizard = Wizard(npages=3)
#     wizard.master.minsize(400, 350)
#     page0 = ttk.Label(wizard.page_container(0), text='Page 1')
#     page1 = ttk.Label(wizard.page_container(1), text='Page 2')
#     page2 = ttk.Label(wizard.page_container(2), text='Page 3')
#     wizard.add_page_body(page0)
#     wizard.add_page_body(page1)
#     wizard.add_page_body(page2)
#     wizard.pack(fill='both', expand=True)
#     root.mainloop()
# 
# if __name__ == "__main__":
#     demo()

