import random
import subprocess
import os

def add_sous(x = None, x_max = 40, a_max = 30, exp = 'x', latex=False, positive=False):
    if not x:
        x = get_new_int(lim=x_max, positive=positive)
   
    a = get_new_int(lim=a_max, positive=False, exclusions=[0])    
    y = x + a
    
    if random.randint(0, 1) > 0:
        if a < 0:
            return_exp = f'{exp} - {abs(a)}'
        else:
            return_exp = f'{exp} + {a}'
    else:
        return_exp = f'{a} + {exp}'        
    
    return return_exp, x, y


def div_multi(x = None, x_max = 20, a_max = 9, exp = 'x', latex=False, positive=False):
    if len(exp) > 1:
        exp= '(' + exp+ ')'
    
    if not x:
        x = get_new_int(lim=x_max, positive=positive)    

    a = get_new_int(lim=a_max, positive=positive, exclusions=[0, 1])
    
    y = a*x
    if random.randint(0, 1) > 0:
        if latex:
            return f'{a}{exp}', x, y
        else:
            return f'{a}*{exp}', x, y
    else:
        if latex:
            return f'\\frac{{ {y} }}{{ {exp} }}', x, a
        else:
            return f'{y}/{exp}', x, a

def expo(x = None, x_max = 10, exp = 'x', latex=False, positive=True):
    if len(exp) > 1:
        exp= '(' + exp+ ')'
    
    if not x:
        x = get_new_int(lim=x_max, positive=positive, exclusions=[0, -1, 1])
    
    y = x**2
    if latex:
        return f'{{ {exp} }}^2', x, y
    else:
        return f'{exp}**2', x, y
   
def get_new_int(lim = 20, positive = False, exclusions = [0]):
    x = 0
    while x in exclusions:
        if positive:
            x = random.randint(0, lim)
        else:
            x = random.randint(-1*lim, lim)

    return x

def generate_exercice(op = '+', latex=False):
    if op == '+':
        exp, x, y = add_sous(latex=latex)
        eq, ans = f'{exp} = {y}', x 

    elif op == '*':
        exp, x, y = div_multi(latex=latex)
        eq, ans = f'{exp} = {y}', x
    
    elif op == '^':
        exp, x, y = expo(latex=latex, positive=True)
        eq, ans = f'{exp} = {y}', x 
    elif op == '+*':
        exp, x, y = add_sous(latex=latex)
        exp2, x2, y2 = div_multi(x=y, exp=exp, latex=latex)
        eq, ans = f'{exp2} = {y2}', x

    elif op == '+^':
        exp, x, y = add_sous(latex=latex)
        exp2, x2, y2 = expo(x = y, exp=exp, latex=True, positive=(y>0))
        eq, ans = f'{exp2} = {y2}', x   
    
    elif op == '*+':
        exp, x, y = div_multi(latex=latex)
        exp2, x2, y2 = add_sous(x=y, exp=exp, latex=latex)
        eq, ans = f'{exp2} = {y2}', x
    
    elif op == '*^':
        exp, x, y = div_multi(latex=latex)
        exp2, x2, y2 = expo(x=y, exp=exp, latex=latex, positive=(y>0))
        eq, ans = f'{exp2} = {y2}', x

    elif op == '^+':
        exp, x, y = expo(latex=latex, positive=True)
        exp2, x2, y2 = add_sous(x=y, exp=exp, latex=latex)
        eq, ans = f'{exp2} = {y2}', x
    
    elif op == '^*':
        exp, x, y = expo(latex=latex, positive=True)
        exp2, x2, y2 = add_sous(x=y, exp=exp, latex=latex)
        eq, ans = f'{exp2} = {y2}', x 
    
    return eq, ans


def append_to_file(f, src_file):
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

def append_section_to_file(f, title, qty, exercices=['+', '*']):
    f.write('\\section{' + title + '}\n\n')
    f.write('\\begin{longtable}{l p{.75\\textwidth} r}\n')
    for i in range(qty):
        if len(exercices) == 1:
            op = exercices[0]
        else:
            op_id = random.randint(0, len(exercices)-1)
            op = exercices[op_id]

        eq, ans = generate_exercice(op = op, latex = True)
        append_exercice_to_file(f, f'${eq}$', ans, n=i+1, last=(i == qty-1))

    f.write('\\end{longtable}\n\nzo')

def gen_exercice_sheet():
    tex_file = 'latex/exercices_algebre.tex'
    output_dir = 'latex/out'

    with open(tex_file, 'w') as f:
        append_to_file(f, 'latex/header.txt')
        append_section_to_file(f, 'Addition et Soustraction', 30, exercices=['+'])
        append_section_to_file(f, 'Multiplication et Division', 30, exercices=['*'])
        append_section_to_file(f, 'Carrés', 30, exercices=['^', '^+', '^*', '*^', '+^'])
        append_section_to_file(f, "Combinaison d'opérations", 50, exercices=['+*', '*+'])
        append_section_to_file(f, "Aléatoire", 100, exercices=['+', '*', '+*', '*+'])
        append_to_file(f, 'latex/footer.txt')

    cmd = ['pdflatex', '--output-directory', output_dir, tex_file]
    proc = subprocess.Popen(cmd)
    proc.communicate()

if  __name__ == '__main__':
    gen_exercice_sheet()
    #print(generate_exercice('^*', True))
    #print(generate_exercice('^+', True))
    #print(generate_exercice('*^', True))
    #print(generate_exercice('*+', True))

