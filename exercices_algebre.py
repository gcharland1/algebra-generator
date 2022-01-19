import random
import subprocess


def add_sous(x=None, x_max=40, a_max=30, exp='x', positive=False):
    if x is None:
        x = get_new_int(lim=x_max, positive=positive, exclusions=[0])

    a = get_new_int(lim=a_max, positive=False, exclusions=[0, -x])
    y = x + a

    if random.randint(0, 1) > 0:
        if a < 0:
            return_exp = f'{exp} - {abs(a)}'
        else:
            return_exp = f'{exp} + {a}'
    else:
        return_exp = f'{a} + {exp}'

    return return_exp, x, y


def div_multi(x=None, x_max=20, a_max=9, exp='x', latex=False, positive=False):
    if len(exp) > 1 and not exp.startswith('(') == '(' and not exp.endswith('^2'):
        exp = '(' + exp + ')'

    if x is None:
        x = get_new_int(lim=x_max, positive=positive, exclusions=[0, 1])

    a = get_new_int(lim=a_max, positive=positive, exclusions=[0, 1])

    y = a * x
    if random.randint(0, 1) > 0:
        # y = a*x
        if latex:
            return f'{a}{exp}', x, y
        else:
            return f'{a}*{exp}', x, y
    else:
        # a = y/x
        if latex:
            return f'\\frac{{ {y} }}{{ {exp} }}', x, a
        else:
            return f'{y}/{exp}', x, a


def expo(x=None, x_max=10, exp='x', latex=False, positive=True):
    if len(exp) > 1:
        exp = '(' + exp + ')'

    if x is None:
        x = get_new_int(lim=x_max, positive=positive, exclusions=[0, 1])

    y = x ** 2
    if latex:
        return f'{{ {exp} }}^2', x, y
    else:
        return f'{exp}**2', x, y


def get_new_int(lim=20, positive=False, exclusions=None):
    if exclusions is None:
        exclusions = [0]
    x = 0
    while x in exclusions:
        if positive:
            x = random.randint(0, lim)
        else:
            x = random.randint(-1 * lim, lim)

    return x


def generate_exercice(operations='+', x=None, exp='x', latex=False, positive=None):
    if positive is None:
        positive = '^' in operations

    if len(operations) == 1:
        op = operations[0]
        if op == '+':
            return add_sous(x=x, exp=exp, positive=positive)

        elif op == '*':
            return div_multi(x=x, exp=exp, latex=latex, positive=positive)

        elif op == '^':
            return expo(x=x, exp=exp, latex=latex, positive=positive)

    else:
        y = None
        exp = 'x'
        counter = 0
        for op in operations:
            exp, x, y = generate_exercice(operations=op, x=y, exp=exp, latex=latex, positive=positive)
            counter += 1
            if counter == 1:
                x1 = x

    return exp, x1, y


def import_tex_fragment(f, src_file):
    with open(src_file, 'r') as src:
        for line in src:
            f.write(line)


def append_exercice_to_file(f, eq, answer, n=0, last=False):
    if n > 0:
        line = f'{n}) & '
    else:
        line = '& '

    if last:
        line += f'{eq} & x = {answer} \n'
    else:
        line += f'{eq} & x = {answer} \\\\ \n'

    f.write(line)


def gen_random_operation_sequence(depth=4):
    seq = random.sample(['+', '*', '^'], 1)[0]
    for i in range(depth-1):
        op = seq[-1]
        while op == seq[-1]:
            op = random.sample(['', '+', '*', '^'], 1)[0]
        seq += op
    print(seq)
    return seq


def append_section_to_file(f, title, qty, exercices=None):
    f.write('\\section{' + title + '}\n\n')
    f.write('\\begin{longtable}{l p{.75\\textwidth} r}\n')
    for i in range(qty):
        if exercices is None:
            op = gen_random_operation_sequence()
        elif len(exercices) == 1:
            op = exercices[0]
        else:
            op_id = random.randint(0, len(exercices) - 1)
            op = exercices[op_id]

        exp, x, y = generate_exercice(operations=op, latex=True)
        eq, ans = f'{exp} = {y}', x
        append_exercice_to_file(f, f'${eq}$', ans, n=i + 1, last=(i == qty - 1))

    f.write('\\end{longtable}\n\n')


def gen_exercice_sheet():
    tex_file = 'latex/exercices_algebre.tex'
    output_dir = 'latex/out'

    with open(tex_file, 'w') as f:
        import_tex_fragment(f, 'latex/header.txt')
        append_section_to_file(f, 'Add., Sous., Multip, Division', qty=30, exercices=['+', '+*', '*', '*+'])
        append_section_to_file(f, 'Carrés', qty=30, exercices=['^', '^+', '^*', '*^', '+^'])
        append_section_to_file(f, "Aléatoire", qty=100, exercices=None)
        import_tex_fragment(f, 'latex/footer.txt')

    cmd = ['pdflatex', '--output-directory', output_dir, tex_file]
    proc = subprocess.Popen(cmd)
    proc.communicate()


if __name__ == '__main__':
    gen_exercice_sheet()
