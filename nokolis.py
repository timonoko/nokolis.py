#! /usr/bin/python3

import math,time,os,sys
import resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

class oblist:
    func=[]
    args=[]
    jemma=[]
    _id_t="t"

def repl():
  oblist.func=[]
  oblist.args=[]
  oblist.jemma=[]
  try:
    while True:
        rivi=input("> ")
        if rivi[0]=="@":
            exec("oblist._id_Miumau="+rivi[1:])
            Nprint(oblist._id_Miumau)
        else:
            Nprint(Neval(parse(rivi)))
        print('')
  except Exception as ex:
    print("Error:",ex)
    print("TRACE=",oblist.func)
    print("(quit) 2 exit.")
    oblist._id_TRACE=(oblist.func)
    repl()
       
        
def oblist_name2(x):
    a=[c for c in x]
    d=""
    for c in a:
        if ord(c) in range(ord('a'), ord('z')): d=d+c
        elif ord(c) in range(ord('A'),ord('Z')): d=d+c
        elif ord(c) in range(ord('0'),ord('9')): d=d+c
        else: d=d+str(ord(c))
    return f'_id_{d}'

def oblist_name(x):
    return f'oblist.{oblist_name2(x)}'

def parse(program):
    a,b=readtokens(tokenize(program))
    return a

def tokenize(s):
    return s.replace('(',' ( ').replace(')',' ) ').replace("'"," ' ").replace(","," , ").replace('"',' " ').replace('[',' [ ').replace(']',' ] ').split()

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

def readarray(tokens):
    if tokens==[]: return [],[]
    eka,tokens2=readtokens(tokens)
    if car(eka)=='quote':
        eka=(cadr(eka)) 
    if eka==']':
        return [],tokens2
    elif eka==',':
        toka,tokens3=readarray(tokens2)
        return toka,tokens3
    else:
        toka,tokens3=readarray(tokens2)
        if toka==[] : return [eka],tokens3 
        else: return [eka]+toka,tokens3
            
def readtokens(tokens):
    if tokens==[]: return [],[]
    token = tokens.pop(0)
    if '(' == token:
        return readrest(tokens)
    elif ')' == token:
        return token,tokens
    elif '[' == token:
        return readarray(tokens)
    elif ']' == token:
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
    elif len(x)>2:
        print(x,end="")
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
        oblist.func.append(car(x))
        oblist.args.append(cdr(x))
        retu=Neval(Neval(car(x)))
        oblist.func.pop()
        return retu
    
def value_of(x):
   try:
       return eval(oblist_name(x))
   except:
       if identp(x): exec(f'{oblist_name(x)}=[]')
       return []

def Nset(x,y):   
    if identp(y):
       try:
           exec(f"{oblist_name(x)}='{y}'")
       except:
           exec(f'{oblist_name(x)}="{y}"')
    else:
      try:
          oblist.temp=y
          exec(f'{oblist_name(x)}=oblist.temp')
      except:
          try:
              setattr(oblist,oblist_name2(x),y)
          except:
              pass
    return y

def defq(x,y):
    try:
        exec(f'{oblist_name(x)}={y}')
    except:
        exec(f"{oblist_name(x)}='{y}'")
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
def numberp(x):
    return type(x)==type(1)
        
def save_vars(x):
    if atom(x):
        if identp(x):
            try: oblist.jemma.append(eval(oblist_name(x)))
            except: oblist.jemma.append([])
    else:
        save_vars(car(x))
        save_vars(cdr(x))
    
def restore_vars(x):
    if atom(x):
        if identp(x):
            exec(f'{oblist_name(x)}=oblist.jemma.pop()')
    else:
        restore_vars(cdr(x))
        restore_vars(car(x))

def assign_vars(x,y):
    if atom(x):
        Nset(x,y)
    else:
        assign_vars(car(x),car(y))
        assign_vars(cdr(x),cdr(y))

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
    save_vars(vars)
    assign_vars(vars,z)
    tulos=Nprogn(y)
    restore_vars(vars)
    return tulos

def Nmacroexpand(vars,args,y):
    z=args
    save_vars(vars)
    assign_vars(vars,z)
    tulos=Nprogn(y)
    restore_vars(vars)
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

def explode(x):
    if numberp(x):
       return explode(str(x))
    if identp(x):
       return array2list([ord(char) for char in x])
    elif atom(x): return []
    else:
      return cons(explode(car(x)),explode(cdr(x)))
 
     
def array2list(x):
  if x!=[]:
    if type(x[0])==type([1]):
        y=array2list(x[0])
    else:
        y=x[0]
    return [y,array2list(x[1:])]
  else:
    return []

def compress(x):
     if x==[]:
         return ""
     else:
         return chr(x[0])+compress(x[1])


def list2array(x):
    if atom(car(x)):
        y=car(x)
    else:
        y=list2array(car(x))
    if cdr(x)==[]:
         return [y]
    else:
         return [y]+list2array(cdr(x))

def arraynthset(x,y,z):
     y[x]=z
     return y


def nthcdr(x,y):
     if y==[]:
        return []
     elif x==0:
        return y
     else:
        return nthcdr(x-1,cdr(y))

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

readcc=_GetchUnix()
     
defq('plus', 'lambda x: Neval(car(x))+Neval(cadr(x))')
defq('difference','lambda x: Neval(car(x))-Neval(cadr(x))')
defq('times','lambda x: Neval(car(x))*Neval(cadr(x))')
defq('quotient','lambda x: Neval(car(x))/Neval(cadr(x))')
defq('remainder','lambda x: Neval(car(x))%Neval(cadr(x))')
defq('eqn','lambda x: Ntest(Neval(car(x))==Neval(cadr(x)))')
defq('eq','lambda x: Ntest(Neval(car(x)) is Neval(cadr(x)))')
defq('lessp','lambda x: Ntest(Neval(car(x))<Neval(cadr(x)))')
defq('greaterp','lambda x: Ntest(Neval(car(x))>Neval(cadr(x)))')
defq('atom','lambda x: Ntest(atom(Neval(car(x))))')
defq('not','lambda x: Nnot(Neval(car(x)))')
defq('print','lambda x: Nprint(Neval(car(x)))')
defq('quote','lambda x: car(x)')
defq('function','lambda x: car(x)')
defq('setq','lambda x: Nset(car(x),Neval(cadr(x)))')
defq('set','lambda x: Nset(Neval(car(x)),Neval(cadr(x)))')
defq('defq','lambda x: defq(car(x),cadr(x))')
defq('cons', 'lambda x: [Neval(car(x)),Neval(cadr(x))]')
defq('car', 'lambda x: car(Neval(car(x)))')
defq('cdr', 'lambda x: cdr(Neval(car(x)))')
defq('cddr', 'lambda x: cddr(Neval(car(x)))')
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
defq('oblist', 'lambda x: dir(oblist)')
defq('oblist-name-raw', 'lambda x: str(oblist_name2(Neval(car(x))))')
defq('explode', 'lambda x: explode(Neval(car(x)))')
defq('compress', 'lambda x: compress(Neval(car(x)))')
defq('read-str', 'lambda x: input("? ")')
defq('array2list', 'lambda x: array2list(Neval(car(x)))')
defq('list2array', 'lambda x: list2array(Neval(car(x)))')
defq('array2str',  'lambda x: "".join(str(Neval(car(x))))')
defq('python-eval', 'lambda x: eval(Neval(car(x)))')
defq('quit', 'lambda x: os._exit(1)')
defq('array-nth', 'lambda x: Neval(cadr(x))[Neval(car(x))]')
defq('array-nth-set', 'lambda x: arraynthset(Neval(car(x)),Neval(cadr(x)),Neval(caddr(x)))')
defq('array-append', 'lambda x: Neval(car(x))+Neval(cadr(x))')
defq('array-length', 'lambda x: len(Neval(car(x)))')
defq('nthcdr', 'lambda x: nthcdr(Neval(car(x)),Neval(cadr(x)))')
defq('int', 'lambda x: int(Neval(car(x)))')
defq('dir', 'lambda x: os.listdir()')
defq('printc', 'lambda x: print(chr(Neval(car(x))),end="")')
defq('readcc', 'lambda x: ord(readcc())')

lsp(""" (progn
 (defq defun (macro (x) (list 'defq (car x) (cons 'lambda (cdr x)))))
 (defq defmacro (macro (x) (list 'defq (car x) (cons 'mlambda (cdr x)))))
 (defq defmacrotest (macro (x) (list 'defq (car x) (cons 'nlambda (cdr x)))))
 (defq defnacro (macro (x) (list 'defq (car x) (cons 'macro (cdr x)))))
 (defq defnacrotest (macro (x) (list 'defq (car x) (cons 'macrotest (cdr x)))))) """)

lsp(""" (progn
 (defun cadr (x) (car (cdr x)))
 (defun cdddr (x) (cdr (cddr x)))
 (defun caddr (x) (car (cddr x)))
 (defun cadddr (x) (car (cdddr x)))
 (defun caar (x) (car (car x))) 

 (defun arith-macroes ((x y . z) ope)
         (if z 
           (list ope (list ope x y) (arith-macroes z ope))
           (if y (list ope x y) x)))
 (defnacro + (x) (arith-macroes x 'plus))
 (defnacro - (x) (arith-macroes x 'difference))
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
              (eqn x y) 
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


 (defun depthless (n x)
      (if (> 0 n) 0
        (if (atom x)
             (- n 1)
             (depthless (depthless n (car x)) (cdr x)))))
              
 (defun tab (x) (if (numberp x)
       (if (lessp 0 x) (progn (sp) (tab (- x 1)))))30)

 (defun pprint (x tabs)
           (or tabs (setq tabs 1))
           (if (< 1 (depthless 20 x))
              (print x)
              (progn (lb)
               (while x 
                (pprint (car x) (+ 1 tabs))
                (if (cdr x) (progn (cr) (tab tabs))) 
                (setq x (cdr x)))
              (rb))))

(defun nth (x y) (if (arrayp y) (array-nth x y) (car (nthcdr x y))))


 (defun cond-jatko (((xZ . yZ) . zZ))
           (list 'if xZ (cons 'progn yZ) (if zZ (cond-jatko zZ))))

 (defnacro cond (xZ) (cond-jatko xZ)))

)))""")

lsp(""" (progn 

(print 'hello)
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
  (function
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

(defun array x (array2list x))

(defun arrayp (x) (> (array-length x) 2))

(defun length (x) 
    (if x 
      (if (arrayp x) (array-length x) (plus 1 (length(cdr x))))
       0))

(defmacro nth-set (x y z)
   (backquote progn
         (if (arrayp ,y) 
                 (array-nth-set ,x ,y ,z)
                 (rplaca (nthcdr ,x ,y) ,z))
    ,y))

(defun add1 (x) (plus 1 x))
(defun sub1 (x) (difference x 1))

(setq null not)

(defun numberp(x) (equal (type x) (type 1)))

(defun getchar (x n) (nth (difference n 1) (explode x)))

(defmacro when (x . y) (backquote if ,x (progn @ y)))

(defun macroexpand   (x9 hantaa-vaan)
   (cond
    ((atom x9) x9)
    ((equal (car x9) 'quote) x9)
    ((equal (car x9) 'lambda)
     (cons (car x9) (cons (cadr x9) (macroexpand (cddr x9)))))
    ((and
      (equal (car x9) 'if)
      (member (car (cadr x9)) '(null not)))
     (macroexpand (list 'if (cadr (cadr x9)) (cadddr x9) (caddr x9))))
    ((and
      (not hantaa-vaan)
      (identp (car x9))
      (member (car (eval (car x9))) '(macro mlambda)))
     (macroexpand
      (eval
       (cons
        (list
         'function
         (cons
          (if
           (equal (car (eval (car x9))) 'mlambda)
           'nlambda
           'macrotest)
          (cdr (eval (car x9)))))
        (cdr x9)))))
    (t (cons (macroexpand (car x9)) (macroexpand (cdr x9) t))))))


)))""")

lsp("(defun sort (x) (array2list (arraysort (list2array x))))")
defq('arraysort', 'lambda x: arraysort(Neval(car(x)))')
def arraysort(x): x.sort(); return x


def print_to_file(x,y,pretty):
    original_stdout = sys.stdout
    with open(x, 'w') as f:
        sys.stdout = f
        print("")
        if pretty==[]:
            Nprint(y)
        else:
            oblist._id_temp=y
            lsp("(pprint temp")
        print("")
        f.close()
        sys.stdout = original_stdout

defq('print-to-file', 'lambda x: print_to_file(Neval(car(x)),Neval(cadr(x)),Neval(caddr(x)))')

def loadlisp(name):
    with open(name,"r") as f:
       c =f.read()
    f.close
    lsp("(progn "+c+"))))))")
    return name
    
defq('load', 'lambda x: loadlisp(Neval(car(x)))')

loadlisp("bootpy.lsp")
loadlisp("cursor.lsp")

lsp("(defun repl () (while t (cr) (pprint (eval (read)))))")

#secondary repl
repl()

    

