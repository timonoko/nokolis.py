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
        if toka==[] : return [eka,[]],tokens3 
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

def setq(x9,y):
    z=Neval(y)
    if identp(z):
        exec(f'{oblist_name(x9)}="{z}"')
    else:    
      try:
          exec(f'{oblist_name(x9)}={z}')
      except:
          try:
              setattr(oblist,oblist_name2(x9),z)
          except:
              pass
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
    return type(x)==type("abba")
        
def save_vars_list(x):
    if atom(x):
        if identp(x):
            try: exec(f'oblist.jemma.append({oblist_name(x)})')
            except: exec(f'oblist.jemma.append(x)')
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

def assign_vars(x2a9,y2a9):
    if atom(x2a9):
        if identp(x2a9):
          if identp(y2a9):
            exec(f'{oblist_name(x2a9)}="{y2a9}"')
          else:    
            try:
               exec(f'{oblist_name(x2a9)}={y2a9}')
            except:
               setattr(oblist,oblist_name2(x2a9),y2a9)
    else:
        assign_vars(car(x2a9),car(y2a9))
        assign_vars(cdr(x2a9),cdr(y2a9))


def Nprogn(x):
    tul=Neval(car(x))
    if cdr(x) == []:
        return tul
    else:
        return Nprogn(cdr(x))

def Nprog1(x):
    tul=Neval(car(x))
    if cdr(x) != []:
        Nprog1(cdr(x))
    return tul
        
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

def Nrplaca(x,y):
    x[0]=y
    return x

def Nrplacd(x2,y2):
    x2[1]=y2
    return x2

def Nlast(x):
    if cdr(x)==[]:
        return x
    else:
        return Nlast(cdr(x))

def Nnconc(x,y):
    Nrplacd(Nlast(x),y)
    return x

def Nnot(x):
    if x==[]:
        return "t"
    else:
        return []

def explode(word):
    return explo2([ord(char) for char in word])

def explo2(x):
    if x!=[]:
        return [x[0],explo2(x[1:])]
    else:
       return []

def compress(x):
     if x==[]:
         return ""
     else:
         return chr(x[0])+compress(x[1])
    
defq('plus', 'lambda x: Neval(car(x))+Neval(cadr(x))')
defq('minus','lambda x: Neval(car(x))-Neval(cadr(x))')
defq('times','lambda x: Neval(car(x))*Neval(cadr(x))')
defq('quotient','lambda x: Neval(car(x))/Neval(cadr(x))')
defq('remainder','lambda x: Neval(car(x))%Neval(cadr(x))')
defq('eqn','lambda x: Ntest(Neval(car(x))==Neval(cadr(x)))')
defq('eq','lambda x: Ntest(Neval(car(x))==Neval(cadr(x)))')
defq('lessp','lambda x: Ntest(Neval(car(x))<Neval(cadr(x)))')
defq('greaterp','lambda x: Ntest(Neval(car(x))>Neval(cadr(x)))')
defq('atom','lambda x: Ntest(atom(Neval(car(x))))')
defq('not','lambda x: Nnot(Neval(car(x)))')
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
defq('prog1', 'lambda x: Nprog1(x)')
defq('macro', 'lambda x: Nmacro(car(car(x)),oblist.args[-1],cdr(x))')
defq('mlambda', 'lambda x: Nmacro(car(x),oblist.args[-1],cdr(x))')
defq('macrotest', 'lambda x: Nmacroexpand(car(car(x)),oblist.args[-1],cdr(x))')
defq('nlambda', 'lambda x: Nmacroexpand(car(x),oblist.args[-1],cdr(x))')
defq('if', 'lambda x: Nif(car(x),cadr(x),caddr(x))')
defq('and', 'lambda x: Nand(x)')
defq('or', 'lambda x: Nor(x)')
defq('cr', 'lambda x: print("")')
defq('sp', 'lambda x: print(" ",end="")')
defq('lb', 'lambda x: print("(",end="")')
defq('rb', 'lambda x: print(")",end="")')
defq('while', 'lambda x: Nwhile(car(x),cdr(x))')
defq('eval', 'lambda x: Neval(Neval(car(x)))')
defq('repeat-times', 'lambda x: Nrepeat_times(Neval(car(x)),cdr(x))')
defq('read', 'lambda x: parse(input("> "))')
defq('rplaca', 'lambda x: Nrplaca(Neval(car(x)),Neval(cadr(x)))')
defq('rplacd', 'lambda x: Nrplacd(Neval(car(x)),Neval(cadr(x)))')
defq('last', 'lambda x: Nlast(Neval(car(x)))')
defq('nconc', 'lambda x: Nnconc(Neval(car(x)),Neval(cadr(x)))')
defq('identp', 'lambda x: Ntest(identp(Neval(car(x))))')
defq('type', 'lambda x: str(type(Neval(car(x))))')
defq('str-raw', 'lambda x: str(Neval(car(x)))')
defq('oblist', 'lambda x: str(dir(oblist))')
defq('oblist-name-raw', 'lambda x: str(oblist_name2(Neval(car(x))))')
defq('explode', 'lambda x: explode(Neval(car(x)))')
defq('compress', 'lambda x: compress(Neval(car(x)))')
defq('python-call', 'lambda x: exec(str(Neval(car(x)))+"("+str(Neval(cadr(x)))+")")')
defq('read-str', 'lambda x: input("? ")')

lsp(""" (progn
 (defq defun (macro (x) (list 'defq (car x) (cons 'lambda (cdr x)))))
 (defq defmacro (macro (x) (list 'defq (car x) (cons 'mlambda (cdr x)))))
 (defq defmacrotest (macro (x) (list 'defq (car x) (cons 'nlambda (cdr x)))))
 (defq defnacro (macro (x) (list 'defq (car x) (cons 'macro (cdr x)))))
 (defq defnacrotest (macro (x) (list 'defq (car x) (cons 'macrotest (cdr x)))))) """)

lsp(""" (progn
 (defun cadr (x) (car (cdr x)))
 (defun cddr (x) (cdr (cdr x)))
 (defun cdddr (x) (cdr (cddr x)))
 (defun caddr (x) (car (cddr x)))
 (defun cadddr (x) (car (cdddr x)))
 (defun caar (x) (car (car x))) 

 (defun arith-macroes ((x y . z) ope)
         (if z 
           (list ope (list ope x y) (arith-macroes z ope))
           (if y (list ope x y) x)))
 (defnacro + (x) (arith-macroes x 'plus))
 (defnacro - (x) (arith-macroes x 'minus))
 (defnacro * (x) (arith-macroes x 'times))
 (defnacro / (x) (arith-macroes x 'quotient))

 (defun comp-macroes ((x y . z) ope)
         (if z 
           (list 'and (list ope x y) (comp-macroes (cons y z) ope))
           (if y (list ope x y) x)))

 (defnacro < (x) (comp-macroes x 'lessp))
 (defnacro > (x) (comp-macroes x 'greaterp))
 (defnacro = (x) (comp-macroes x 'equal))

 (defun equal (x y)
          (or (eq x y) 
              (and 
               (car x)
               (car y)
               (equal (car x) (car y))
               (equal (cdr x) (cdr y)))))

 (defun member (x y)
  (if y (if (equal x (car y))
            y
            (member x (cdr y)))))

 (defun assoc (x y)
  (if y (if (equal x (caar y))
            (car y)
            (assoc x (cdr y)))))

(defun reverse
 (x)
 (if
  (cdr x)
  (nconc (reverse (cdr x)) (list (car x)))
  (list (car x))))


 (defun atomcount (n x)
           (if (atom x)
               (+ n 1)
               (plus (atomcount n  (car x))(atomcount n (cdr x)))))

 (defun tab (x) (if (lessp 0 x) (progn (sp) (tab (- x 1)))))

 (defun pprint (x tabs)
           (or tabs (setq tabs 1))
           (if (lessp (atomcount 0 x) 20)
              (print x)
              (progn (lb)
               (while x 
                (pprint (car x) (+ 1 tabs))
                (if (cdr x) (progn (cr) (tab tabs))) 
                (setq x (cdr x)))
              (rb))))

(defun nthcdr (x y) (if (= x 0) y (nthcdr (- x 1) (cdr y))))
(defun nth (x y) (car (nthcdr x y)))


 (defun cond-jatko (((xZ . yZ) . zZ))
           (list 'if xZ (cons 'progn yZ) (if zZ (cond-jatko zZ))))

 (defnacro cond (xZ) (cond-jatko xZ)))

)))""")

lsp(""" (progn 

(defun append  (x9 y9) (if x9 (cons (car x9) (append (cdr x9) y9)) y9))
 
(defun map (m%f m%x)
  (if m%x
   (cons (m%f (car m%x)) (map m%f (cdr m%x)))))

(defmacro backquote ZYKSX (blockq2 ZYKSX))

(defun blockq2
 (XYPY)
 (cond
  ((atom XYPY) XYPY)
  ((eq (car XYPY) ',)
   (list 'cons (cadr XYPY) (blockq2 (cddr XYPY))))
  ((eq (car XYPY) '@)
   (list 'append (cadr XYPY) (blockq2 (cddr XYPY))))
  ((equal (car XYPY) 'QUOTE)
   (list
    'cons
    (list 'list ''quote (cadr XYPY))
    (blockq2 (cddr XYPY))))
  ((atom (car XYPY))
   (list
    'cons
    (list 'quote (car XYPY))
    (blockq2 (cdr XYPY))))
  (t
   (list 'cons (blockq2 (car XYPY)) (blockq2 (cdr XYPY))))))

(defmacro let (vars . rest)
 (backquote
  (quote
   (lambda , (if (caar vars) (map car vars) vars) @ rest))
  @(if (caar vars) (map cadr vars))))
 
(defmacro for ((varb alku loppu steppi) . body)
 (if steppi () (setq steppi 1))
 (backquote
  let
  ((,varb ,alku))
  (repeat-times
   (/ (- (+ ,loppu , steppi) , alku) , steppi)
   @ body
   (setq , varb (plus , varb , steppi)))))

(defmacro push (x y) (backquote setq ,y (cons ,x ,y)))
(defmacro pop (x) (backquote prog1 (car ,x) (setq ,x (cdr ,x))))

(defun numberp (x) (equal (type x) (type 1)))

(defun listp (x) (equal (type x) (type '(1 2))))

)))""")

with open("bootpy.lsp","r") as f:
    c =f.read()
f.close
c="(progn "+c+"))))))"
lsp(c)

lsp("""
 (progn
   (defun repl () (while t (cr) (pprint (eval (read)))))
   (repl))""")

#secondary repl
repl()

    

