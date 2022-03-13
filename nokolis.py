#! /usr/bin/python3

import math,time,os,sys,re
from math import *

import resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**5)

t="t"
T="T"
nil=[]
NIL=[]

class oblist:
    func=[]
    args=[]
    enviro=[]
    names=[]
    Named_Already={}
    _id_True=True
    _id_False=[]
    _id_t="t"
    _id_T="T"
    _id_nil=[]
    _id_NIL=[]
    _id_HISTORY=[]
    

def repl(n=0):
  quit=False
  while not quit:
    try:
        oblist.func=[]
        oblist.args=[]
        if n==[]:n=0
        for x in range(0,n): print('',end='>')
        rivi=Nread()
        if rivi=="":
            pass
        elif rivi=="quit":
            quit=True
        else:
            pprint(Neval(rivi),1,True)
        print('')
        oblist._id_HISTORY.append(rivi)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as ex:
        if oblist.func==[]:
            quit=True
        else:
            print("Error:",ex)
            print("Stack=",end=""),
            Nprint(array2list(oblist.func))
            print(""),
            oblist._id_TRACE=oblist.func
            repl(n+1)
            try:
                oblist.enviro=unwind_enviro(oblist.enviro,len(oblist.enviro))
            except:
                oblist.enviro=[]
  print("")
  if n==0: save_all()
     
     
import readline
readline.parse_and_bind("tab: complete")
string = readline.get_completer_delims().replace('-', '')
readline.set_completer_delims(string)

    
def add_oblist(x):
    if identp(x) and not x in oblist.names:
        oblist.names.append(x)
        def complete(text,state):
            volcab = oblist.names
            results = [x for x in volcab if x.startswith(text)] + [None]
            return results[state]
        readline.set_completer(complete)

def oblist_name2(x):
  try:
    return oblist.Named_Already[x]
  except:
    a=[c for c in x]
    d="_id_"
    for c in a:
        if ord(c) in range(ord('a'),1+ord('z')): d=d+c
        elif ord(c) in range(ord('A'),1+ord('Z')): d=d+c
        elif ord(c) in range(ord('0'),1+ord('9')): d=d+c
        else: d=d+"_"+str(ord(c))+"_"
    oblist.Named_Already[x]=d
    return d

def oblist_name(x):
    return f'oblist.{oblist_name2(x)}'

def parse(program):
    a,b=readtokens(tokenize(program))
    return a

def tokenize(s):
    return s.replace('(',' ( ').replace(')',' ) ').replace("'"," ' ").replace(","," , ").replace('"',' " ').replace('[',' [ ').replace(']',' ] ').split()

MORE=False

        
def readrest(tokens):
#    if tokens==[]: return [],[]
    if tokens==[]:
        if MORE:
            return readrest(tokenize(input(" ..")))
        else:
            return [],[]
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
    if tokens==[]:
        if MORE:
            return readarray(tokenize(input(" ..")))
        else:
            return [],[]
    eka,tokens2=readtokens(tokens,True)
    if eka==']':
        return [],tokens2
    elif eka == ',':
        toka,tokens3=readarray(tokens2)
        return toka,tokens3
    else:
        toka,tokens3=readarray(tokens2)
        if toka==[] : return [eka],tokens3 
        else: return [eka]+toka,tokens3
            
def readtokens(tokens,at_array=False):
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
      if at_array:
        yksi,tokens2=readtokens(tokens,True)
        return yksi,tokens2
      else:  
        yksi,tokens2=readtokens(tokens)
        return ["quote",[yksi]],tokens2
    else:
        return atomi(token),tokens

def atomi(token):
    try:
        if float(token)==int(token):
            return int(token)
        else:
            return float(token)
    except:
            add_oblist(token)
            return token

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

def cdddr(x):
    return cdr(cddr(x))

def cddddr(x):
    return cdr(cdddr(x))

def caddr(x):
    return car(cddr(x))

def cadddr(x):
    return car(cdddr(x))

def caddddr(x):
    return car(cddddr(x))

def caar(x):
    return car(car(x))

def atom(x):
    if x==[]: return True
    return type(x) != type([1])

def Nprintrest(x,strings):
    if x==[] :
        print(")",end='')
    elif atom(x):
        print(" . ",x,")",end='')
    else:
        Nprint(car(x),strings)
        if cdr(x)!=[]: print(" ",end='')
        Nprintrest(cdr(x),strings)
        
def Nprint(x,strings=False):
    if atom(x):
        if x==[]:
            print('()',end='')
        else:
            print(x,end='')
    elif len(x)>2:
        print(x,end="")
    elif car(x)=='quote':
        print("'",end='')
        Nprint(car(cdr(x)),strings)
    elif strings and flat(x) and numberp(car(x)) and car(x)==34:
        print(compress(x),end='"') 
    else:
        print("(",end='')
        Nprintrest(x,strings)
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
        eka=Neval(car(x))
        if eka==[]: print(f'Error: {car(x)} == [] ')
        retu=Neval(eka)
        try: oblist.func.pop()
        except: pass
        return retu
    
def value_of(x):
   try:
       return eval(oblist_name(x))
   except:
       if identp(x): exec(f'{oblist_name(x)}=[]')
       return []

   
def Nset(x,y):
    if x==[]:
        return y
    if not identp(x) or x in ['nil',"NIL",'t','T','True','False']:
        print("CANT ASSIGN:",x,"=",y)
        return(y)
    x2=oblist_name(x)
    if identp(y):
       try:
           exec(f"{x2}='{y}'")
       except:
           exec(f'{x2}="{y}"')
    else:
      try:
          oblist.temp=y
          exec(f'{x2}=oblist.temp')
      except:
          try:
              setattr(oblist,oblist_name2(x),y)
          except:
              print("CANT ASSIGN:",x,"=",y)
    return y

def defq(x,y):
    add_oblist(x)    
    try:
        exec(f'{oblist_name(x)}={y}')
    except:
        exec(f"{oblist_name(x)}='{y}'")
    return x

def lsp(x):
    return Neval(parse(x))

def cons(x,y=[]):
    return [x,y]

def Nlist(x):
    if atom(x): return x
    else:
        return cons(Neval(car(x)),Nlist(cdr(x)))

def identp(x):
    return type(x)==type("abba")
def numberp(x):
    return (type(x)==type(1))or(type(x)==type(1.1))
        
def save_vars(x):
    if atom(x):
        if identp(x):
            y=oblist_name(x)
            try: oblist.enviro.append([x,eval(y)])
            except: oblist.enviro.append([x,[]])
    else:
        save_vars(car(x))
        save_vars(cdr(x))
    
def restore_vars(x):
    if atom(x):
        if identp(x):
            Nset(x,oblist.enviro.pop()[1])
    else:
        restore_vars(cdr(x))
        restore_vars(car(x))

def unwind_enviro(alku,maara):
    for x in range(0,maara):
        yksi=alku.pop()
        Nset(yksi[0],yksi[1])
    return alku

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
    tulos=catch('return',cons('progn',y))
    restore_vars(vars)
    return tulos

def Nexpand(vars,args,y):
    z=args
    save_vars(vars)
    assign_vars(vars,z)
    tulos=Nprogn(y)
    restore_vars(vars)
    return tulos

def Nmacro(vars,args,y):
    return Neval(Nexpand(vars,args,y))

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

def rplaca(x,y):
    x[0]=y
    return x

def rplacd(x2,y2):
    x2[1]=y2
    return x2

def last(x):
    if cdr(x)==[]:
        return x
    else:
        return last(cdr(x))

def nconc(x,y):
    if len(x)==2:
        rplacd(last(x),y)
        return x
    else:
        return y
    
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
        if identp(x[0]):
          add_oblist(x[0])
    return [y,array2list(x[1:])]
  else:
    return []

def tuple2list(x):
    return array2list(list(x))
def list2tuple(x):
    return tuple(list2array(x))

def compr2(x):
     if x==[]:
         return ""
     elif numberp(car(x)):
         return chr(x[0])+compr2(x[1])
     elif atom(car(x)):
         return str(car(x))+compr2(x[1])
     else:
         y=compr2(x[0])+compr2(x[1])
         return y

def compress(x):
    y=compr2(x)
    add_oblist(y)
    return y
     
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

def printc(x):
    print(chr(x),end="")

def a1(x):return Neval(car(x))
def a2(x):return Neval(cadr(x))
def a3(x):return Neval(caddr(x))
def a4(x):return Neval(cadddr(x))
def a5(x):return Neval(caddddr(x))
def a6(x):return Neval(car(cdr(cddddr(x))))
def a7(x):return Neval(car(cddr(cddddr(x))))
defq('plus', 'lambda x: a1(x)+a2(x)')
defq('difference','lambda x: a1(x)-a2(x)')
defq('times','lambda x: a1(x)*a2(x)')
defq('quotient','lambda x: a1(x)/a2(x)')
defq('remainder','lambda x: a1(x)%a2(x)')
defq('eqn','lambda x: Ntest(a1(x)==a2(x))')
defq('eq','lambda x: Ntest(a1(x) is a2(x))')
defq('lessp','lambda x: Ntest(a1(x)<a2(x))')
defq('greaterp','lambda x: Ntest(a1(x)>a2(x))')
defq('atom','lambda x: Ntest(atom(a1(x)))')
defq('not','lambda x: Nnot(a1(x))')
defq('print','lambda x: Nprint(a1(x),a2(x))')
defq('quote','lambda x: car(x)')
defq('function','lambda x: car(x)')
defq('setq','lambda x: Nset(car(x),a2(x))')
defq('set','lambda x: Nset(a1(x),a2(x))')
defq('defq','lambda x: defq(car(x),cadr(x))')
defq('cons', 'lambda x: [a1(x),a2(x)]')
defq('car', 'lambda x: car(a1(x))')
defq('cdr', 'lambda x: cdr(a1(x))')
defq('cddr', 'lambda x: cddr(a1(x))')
defq('list', 'lambda x: Nlist(x)')
defq('lambda', 'lambda x: Nlambda(car(x),oblist.args[-1],cdr(x))')
defq('progn', 'lambda x: Nprogn(x)')
defq('prog1', 'lambda x: Nprog1(x)')
defq('macro', 'lambda x: Nmacro(car(car(x)),oblist.args[-1],cdr(x))')
defq('mlambda', 'lambda x: Nmacro(car(x),oblist.args[-1],cdr(x))')
defq('macrotest', 'lambda x: Nexpand(car(car(x)),oblist.args[-1],cdr(x))')
defq('nlambda', 'lambda x: Nexpand(car(x),oblist.args[-1],cdr(x))')
defq('if', 'lambda x: Nif(car(x),cadr(x),caddr(x))')
defq('and', 'lambda x: Nand(x)')
defq('or', 'lambda x: Nor(x)')
defq('cr', 'lambda x: print("")')
defq('sp', 'lambda x: print(" ",end="")')
defq('lb', 'lambda x: print("(",end="")')
defq('rb', 'lambda x: print(")",end="")')
defq('while', 'lambda x: Nwhile(car(x),cdr(x))')
defq('eval', 'lambda x: Neval(a1(x))')
defq('repeat-times', 'lambda x: Nrepeat_times(a1(x),cdr(x))')
defq('rplaca', 'lambda x: rplaca(a1(x),a2(x))')
defq('rplacd', 'lambda x: rplacd(a1(x),a2(x))')
defq('last', 'lambda x: last(a1(x))')
defq('nconc', 'lambda x: nconc(a1(x),a2(x))')
defq('identp', 'lambda x: Ntest(identp(a1(x)))')
defq('type', 'lambda x: str(type(a1(x)))')
defq('str-raw', 'lambda x: str(a1(x))')
defq('oblist', 'lambda x: array2list(oblist.names)')
defq('oblist-name-raw', 'lambda x: str(oblist_name2(a1(x)))')
defq('explode', 'lambda x: explode(a1(x))')
defq('compress', 'lambda x: compress(a1(x))')
defq('array2list', 'lambda x: array2list(a1(x))')
defq('list2array', 'lambda x: list2array(a1(x))')
defq('python-eval', 'lambda x: eval(a1(x))')
defq('python-exec', 'lambda x: exec(a1(x),globals())')
defq('quit', 'lambda x: os._exit(1)')
defq('array-nth', 'lambda x: a2(x)[a1(x)]')
defq('array-nth-set', 'lambda x: arraynthset(a1(x),a2(x),a3(x))')
defq('array-append', 'lambda x: a1(x)+a2(x)')
defq('array-length', 'lambda x: len(a1(x))')
defq('nthcdr', 'lambda x: nthcdr(a1(x),a2(x))')
defq('int', 'lambda x: int(a1(x))')
defq('printc', 'lambda x: print(chr(a1(x)),end="")')
defq('readcc', 'lambda x: ord(readcc())')
defq('read-str', 'lambda x: input("? ")')
defq('read-from-str', 'lambda x: parse(a1(x))')
defq('return', 'lambda x: throw("return",a1(x))')
defq('readc', 'lambda x: readc() ')
defq('read', 'lambda x: Nread()')
defq('readline', 'lambda x: parse(input("> "))')
defq('file2str', 'lambda x: file2str(a1(x))')

def file2str(x):
    from pathlib import Path
    return Path(x).read_text()

def Nread():
     global MORE
     MORE=True
     tulos=parse(input("> "))
     MORE=False
     return tulos

def readc():
    try: return ord(sys.stdin.read(1))
    except: return -1
 
def null(x): return x==[]

defq('throw', 'lambda x: throw(a1(x),a2(x))')
def throw(name,data):
      raise Exception(name,data)

defq('catch', 'lambda x: catch(a1(x),cadr(x))' )
def catch(name,data):
    enviro=len(oblist.enviro)
    try:
       return Neval(data) 
    except Exception as inst:
        oblist.enviro=unwind_enviro(oblist.enviro,len(oblist.enviro)-enviro)
        try:
            name2,data2 = inst.args
        except:
            name2,data2 = ('?',inst)
        if name==name2:
            return data2
        else:
            throw(name2,data2)

            

lsp(""" (progn
 (defq defun (macro (x) (list 'defq (car x) (cons 'lambda (cdr x)))))
 (defq defmacro (macro (x) (list 'defq (car x) (cons 'mlambda (cdr x)))))
 (defq defmacrotest (macro (x) (list 'defq (car x) (cons 'nlambda (cdr x)))))
 (defq defnacro (macro (x) (list 'defq (car x) (cons 'macro (cdr x)))))
 (defq defnacrotest (macro (x) (list 'defq (car x) (cons 'macrotest (cdr x)))))) """)

lsp(""" (progn
 (defun cadr (x) (car (cdr x)))
 (defun cdddr (x) (cdr (cddr x)))
 (defun cddddr (x) (cdr (cdddr x)))
 (defun caddr (x) (car (cddr x)))
 (defun cadddr (x) (car (cdddr x)))
 (defun caddddr (x) (car (cddddr x)))
 (defun caar (x) (car (car x))) 


 (defq
  amacro
  (lambda
   (x ope)
   (if
    (cdr x)
    (list ope (car x)
        (amacro (cdr x)
          (case ope (difference 'plus) (quotient 'times) (t ope))))
    (car x))))

 (defnacro + (x) (amacro x 'plus))
 (defnacro * (x) (amacro x 'times))
 (defnacro / (x) (amacro x 'quotient))
 (defnacro - (x) (amacro x 'difference))
 (defnacro % (x) (amacro x 'remainder))


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

 (defq
  delete
  (lambda
   (x lista)
   (if
    lista
    (if
     (equal x (car lista))
     (delete x (cdr lista))
     (cons (car lista) (delete x (cdr lista)))))))

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
           (list 'if xZ (if (cdr yZ) (cons 'progn yZ) (car yZ)) (if zZ (cond-jatko zZ))))

(defnacro cond (xZ) (cond-jatko xZ))

(defun condf-jatko (((xZ . yZ) . zZ))
           (list 'iff xZ (if (cdr yZ) (cons 'progn yZ) (car yZ)) (if zZ (condf-jatko zZ))))

(defmacro condf xZ (condf-jatko xZ)))

)))""")

def iff(x=[],y=[],z=[]):
    if x==[]: return z
    if x : return y
    else: return z
defq('iff','lambda x: iff(a1(x),a2(x),a3(x))')
    
lsp(""" (progn 

(defun append  (x9 y9) (if x9 (cons (car x9) (append (cdr x9) y9)) y9))
 
(defun map (m%f m%x)
  (if m%x
   (cons (m%f (car m%x)) (map m%f (cdr m%x)))))

(defun mapc (m%f m%x)
  (if m%x
   (progn (m%f (car m%x)) (map m%f (cdr m%x)) t)))

 (defq
  filter
  (lambda
   (f%m x%m)
   (if
    x%m
    (if
     (f%m (car x%m))
     (cons (car x%m) (filter f%m (cdr x%m)))
     (filter f%m (cdr x%m))))))

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
(defmacro setqpop (x y) (backquote progn (setq ,x (car ,y)) (setq ,y (cdr ,y))))


(defun numberp (x) (equal (type x) (type 1)))

(defun listp (x) (equal (type x) (type '(1 2))))

(defun array x (array2list x))

(defun arrayp (x) (> (array-length x) 2))

(defun length (x) 
    (if x 
      (plus 1 (length(cdr x)))
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

(defun numberp(x) (or (equal (type x) (type 1))
                      (equal (type x) (type 1.1))))

(defun getchar (x n) (nth (difference n 1) (explode x)))

(defmacro when (x . y) (backquote if ,x (progn @ y)))

(defq unless
  (mlambda
   (x . y)
   (list
    'if
    (list 'not x)
    (cons 'progn y))))


(defun macroexpand-old   (x9 hantaa-vaan)
   (cond
    ((atom x9) x9)
    ((equal (car x9) 'quote) x9)
    ((equal (car x9) 'lambda)
     (cons (car x9) (cons (cadr x9) (macroexpand (cddr x9)))))
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
    (t (cons (macroexpand (car x9)) (macroexpand (cdr x9) t)))))

(defun subst (old new tree)
 (cond
  ((null tree) tree)
  ((equal old tree) new)
  ((atom tree) tree)
  (t
   (cons
    (subst old new (car tree))
    (subst old new (cdr tree))))))

 (defmacro case (x  .  y )
       (cons
        'cond
        (map
         (function
          (lambda
           (y)
           (cond
            ((equal (car y) 't) y)
            ((atom (car y))
             (backquote (equal , x QUOTE (car y)) @ (cdr y)))
            (t (backquote (member , x QUOTE (car y)) @ (cdr y))))))
         y)))

(defmacro casef (x  .  y )
       (cons
        'condf
        (map
         (function
          (lambda
           (y)
           (cond
            ((equal (car y) 't) y)
            ((atom (car y))
             (backquote (equal , x QUOTE (car y)) @ (cdr y)))
            (t (backquote (member , x QUOTE (car y)) @ (cdr y))))))
         y)))

 (defq foreach
  (mlambda
   (x . y)
   (backquote mapc (function (lambda (, (car x)) @ y)) , (cadr x))))


)))""")

lsp("(defun sort (x) (array2list (arraysort (list2array x))))")
defq('arraysort', 'lambda x: arraysort(a1(x))')
def arraysort(x): x.sort(); return x

defq('cadr', 'lambda x: cadr(a1(x))')
defq('cdddr', 'lambda x: cdddr(a1(x))')
defq('cddddr', 'lambda x: cddddr(a1(x))')
defq('caddr', 'lambda x: caddr(a1(x))')
defq('cadddr', 'lambda x: cadddr(a1(x))')
defq('caddddr', 'lambda x: caddddr(a1(x))')
defq('caar', 'lambda x: caar(a1(x))')

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
defq('print-to-file', 'lambda x: print_to_file(a1(x),a2(x),a3(x))')

def with_out_file(x,y):
    original_stdout = sys.stdout
    with open(x, 'w') as f:
        sys.stdout = f
        try: tulos=Nprogn(y)
        except: tulos="Some error in with_out_file"
        print("")
        f.close()
    sys.stdout = original_stdout
    return tulos
defq('with-out-file', 'lambda x: with_out_file(a1(x),cdr(x))')

def with_in_file(x,y):
    original_stdin = sys.stdin
    with open(x, 'r') as f:
        sys.stdin = f
        try: tulos=Nprogn(y)
        except: tulos= "Some error in with_in_file"
        f.close()
    sys.stdin = original_stdin
    return tulos
defq('with-in-file', 'lambda x: with_in_file(a1(x),cdr(x))')

def hii(lis):
    if lis!=[]:
        x=car(lis)
        if car(x)=="defq":
            Nset(cadr(x),caddr(x))
        hii(cdr(lis))

def loadlisp(name):
    if ".npy" in name: 
        hii(read_npy(name))
        return name
    with open(name,"r") as f:
        c =f.read()
    f.close
    Neval(parse(c+")))"))
    return name

array2list(os.listdir())    
defq('load', 'lambda x: loadlisp(a1(x))')

def write_npy(na,ar):
    from numpy import save,array
    nar=array(ar,dtype=object)
    return save(na,nar)
defq('write-npy','lambda x: write_npy(a1(x),a2(x))')

def read_npy(na):
    from numpy import load
    return load(na,allow_pickle=True).tolist()
defq('read-npy','lambda x: read_npy(a1(x))')

lsp("""(progn
 (defq
  save-formula
  (lambda
   (module)
   (cons
    (quote progn)
    (cons
     (list 'defq 'MODULE module)
     (let
      ((__tulo_s nil)
       (__modu_le (eval module))
       (__myfu
        (function
         (lambda
          (x%x)
          (uncompile x%x)
          (if
           (or
            (equal (type (eval x%x)) (type car))
            (equal (type (eval x%x)) (type plus))
            (member x%x '(m%f m%x module x%x True False T NIL nil t __myfu __modu_le)))
           x%x
           (list 'defq x%x (eval x%x)))))))
      (while __modu_le (push (__myfu (pop __modu_le)) __tulo_s))
      __tulo_s)))))
 (defq
  save
  (lambda
   (m)
   (if (null m) (setq m MODULE))
   (print-to-file
    (compress (append (explode m) '(46 76 83 80)))
    (save-formula m)
    'pretty)
   (list m 'saved)))
 (defq
  save-module-npy
  (lambda
   (m)
   (if (null m) (setq m MODULE))
   (write-npy
    m
    (save-formula m))
   (list m 'npy))))""")

oblist.gensym=0
def gensym():
    oblist.gensym=oblist.gensym+1
    return "gensym"+str(oblist.gensym)
defq('gensym','lambda x: gensym()')


def equal(x,y):
    return ((x is y) or ((x == y) or (car(x) and (car(y) and (equal(car(x),car(y)) and equal(cdr(x),cdr(y)))))))
defq('equal', 'lambda x:  Ntest(equal(a1(x),a2(x)))')

def depthless(n,x):
    if (0 > n):
        return 0
    else:
        if atom(x):
            return (n - 1)
        else:
            return depthless(depthless(n,car(x)),cdr(x))
defq('depthless2','lambda x: Ntest(depthless(a1(x),a2(x)))')

def tab(x):
    if (0 < x):
            print(" ",end="")
            tab((x - 1))
    return 30

def flat(x):
    if x:
        if atom(car(x)):
            return flat(cdr(x))
        else:
            return False
    else:
        return True
defq('flat','lambda x: Ntest(flat(a1(x)))')
    
def pprint(x,tabs=1,strings=False):
    if not numberp(tabs): tabs=1
    if atom(x):
        Nprint(x)
    elif len(x) > 2:
        print("[",end="")
        n=10
        i=0
        while i<len(x):
            pprint(x[i],1+tabs,strings)
            i=i+1
            if i < len(x):
                if n>0:
                    print(", ",end="")
                    n=n-1
                else:
                    print(",")
                    tab(tabs)
                    n=10
        print("]",end="")
    elif atom(cdr(x)):
        Nprint(x)
    elif flat(x):
      if strings and numberp(car(x)) and car(x)==34:
        print(compress(x),end='"') 
      else:    
        print("(",end="")
        n=10
        while x!=[]:
            Nprint(car(x))
            x=cdr(x)
            if x!=[]:
               if n>0:
                   print(" ",end="")
                   n=n-1
               else:
                   print("")
                   tab(tabs)
                   n=10
        print(")",end="")
    elif (1 < depthless(20,x)):
        Nprint(x,strings)
    else:
        print("(",end="")
        while x:
            pprint(car(x), 1+tabs,strings)
            if cdr(x):
                print("")
                tab(tabs)
            x=cdr(x)
        print(")",end="")
defq('pprint', 'lambda x: pprint(a1(x),a2(x),a3(x))')

defq('member','lambda x:member(a1(x),a2(x))')
def member(x,y):
    if y == []:
        return []
    else:
        if equal(x,car(y)):
            return y
        else:
            return member(x,cdr(y))

def macroexpand(x9,hv=()):
    if atom(x9):
        return x9
    elif equal(car(x9),"quote"):
        return x9
    elif equal(car(x9),"lambda"):
        return cons(car(x9),cons(cadr(x9),macroexpand(cddr(x9))))
    elif (not(hv) and (identp(car(x9)) and member(car(Neval(car(x9))),['macro', ['mlambda', []]]))):
        if equal(car(Neval(car(x9))),"mlambda"):
            iik="nlambda"
        else:
            iik="macrotest"
        return macroexpand(Neval(cons(cons("function",cons(cons(iik,cdr(Neval(car(x9)))),[])),cdr(x9))))
    elif True:
        return cons(macroexpand(car(x9)),macroexpand(cdr(x9),t))
defq('macroexpand','lambda x: macroexpand(a1(x),a2(x))')


defq('subst','lambda x: subst(a1(x),a2(x),a3(x))')                    
def subst(old,new,tree):
    if tree:
        if equal(old,tree):
            return new
        else:
            if atom(tree):
                return tree
            else:
                
                return cons(subst(old,new,car(tree)),subst(old,new,cdr(tree)))
    else:
        return tree

defq('copy','lambda x: copy(a1(x))')
def copy(x):
    if atom(x):
        return x
    else:
        return cons(copy(car(x)),copy(cdr(x)))

# (mappy explode '(a b)) == (map explode '(a b)) 
def mappy(f,x):
    if x==[]: return []
    else: return cons(f(car(x)),mappy(f,cdr(x)))
defq('mappy','lambda x: mappy(eval(car(x)),a2(x))')  

def mapcpy(f,x):
    if x==[]: pass
    else:
        f(car(x))
        mapcpy(f,cdr(x))
defq('mapcpy','lambda x: mapcpy(eval(car(x)),a2(x))')  

def filterpy(f,x):
    if x==[]: return []
    elif f(car(x)):
        return cons(car(x),filterpy(f,cdr(x)))
    else:
        return filterpy(f,cdr(x))
defq('filterpy','lambda x: filterpy(eval(car(x)),a2(x))')  

def apppy(f,x):return f(x)
defq('apppy','lambda x: apppy(eval(car(x)),a2(x))')  
lsp("(defmacro apply (f x) (cons f x))")

defq('blockq3','lambda x: blockq2(a1(x))')
def blockq2(XYPY):
    if atom(XYPY):
        return XYPY
    elif (car(XYPY) == ","):
        return cons("cons",cons(cadr(XYPY),cons(blockq2(cddr(XYPY)),[])))
    elif (car(XYPY) == "@"):
        return cons("append",cons(cadr(XYPY),cons(blockq2(cddr(XYPY)),[])))
    elif equal(car(XYPY),"QUOTE"):
        return cons("cons",cons(cons("list",cons(['quote', ['quote', []]],cons(cadr(XYPY),[]))),cons(blockq2(cddr(XYPY)),[])))
    elif atom(car(XYPY)):
        return cons("cons",cons(cons("quote",cons(car(XYPY),[])),cons(blockq2(cdr(XYPY)),[])))
    elif True:
        return cons("cons",cons(blockq2(car(XYPY)),cons(blockq2(cdr(XYPY)),[])))
lsp("(defmacro backquote ZYKSX (blockq3 ZYKSX))")

def reverse(x):
    if cdr(x):
        return nconc(reverse(cdr(x)),cons(car(x),[]))
    else:
        return cons(car(x),[])
defq('reverse','lambda x: reverse(a1(x))')

def nreverse(lst=[]):
    if lst[1]:
        return nconc(nreverse(lst[1]),rplacd(lst,nil))
    else:
        return lst
defq('nreverse','lambda x: nreverse(a1(x))')

def append(x9,y9):
    if x9:
        return cons(car(x9),append(cdr(x9),y9))
    else:
        return y9
defq('append','lambda x: append(a1(x),a2(x))')

def error_trap(x):
    try:
        return Nprogn(x)
    except Exception as ex:
        try:
            name,data=ex.args
        except:
            name,data=('?',ex)
        if "return"==name :
            raise Exception("return",data)
        else:
            print("Error: ",ex)
            return []
defq('error-trap','lambda x: error_trap(x)')    

lsp("""
(progn
 (defq
  uncompile
  (lambda
   (x y)
   (when
    (setq y (assoc x _COMPILED_))
    (setq _COMPILED_ (delete y _COMPILED_))
    (set x (cdr y))
    (list x 'uncompiled))))
 (defq
  compile
  (lambda
   (x)
   (if
    (assoc x _COMPILED_)
    ()
    (progn
     (push (cons x (eval x)) _COMPILED_)
     (set x (macroexpand (eval x)))
     (list x 'compiled)))))
 (defq
  mapp
  (lambda
   (m%f m%x)
   (if m%x (cons (m%f (car m%x)) (mapp m%f (cdr m%x))))))))
""")

lsp("(defq pristr (nlambda (x) (print (compress (cdr x)))))")

def re_search(x,y):
    import re
    tulos=[]
    for l in y:
        if re.search(x,l):
            tulos.append(l)
    return tulos
defq('search-array','lambda x: re_search(a1(x),a2(x))')
lsp("(defun search (x y) (array2list (search-array x (list2array y))))")
defq('listdir', 'lambda x: os.listdir(a1(x))')
lsp("(defun dir (x y) (if (null y) (setq y '.)) (array2list(if x (search-array x (listdir y)) (listdir y))))")
lsp("(defun continue () (cd '/tmp/) (load (car (reverse (sort (dir '^OBLIST))))) (cd CWD))")
defq('os-remove','lambda x: os.remove(a1(x))')
lsp("(defun del-file (x) (mapc os-remove (dir x)) (dir))") 
lsp("(defun perkele () (setq CWD (cd)) (cd '/tmp/) (del-file '^OBLIST) (cd CWD))")
defq('ls','lambda x: array2list(os.popen("ls "+a1(x)).read().split())')

defq("loadimage", 'lambda x: loadimage(a1(x))')
defq("saveimage", 'lambda x: saveimage(a1(x),a2(x))')
defq("showimage", 'lambda x: showimage(a1(x))')
defq("putpixel", 'lambda x: putpixel(a1(x),a2(x),a3(x),a4(x))')
defq("getpixel", 'lambda x: getpixel(a1(x),a2(x),a3(x))')
defq("imagesize", 'lambda x: imagesize(a1(x))')
defq("newimage", 'lambda x: newimage(a1(x),a2(x),a3(x),a4(x))')
defq("killdisplay", 'lambda x: killdisplay()')
defq("imagetext",'lambda x: imagetext(a1(x),a2(x),a3(x),a4(x))')
defq("imagedraw",'lambda x: imagedraw(a1(x),a2(x),a3(x),a4(x))')

lsp("""
 (defun image-example ()
   (setq im (newimage 100 50 RED))
   (imagebox im '(3 3) '(93 43) WHITE)
   (imagetext im '(10 10) FONTTI 'HELLO)
   (showimage im)
   (sleep 1)
   (killdisplay))) """)


from PIL import Image,ImageDraw,ImageFont

def imagedraw (im,s,e,c):
    line=(car(s),cadr(s),car(e),cadr(e))
    color=list2tuple(c)
    draw = ImageDraw.Draw(im)
    draw.line(line,color)
    return im

FreeFonts="/usr/share/fonts/truetype/freefont/"
defq('FONTS',array2list(os.listdir(FreeFonts)))

def imagetext(im,p,fsc,text):
    pos=(car(p),cadr(p))
    fnt=car(fsc)
    size=cadr(fsc)
    v=caddr(fsc)
    color=list2tuple(v)
    fnt = ImageFont.truetype(FreeFonts+fnt,size)
    d = ImageDraw.Draw(im)
    d.text(pos, str(text), font=fnt, fill=color)
    return im
    
def showimage(im):
     im.show()

def loadimage(x):
    im=Image.open(x)
    return im

def saveimage(im,f):
    im.save(f)
    return f

def getpixel(im,x,y):
    return tuple2list(im.getpixel((x,y)))
                    
def putpixel(im,x,y,v):
    im.putpixel((x,y),list2tuple(v))
    return v

def imagesize(im):
    return tuple2list(im.size)
    
def newimage(x,y,v,typ=[]):
    if typ==[]: typ="RGB"
    return Image.new(typ,(x,y),list2tuple(v))

def killdisplay():
    os.system("killall display")

lsp(""" (defun global-colors()
        (global RED '(255 0 0))
        (global GREEN '( 0 255 0))
        (global BLUE '( 0 0 255))
        (global YELLOW '(255 255 0))
        (global BLACK '( 0 0 0))
        (global WHITE '( 255 255 255))
        (global FONTTI '(FreeSansBold.ttf 20 (0 0 0))))) """)

def imagepaste(im=[],p=[],uusi=[],color=[255,[255,[255,[]]]]):
    s=imagesize(uusi)
    for x in range(0,(1 + (s[0] - 1))):
        for y in range(0,(1 + (s[1][0] - 1))):
            pix=getpixel(uusi,x,y)
            if not equal(pix,color):
                putpixel(im,(p[0] + x),(p[1][0] + y),pix)
defq('imagepaste','lambda x: imagepaste(a1(x),a2(x),a3(x))')

def eeprint25(x,dec):
    printc(9)
    if numberp(x):
        Nprint(x)
        printc(9)
        if ((32 < x) and (x < 256)):
            return Nprint(compress(cons(x,[])))
    elif atom(x):
        return Nprint(x)
    elif ((type(x) == type([1, []])) and (2 < len(x))):
        return Nprint(x)
    elif (flat(x) and equal(34,car(x))):
        return Nprint(x,True)
    elif True:
        dec=10
        printc(40)
        while x:
            if atom(x):
                printc(46)
                printc(32)
                Nprint(x)
                x=nil
            elif (dec < 0):
                Nprint("&")
            elif atom(car(x)):
                Nprint(car(x))
                if cdr(x):
                    printc(32)
            elif (1 < depthless(dec,car(x))):
                Nprint(car(x))
            elif True:
                Nprint("&")
                printc(32)
            dec=(dec + -3)
            gensymz8=car(x)
            x=cdr(x)
            gensymz8
        return printc(41)

    
defq('chdir','lambda x: os.chdir(a1(x))')
defq('getcwd','lambda x: os.getcwd()')
lsp("(defq cd (lambda (x) (if x (chdir x)) (getcwd))))")
defq('isdir','lambda x: Ntest(os.path.isdir(a1(x)))')

defq('delete','lambda x: delete(a1(x),a2(x))')
def delete(x=[],lista=[]):
    if lista!=[]:
        if equal(x,lista[0]):
            return delete(x,lista[1])
        else:
            return cons(lista[0],delete(x,lista[1]))
    return lista

lsp("""(defq imagebox
  (lambda (im p s c)
   (let
    ((p1 (list (car p) (cadr p)))
     (p2 (list (+ (car p) (car s)) (cadr p)))
     (p3 (list (+ (car p) (car s)) (+ (cadr p) (cadr s))))
     (p4 (list (car p) (+ (cadr p) (cadr s)))))
    (imagedraw im p1 p2 c)
    (imagedraw im p2 p3 c)
    (imagedraw im p3 p4 c)
    (imagedraw im p4 p1 c))))
""")

defq('time','lambda x: parse(f"({time.localtime().tm_year} {time.localtime().tm_mon}\
             {time.localtime().tm_mday} {time.localtime().tm_hour} {time.localtime().tm_min}\
             {time.localtime().tm_sec})")')

defq('sleep','lambda x: time.sleep(a1(x))')
def sleep(x): time.sleep(x)
    
lsp("(set (compress '(955)) lambda)")

def googlemap(xtile,ytile, zoom):
    from urllib.request import urlretrieve
    urlretrieve('https://mts1.google.com/vt/x=%d&y=%d&z=%d' % (int(xtile),int(ytile), zoom),"/tmp/temp.png")
    return loadimage("/tmp/temp.png")
defq('googlemap','lambda x: googlemap(a1(x),a2(x),a3(x))')

def maptile(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = (lon_deg + 180.0) / 360.0 * n
    ytile = ((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return cons(xtile,cons(ytile))
defq('maptile','lambda x: maptile(a1(x),a2(x),a3(x))')

def save_all():
     ni=f"/tmp/OBLIST{time.localtime().tm_mday:02d}{time.localtime().tm_hour:02d}{time.localtime().tm_min:02d}"
     print(f"saving {ni}.npy")
     lsp("(setq CWD (cd))")
     lsp(f"(setq {ni} (oblist))")
     lsp(f"(save-module-npy '{ni})")
defq('save-all','lambda x: save_all()')

defq('mouse','lambda x: mouse(a1(x))')
def mouse(id=14):
    if id==[]:
        return os.popen('xinput').read()
    else:    
        a=os.popen(f'xinput --query-state {id}|grep "button"|grep "\[1\]\|\[2\]\|\[3\]"|cut -d "=" -f 2 -').read()
        b=os.popen(f'xinput --query-state {id}|grep "valuator"|grep "\[0\]\|\[1\]"|cut -d "=" -f 2 -').read()
        return parse("("+b+a+")))")

defq('sun_alt','lambda x: sun_alt(a1(x),a2(x),a3(x),a4(x),a5(x),a6(x))')
def sun_alt(mon,day,hour,mins,lat=60.1,lon=25):
    import astropy.coordinates as coord
    from astropy.time import Time
    import astropy.units as u
    if  lat==[]: lat=60.1
    if  lon==[]: lon=25
    loc = coord.EarthLocation(lon=lon * u.deg, lat=lat * u.deg)
    times = f'2022-{mon}-{day}T{hour}:{mins}:00'
    now  = Time(times, format='isot', scale='utc')
    altaz = coord.AltAz(location=loc, obstime=now)
    sun = coord.get_sun(now).transform_to(altaz).alt
    return sun.degree

def length(x=[]):
    if x!=[]:
        return (1 + length(cdr(x)))
    else:
        return 0
defq('length','lambda x: length(a1(x))')

lsp("""(defun imagefill1 (im x y color border)
   (setq DOIT (list (list x y)))
   (while
    DOIT
    (setqpop zz DOIT)
    (setq x (car zz))
    (setq y (cadr zz))
    (when
     (and (< x (car (imagesize im))) (< y (cadr (imagesize im))))
     (setq p (getpixel im x y))
     (cond
      ((equal p color) pass)
      ((equal p border) pass)
      (t
       (putpixel im x y color)
       (setq
        DOIT
        (nconc
         (list
          (list (+ x 1) y)
          (list x (+ y 1))
          (list (- x 1) y)
          (list x (- y 1)))
         DOIT))))))
   True))""")

def imagefill(im=[],x=[],y=[],color=[],border=[]):
    DOIT=cons(cons(x,cons(y,[])),[])
    while DOIT:
        zz=DOIT[0]
        DOIT=DOIT[1]
        x=zz[0]
        y=zz[1][0]
        if ((x < imagesize(im)[0]) and (y < imagesize(im)[1][0])):
            p=getpixel(im,x,y)
            if equal(p,color):
                pass
            elif equal(p,border):
                pass
            elif True:
                putpixel(im,x,y,color)
                DOIT=nconc(cons(cons((x + 1),cons(y,[])),cons(cons(x,cons((y + 1),[])),cons(cons((x - 1),cons(y,[])),cons(cons(x,cons((y - 1),[])),[])))),DOIT)
    return True
defq('imagefill','lambda x: imagefill(a1(x),a2(x),a3(x),a4(x),a5(x))')

lsp(""" (defq secret (lambda (s)
   (setq tulos 0)
   (setq koodi (reverse (explode 'oizeasbthg)))
   (foreach
    (x (explode s))
    (if (member x koodi)
       (setq tulos (+ (* 10 tulos) (+ -1 (length (member x koodi)))))))
   tulos)) """)

import random
defq('random','lambda x: random.random()')
defq('nthchar','lambda x: ord(a2(x)[a1(x)])')
def nthchar (x,y): return ord(y[x])
defq('arraypop','lambda x: a1(x).pop()')

loadlisp("EDITOR.LSP")
loadlisp("COMP.LSP")
lsp("(compile 'comyp2)")
lsp("(setq eeprint251 eeprint25)")
lsp("(compile-edit)")
defq('eeprint25','lambda x: eeprint25(a1(x),a2(x))')
loadlisp("MATH.LSP")
lsp("(define-all)")
lsp("(setq MODULE 'NEW)")
lsp("(global-colors)")

defq('repl','lambda x: repl(a1(x))')
lsp("(defun sys.argv() (cdr (array2list (python-eval 'sys.argv))))")
lsp("(defq -l (nlambda (x) (load x)))")
lsp("(defq -s (nlambda (x) (eval(read-from-str x))))")
lsp("(defq -e (nlambda (x) (pprint (eval(read-from-str x)) 1 t) (cr) (quit)))")
lsp("(defq -f (nlambda (x y) (with-out-file x (pprint (eval(read-from-str y)) 1 t) (cr)) (quit)))")


#lsp("(eval(sys.argv))")
#repl()
