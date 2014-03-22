import yaml
import os
import subprocess
import copy

def sh(cmd, cwd=None):
    p = subprocess.Popen(cmd, cwd=cwd)
    p.wait()

pdfs = [
    ('Fyrir hádegi', 'fk_2014_trinity_fyrir_hadegi', [
        "bilad_lyklabord",
        "saldur_eratosthenesar",
        "eg_elska_hana",
        "gongutur",
        "rod",
        "hq9plus",
        "evil_odious",
        "teiknum_krossa",
        "popp",
    ]),
    ('Eftir hádegi', 'fk_2014_trinity_eftir_hadegi', [
        "netkerfi",
        "sjukdomagreining",
        "deiling",
        "ip_address",
        "bencoding",
        "tonlist",
        "ordasamsetning",
        "stofn_og_lauf_plott",
        "robotavandraedi",
    ])
]

# used = set()

for title, name, problems in pdfs:

    try:
        os.mkdir(name)
    except:
        pass

    sh(['cp', 'problem_template.tex', os.path.join(name, 'problem_template.tex')])

    for problem in problems:

        with open(os.path.join('../problems', problem, 'statement.md'), 'r') as f:
            statement = f.read()

        with open(os.path.join('../problems', problem, 'problem.yml'), 'r') as f:
            opts = yaml.load(f.read())

        fake_opts = copy.deepcopy(opts)

        for i in range(len(fake_opts['examples'])):
            fake_opts['examples'][i]['input'] = 'XINPUT%dX' % i
            fake_opts['examples'][i]['output'] = 'XOUTPUT%dX' % i

        with open(os.path.join(name, problem + '.md'), 'w') as f:
            f.write('---\n' + yaml.dump(fake_opts) + '\n...\n' + statement)

        sh(['pandoc', '-f', 'markdown', '-t', 'latex', '--template', 'problem_template.tex', '-o', problem + '.tex', problem + '.md'], cwd=name)

        with open(os.path.join(name, problem + '.tex'), 'r') as f:
            tex = f.read()


        for i in range(len(fake_opts['examples'])):
            # print(opts['examples'][i]['input'])
            # print(opts['examples'][i]['output'])
            # used |= set(opts['examples'][i]['input'])
            # used |= set(opts['examples'][i]['output'])
            # assert '~' not in opts['examples'][i]['input']
            # assert '~' not in opts['examples'][i]['output']
            # tex = tex.replace('XINPUT%dX' % i, '\\verb~' + opts['examples'][i]['input'] + '~')
            # tex = tex.replace('XOUTPUT%dX' % i, '\\verb~' + opts['examples'][i]['output'] + '~')
            tex = tex.replace('XINPUT%dX' % i, '\n'.join([ '\\verb~%s~\\\\' % line for line in opts['examples'][i]['input'].split('\n') ]))
            tex = tex.replace('XOUTPUT%dX' % i, '\n'.join([ '\\verb~%s~\\\\' % line for line in opts['examples'][i]['output'].split('\n') ]))

        with open(os.path.join(name, problem + '.tex'), 'w') as f:
            f.write(tex)

    with open(name + '.tex', 'r') as f:
        template = f.read()

    template = template.replace('__PROBLEMS__', '\n'.join( '\problemstatement{%s}' % problem for problem in problems ))

    with open(os.path.join(name, name + '.tex'), 'w') as f:
        f.write(template)

    sh(['cp', 'olymp.sty', os.path.join(name, 'olymp.sty')])
    sh(['latexmk', '-pdf', name + '.tex'], cwd=name)


# import string
# print(used)
# print(set(string.printable) - used)
