
(progn
 (defq MODULE COMP)
 (defq
  comyp2
  (lambda
   (x tabs return)
   (if
    (assoc (car x) CH-NAME)
    (setq x (cons (cadr (assoc (car x) CH-NAME)) (cdr x))))
   (cond
    ((numberp x) (print x))
    ((identp x) (do-globals x))
    ((atom x) (printc 91) (printc 93))
    ((identp (car x))
     (if
      (assoc (car x) COZMP-MACROS)
      (comyp2
       (macroexpand
        (eval (backquote QUOTE (cadr (assoc (car x) COZMP-MACROS)) QUOTE (cdr x))))
       tabs
       return)
      (case
       (car x)
       (setq
        (if
         (member (car (caddr x)) STATEMENTS)
         (comyp2
          (do-lambda
           (backquote setq , (cadr x) ((function (lambda () , (caddr x)))))
           tabs)
          tabs)
         (progn
          (cr)
          (tab tabs)
          (do-globals (cadr x))
          (print '=)
          (comyp2 (caddr x) (+ 4 tabs))
          (car x))))
       (function (comyp2 (cadr x) tabs))
       (quote
        (cond
         ((numberp (cadr x)) (print (cadr x)))
         ((identp (cadr x)) (printc 34) (print (cadr x)) (printc 34))
         (t (print (str-raw (cadr x))))))
       ((eq eqn plus difference times greaterp lessp quotient remainder)
        (printc 40)
        (comyp2 (cadr x) tabs)
        (printc 32)
        (print
         (cadr
          (assoc
           (car x)
           (quote
            ((eqn ==)
             (eq is)
             (plus +)
             (difference -)
             (times *)
             (greaterp >)
             (lessp <)
             (remainder %)
             (quotient /))))))
        (printc 32)
        (comyp2 (caddr x) tabs)
        (printc 41))
       (defq
        (comyp2
         (list 'setq (cadr x) (list 'function (caddr x)))
         tabs
         return))
       (while
        (print 'while)
        (sp)
        (comyp2 (cadr x) tabs)
        (print ':)
        (cozmp-progn (cddr x) (+ 4 tabs)))
       ((if elif)
        (if
         (equal (cadr x) 't)
         (comyp2 (cons (car x) (list 'True (caddr x))) tabs return)
         (progn
          (print (car x))
          (sp)
          (comyp2 (cadr x) tabs)
          (print ':)
          (cozmp-progn (list (caddr x)) (+ 4 tabs) return)
          (when
           (cadddr x)
           (setq x (cadddr x))
           (if
            (equal 'if (car x))
            (cozmp-progn (list (cons 'elif (cdr x))) tabs return)
            (progn
             (cr)
             (tab tabs)
             (print 'else:)
             (cozmp-progn (list x) (+ 4 tabs) return)))))))
       (progn (cozmp-progn (cdr x) tabs return))
       (prog1
        (let
         ((name (gensym)))
         (comyp2
          (backquote progn (setq , name , (cadr x)) @ (cddr x) , name)
          tabs
          return)))
       (list
        (if
         (cddr x)
         (comyp2 (list 'cons (cadr x) (cons 'list (cddr x))))
         (comyp2 (list 'cons (cadr x) '()))))
       ((and or)
        (if
         (cddr x)
         (progn
          (printc 40)
          (comyp2 (cadr x) tabs)
          (printc 32)
          (print (car x))
          (printc 32)
          (comyp2 (cons (car x) (cddr x)))
          (printc 41))
         (comyp2 (cadr x) tabs)))
       (python_for
        (print 'for)
        (sp)
        (print (car (cadr x)))
        (sp)
        (print 'in)
        (sp)
        (print 'range)
        (printc 40)
        (comyp2 (cadr (cadr x)) tabs)
        (print ',)
        (comyp2 (list 'plus 1 (caddr (cadr x))) tabs)
        (when
         (cdddr (cadr x))
         (print ',)
         (comyp2 (cadddr (cadr x)) tabs))
        (printc 41)
        (print ':)
        (cozmp-progn (macroexpand (cddr x)) (+ 4 tabs)))
       (python-foreach
        (print 'for)
        (sp)
        (print (car (cadr x)))
        (sp)
        (print 'in)
        (sp)
        (print 'list2array)
        (printc 40)
        (comyp2 (cadr (cadr x)) tabs)
        (printc 41)
        (print ':)
        (cozmp-progn (macroexpand (cddr x)) (+ 4 tabs)))
       (python-let
        (mapc
         (function (lambda (x) (comyp2 (cons 'setq x) tabs)))
         (cadr x))
        (cozmp-progn (cddr x) tabs return))
       ((car cdr)
        (comyp2 (cadr x) tabs)
        (printc 91)
        (print (case (car x) (car 0) (t 1)))
        (printc 93))
       ((cadr caddr cadddr cddr cdddr)
        (let
         ((y (cadr x)))
         (mapc
          (function
           (lambda
            (z)
            (case
             z
             (97 (setq y (list 'car y)))
             (100 (setq y (list 'cdr y))))))
          (reverse (explode (car x))))
         (comyp2 y tabs return)))
       (return (comyp2 (cadr x) tabs 'return))
       (lambda (print '(mita paskaa)))
       (t
        (print
         (if
          (assoc (car x) CH-NAME)
          (cadr (assoc (car x) CH-NAME))
          (car x)))
        (printc 40)
        (let
         ((rest (cdr x)) (args (cdr (assoc (car x) LAMBDA-ARGS))))
         (unless args (setq args rest))
         (while
          args
          (comyp2 (if rest (pop rest) (car args)) tabs)
          (pop args)
          (if args (print ',))))
        (printc 41))))))))
 (defq
  COMP
  (comppy do-globals full-oblist-name print-nice PYTHON save-py esimerkki_copy esimerkki ch-name want_value STATEMENTS
   link-str expand4ever CH-NAME COZMP-MACROS do-lambda cozmp-lambda comppp cozmp-progn lambda-args COMP comyp2))
 (defq
  lambda-args
  (lambda
   (x eka)
   (if
    eka
    (progn (printc 40) (lambda-args x) (printc 41))
    (if
     x
     (progn
      (print (pop x))
      (print-nice (34 61 91 93))
      (if x (print ',))
      (lambda-args x))))))
 (defq
  cozmp-progn
  (lambda
   (x tabs return)
   (push x CP)
   (unless (member (caar x) '(setq progn prog1)) (cr) (tab tabs))
   (when
    (and
     return
     x
     (not (cdr x))
     (not
      (member
       (caar x)
       '(python-let return foreach elif python-foreach python_for for setq progn if while prog1))))
    (print 'return)
    (sp))
   (comyp2 (car x) tabs (unless (cdr x) return))
   (if (cdr x) (cozmp-progn (cdr x) tabs return))))
 (defq
  comppp
  (lambda
   (x tabs)
   (unless (numberp tabs) (setq tabs 0))
   (setq LAMBDA-ARGS nil)
   (setq z (if (identp x) (list 'setq x (eval x)) x))
   (comyp2 (expand4ever z) tabs)
   (cr)
   (when (identp x) (link-str x) (cr) (cr))
   file))
 (defq
  cozmp-lambda
  (lambda
   (x tabs)
   (cr)
   (cr)
   (tab tabs)
   (print 'def)
   (sp)
   (let
    ((name (gensym)) (new-args (cadr x)))
    (print name)
    (push (cons name new-args) LAMBDA-ARGS)
    (lambda-args new-args t)
    (print ':)
    (cozmp-progn
     (macroexpand (do-lambda (cddr x) (+ 4 tabs)))
     (+ tabs 4)
     (quote return))
    (cr)
    name)))
 (defq
  do-lambda
  (lambda
   (x tabs y)
   (cond
    ((atom x) x)
    ((equal (car x) 'quote) x)
    ((equal (car x) 'function) (do-lambda (cadr x) tabs))
    ((equal (car x) 'lambda)
     (cozmp-lambda
      (list 'lambda (cadr x) (cons 'progn (cddr x)))
      tabs))
    (t (cons (do-lambda (car x) tabs) (do-lambda (cdr x) tabs))))))
 (defq
  COZMP-MACROS
  ((prog1
    (lambda
     (x)
     (setq y (gensym))
     (backquote progn (setq , y , (car x)) @ (cdr x) , y)))
   (arrayp
    (lambda
     (x)
     (backquote
      and
      (eqn (type @ x) (type '(1)))
      (< 2 (len @ x)))))
   (cr '(progn (printc 13) (printc 10)))
   (sp '(printc 32))
   (repeat-times
    (lambda
     (x)
     (let
      ((name (gensym)))
      (backquote
       progn
       (setq , name , (car x))
       (while
        (< 0 , name)
        (progn @ (cdr x))
        (setq , name (- , name 1)))))))))
 (defq
  CH-NAME
  ((let python-let)
   (foreach python-foreach)
   (for python_for)
   (eval Neval)
   (filter filterpy)
   (mapp mappy)
   (map mappy)
   (mapc mapcpy)
   (print Nprint)))
 (defq expand4ever (lambda (x) (do-lambda (macroexpand (ch-name x)) tabs)))
 (defq
  link-str
  (lambda
   (x y)
   (setq y (eval x))
   (print-nice (34 100 101 102 113 40 39))
   (print x)
   (print-nice (34 39 44 39 108 97 109 98 100 97 32 120 58 32))
   (print x)
   (printc 40)
   (for
    (z 1 (length (cadr y)))
    (print 'a)
    (print z)
    (print '(x))
    (if (< z (length (cadr y))) (print ',)))
   (print-nice (34 41 39 41))
   True))
 (defq STATEMENTS (if setq))
 (defq want_value (lambda (x) (backquote ((function (lambda () , x))))))
 (defq
  ch-name
  (lambda
   (x)
   (mapc
    (function (lambda (a) (setq x (subst (car a) (cadr a) x))))
    CH-NAME)
   x))
 (defq
  esimerkki
  (lambda () (foreach (x '(1 2 3)) (print x) (cr))))
 (defq
  esimerkki_copy
  (lambda
   (a b)
   (for
    (x 1 a)
    (for
     (y 1 b)
     (print (list x 'x y '= (* x y)))
     (cr)))))
 (defq
  save-py
  (lambda
   (m)
   (if (null m) (setq m MODULE))
   (with-out-file
    (quote TEMPORARY.PY)
    (progn
     (print-nice (34 108 115 112 40 34 34 34))
     (cr)
     (pprint
      (cons
       (quote progn)
       (cons
        (list 'defq 'MODULE m)
        (mapp
         (quote
          (lambda
           (x)
           (if (assoc x _COMPILED_) (uncompile x))
           (list 'defq x (eval x))))
         (eval m)))))
     (cr)
     (print-nice (34 34 34 34 41)))
    (progn
     (compile 'comyp2)
     (mapc
      (function
       (lambda
        (x)
        (if
         (equal 'lambda (car (eval x)))
         (progn (cr) (uncompile 'x) (comppp x 0) (cr))
         (let
          ((nam (nconc (explode 'oblist.) (oblist-name-raw x))))
          (push x GLOBALS)
          (comyp2
           (list 'setq (full-oblist-name x) (list 'quote (eval x)))
           0)
          (cr)))))
      PYTHON))
    (print (compress (cdr '(34 114 101 112 108 40 41))))
    (cr))
   (with-out-file
    (compress (append (explode m) '(46 98 117 105 108 100)))
    (print 'cat)
    (sp)
    (print 'nokolis.py)
    (sp)
    (print 'TEMPORARY.PY)
    (sp)
    (print '>)
    (sp)
    (print (setq py-file (compress (append (explode m) '(46 112 121)))))
    (cr)
    (print 'python3)
    (sp)
    (print py-file)
    (cr))
   (python-exec (file2str 'TEMPORARY.PY))
   (list m 'compiled)))
 (defq PYTHON (PRIMES prime fib))
 (defq print-nice (nlambda (x) (print (compress (cdr x)))))
 (defq
  full-oblist-name
  (lambda (x) (compress (nconc (explode 'oblist.) (explode (oblist-name-raw x))))))
 (defq
  do-globals
  (lambda (x) (print (if (member x GLOBALS) (full-oblist-name x) x))))
 (defq
  comppy
  (lambda
   (x)
   (if (assoc x _COMPILED_) (uncompile x))
   (push (cons x (eval x)) _COMPILED_)
   (with-out-file '/tmp/tmp.py (comppp x))
   (python-exec (file2str '/tmp/tmp.py))
   (file2str '/tmp/tmp.py))))
