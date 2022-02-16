#! /usr/bin/python3

import math,time

class oblist:
    args=[]
    jemma=[]
    NNN_t="t"

def repl():
    while True:
        Nprint(Neval(parse(input("> "))))
        print('')

def oblist_name2(x):
    x=x.replace('+','Nplus').replace('-','Nminus').replace('*','Ntimes').replace('/','Ndivide').replace('[','Nvhaka')
    x=x.replace(']','Nohaka').replace('.','Npiste').replace('<','Nless').replace('>','Ngreater').replace('=','Nequal')
    x=x.replace('`',"Lapo").replace('@',"Miumau").replace('%',"Nperc")
    return f'NNN_{x}'

def oblist_name(x):
    return f'oblist.{oblist_name2(x)}'

def parse(program):
    a,b=readtokens(tokenize(program))
    return a

def tokenize(s):
    return s.replace('(',' ( ').replace(')',' ) ').replace("'"," ' ").replace(","," , ").split()

def readrest(tokens):
    if tokens==[]: return [],[]
    eka,tokens2=readtokens(tokens)
    if eka==')':
        return [],tokens2
    if eka=='.':
        toka,tokens3=readtokens(tokens2)
        turha,tokens4=readtokens(tokens3)
        if turha != ")" : print('SYNTAX ERROR')
        return toka,tokens4
    else:
        toka,tokens3=readrest(tokens2)
        if toka==[] : return [eka],tokens3 
        else: return [eka,toka],tokens3
    
def readtokens(tokens):
    if tokens==[]: return [],[]
    token = tokens.pop(0)
    if '(' == token:
        return readrest(tokens)
    elif ')' == token:
        return token,tokens
    elif '.' == token:
        return token,tokens
    elif "'" == token:
        yksi,tokens2=readtokens(tokens)
        return ["quote",[yksi]],tokens2
    else:
        return atomi(token),tokens

def atomi(token):
    token=str(token)
    try: return int(token)
    except:
        try: return float(token)
        except: return token

def car(x):
    if atom(x): return []
    try: return x[0]
    except: return []

def cdr(x):
    if atom(x): return []
    try: return x[1]
    except: return []

def cadr(x):
    return car(cdr(x))

def cddr(x):
    return cdr(cdr(x))

def caddr(x):
    return car(cddr(x))

def atom(x):
    if x==[]: return True
    return type(x) != type([1])

def Nprintrest(x):
    if x==[] :
        print(")",end='')
    elif atom(x):
        print(" . ",x,")",end='')
    else:
        Nprint(car(x))
        if cdr(x)!=[]: print(" ",end='')
        Nprintrest(cdr(x))
        
def Nprint(x):
    if atom(x):
        if x==[]:
            print('()',end='')
        else:
            print(x,end='')
    elif car(x)=='quote':
        print("'",end='')
        Nprint(car(cdr(x)))
    else:
        print("(",end='')
        Nprintrest(x)
    return x

def Neval(x):
    if type(x)==type(car):
        return x(oblist.args.pop())
    elif atom(x):
        if x==[] :
            return []
        try:
            return int(x)
        except:
            try:
                return float(x)
            except:
                return value_of(x)
    else:
        oblist.args.append(cdr(x))
        return Neval(Neval(car(x)))
    
def value_of(x):
   try:
       exec(f'oblist.temp={oblist_name(x)}')
       return oblist.temp
   except:
       if identp(x): exec(f'{oblist_name(x)}=[]')
       return []

def setq(x,y):
    z=Neval(y)
    try:
        exec(f'{oblist_name(x)}={z}')
    except:
        try:
            setattr(oblist,oblist_name2(x),z)
        except: pass
    return z

def defq(x,y):
    try:
        exec(f'{oblist_name(x)}={y}')
    except:
        exec(f'{oblist_name(x)}="{y}"')
    return x

def lsp(x):
    Neval(parse(x))

def cons(x,y):
    return [x,y]

def Nlist(x):
    if atom(x): return x
    else:
        return cons(Neval(car(x)),Nlist(cdr(x)))

def identp(x):
    return type(x)==type("a")
        
def save_vars_list(x):
    if atom(x):
        if identp(x):
            try: exec(f'oblist.jemma.append({oblist_name(x)})')
            except: exec(f'oblist.jemma.append([])')
    else:
        save_vars_list(car(x))
        save_vars_list(cdr(x))
    
def restore_vars_list(x):
    if atom(x):
        if identp(x):
            exec(f'{oblist_name(x)}=oblist.jemma.pop()')
    else:
        restore_vars_list(cdr(x))
        restore_vars_list(car(x))

def assign_vars(x,y):
    if atom(x):
        if identp(x):
           try:
               exec(f'{oblist_name(x)}={y}')
           except:
               if identp(y):
                   exec(f'{oblist_name(x)}="{y}"')
               else:
                   setattr(oblist,oblist_name2(x),y)
    else:
        assign_vars(car(x),car(y))
        assign_vars(cdr(x),cdr(y))


def Nprogn(x):
    tul=Neval(car(x))
    if cdr(x) == []:
        return tul
    else:
        return Nprogn(cdr(x))

def Nlambda(vars,args,y):
    z=Nlist(args)
    save_vars_list(vars)
    assign_vars(vars,z)
    tulos=Nprogn(y)
    restore_vars_list(vars)
    return tulos

def Nmacroexpand(vars,args,y):
    z=args
    save_vars_list(vars)
    assign_vars(vars,z)
    tulos=Nprogn(y)
    restore_vars_list(vars)
    return tulos

def Nmacro(vars,args,y):
    return Neval(Nmacroexpand(vars,args,y))

def Nif(x,y,z):
    if Neval(x)!=[]:
        return Neval(y)
    else:
        return Neval(z)

def Nand(x):
    tempo=Neval(car(x))
    if tempo==[]:
        return []
    elif cdr(x)==[]:
        return tempo
    else:
        return Nand(cdr(x))

def Nor(x):
    tempo=Neval(car(x))
    if tempo!=[]:
        return tempo
    elif cdr(x)==[]:
        return []
    else:
        return Nor(cdr(x))
    
def Ntest(x):
    if x:
        return "T"
    else:
        return []
 
def Nwhile(x,y):
    while Neval(x)!=[]:
        tul=Nprogn(y)       
    return []

def Nrepeat_times(x,y):
    x=int(x)
    z=[]
    while x>0:
        z=Nprogn(y)
        x=x-1
    return z

defq('plus', 'lambda x: Neval(car(x))+Neval(cadr(x))')
defq('minus','lambda x: Neval(car(x))-Neval(cadr(x))')
defq('times','lambda x: Neval(car(x))*Neval(cadr(x))')
defq('quotient','lambda x: Neval(car(x))/Neval(cadr(x))')
defq('eqn','lambda x: Ntest(Neval(car(x))==Neval(cadr(x)))')
defq('eq','lambda x: Ntest(Neval(car(x))==Neval(cadr(x)))')
defq('lessp','lambda x: Ntest(Neval(car(x))<Neval(cadr(x)))')
defq('greaterp','lambda x: Ntest(Neval(car(x))>Neval(cadr(x)))')
defq('atom','lambda x: Ntest(atom(Neval(car(x))))')
defq('print','lambda x: Nprint(Neval(car(x)))')
defq('quote','lambda x: car(x)')
defq('setq','lambda x: setq(car(x),cadr(x))')
defq('set','lambda x: setq(Neval(car(x)),cadr(x))')
defq('defq','lambda x: defq(car(x),cadr(x))')
defq('cons', 'lambda x: [Neval(car(x)),Neval(cadr(x))]')
defq('car', 'lambda x: car(Neval(car(x)))')
defq('cdr', 'lambda x: cdr(Neval(car(x)))')
defq('list', 'lambda x: Nlist(x)')
defq('lambda', 'lambda x: Nlambda(car(x),oblist.args[-1],cdr(x))')
defq('progn', 'lambda x: Nprogn(x)')
defq('macro', 'lambda x: Nmacro(car(car(x)),oblist.args[-1],cdr(x))')
defq('macrotest', 'lambda x: Nmacroexpand(car(car(x)),oblist.args[-1],cdr(x))')
defq('if', 'lambda x: Nif(car(x),cadr(x),caddr(x))')
defq('and', 'lambda x: Nand(x)')
defq('or', 'lambda x: Nor(x)')
defq('cr', 'lambda x: print("")')
defq('sp', 'lambda x: print(" ",end="")')
defq('lb', 'lambda x: print("(",end="")')
defq('rp', 'lambda x: print(") ",end="")')
defq('while', 'lambda x: Nwhile(car(x),cdr(x))')
defq('eval', 'lambda x: Neval(Neval(car(x)))')
defq('repeat-times', 'lambda x: Nrepeat_times(Neval(car(x)),cdr(x))')

lsp("(defq defun (macro (x) (list 'defq (car x) (cons 'lambda (cdr x)))))")
lsp("(defq defmacro (macro (x) (list 'defq (car x) (cons 'macro (cdr x)))))")
lsp("(defq defmacrotest (macro (x) (list 'defq (car x) (cons 'macrotest (cdr x)))))")

lsp('(defun cadr (x) (car (cdr x)))')
lsp('(defun cddr (x) (cdr (cdr x)))')
lsp('(defun cdddr (x) (cdr (cddr x)))')
lsp('(defun caddr (x) (car (cddr x)))')
lsp('(defun cadddr (x) (car (cdddr x)))')

lsp("""(defun arith-macroes ((x y . z) ope)
         (if z 
           (list ope (list ope x y) (arith-macroes z ope))
           (if y (list ope x y) x)))""")
lsp("(defmacro + (x) (arith-macroes x 'plus))")
lsp("(defmacro - (x) (arith-macroes x 'minus))")
lsp("(defmacro * (x) (arith-macroes x 'times))")
lsp("(defmacro / (x) (arith-macroes x 'quotient))")

lsp("""(defun comp-macroes ((x y . z) ope)
         (if z 
           (list 'and (list ope x y) (comp-macroes (cons y z) ope))
           (if y (list ope x y) x)))""")

lsp("(defmacro < (x) (comp-macroes x 'lessp))")
lsp("(defmacro > (x) (comp-macroes x 'greaterp))")
lsp("(defmacro = (x) (comp-macroes x 'equal))")

lsp("""(defun equal (x y)
          (or (eq x y) 
              (and 
               (car x)
               (car y)
               (equal (car x) (car y))
               (equal (cdr x) (cdr y)))))""")

lsp("""(defun atomcount (n x)
           (if (atom x)
               (+ n 1)
               (plus (atomcount n  (car x))(atomcount n (cdr x)))))""")

lsp("(defun tab (x) (if (lessp 0 x) (progn (sp) (tab (- x 1)))))")

lsp("""(defun pprint (x tabs)
           (or tabs (setq tabs 1))
           (if (lessp (atomcount 0 x) 20)
              (print x)
              (progn (lb)
               (while x 
                (pprint (car x) (+ 1 tabs))
                (if (cdr x) (progn (cr) (tab tabs))) 
                (setq x (cdr x)))
              (rb))))""")

lsp("""(defun cond-jatko (((x . y) . z))
           (list 'if x (cons 'progn y) (if z (cond-jatko z)))))""")
lsp("(defmacro cond (x) (cond-jatko x))")

lsp("(defun append  (x y) (if x (cons (car x) (append (cdr x) y)) y))")


lsp("""
 (defun fib (x)
    (if (< x 2)
        x
        (+ (fib (- x 1)) (fib (- x 2)))))""")


with open("bootpy.lsp","r") as f:
    c =f.read()
f.close
c="(progn "+c+"))))))"
lsp(c)


def repl():
    while True:
        Nprint(Neval(parse(input("> "))))
        print('')

repl()

    

