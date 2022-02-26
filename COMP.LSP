
(progn
 (defq MODULE COMP)
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
  esimerkki
  (lambda () (foreach (x '(1 2 3)) (print x) (cr))))
 (defq
  ch-name
  (lambda
   (x)
   (mapc
    (function (lambda (a) (setq x (subst (car a) (cadr a) x))))
    CH-NAME)
   x))
 (defq want_value (lambda (x) (backquote ((function (lambda () , x))))))
 (defq STATEMENTS (if setq))
 (defq
  link-str
  (lambda
   (x y pr)
   (setq y (eval x))
   (defq pr (nlambda (x) (print (compress (cdr x)))))
   (pr (34 100 101 102 113 40 39))
   (print x)
   (pr (34 39 44 39 108 97 109 98 100 97 32 120 58 32))
   (print x)
   (printc 40)
   (if
    (car (cadr y))
    (pr (34 78 101 118 97 108 40 99 97 114 40 120 41 41)))
   (if
    (cdr (cadr y))
    (pr
     (34 , 78 101 118 97 108 40 99 97 d
      114 40 120 41 41)))
   (if
    (cddr (cadr y))
    (pr
     (34 , 78 101 118 97 108 40 99 97 d
      d 114 40 120 41 41)))
   (pr (34 41 39 41))
   True))
 (defq
  comment-on-compiler
  (While I have totally perfect Nokolisp-to-Pascal and Nokolisp-to-C compiler , I
   realized I dont want to such unreadable mess with gensyms and
   mysterious functions implementing retun-with-value statements. This is deliberately Pythonic , you
   cannot assign from SETQ or IF , and OR works only
   in expressions. LET seems to generate LAMBDA and GENSYM-named function ,
   but that is avoidable))
 (defq expand4ever (lambda (x) (do-lambda (macroexpand (ch-name x)) 0)))
 (defq
  CH-NAME
  ((foreach python-foreach)
   (for python_for)
   (eval Neval)
   (mapp mappy)
   (map mappy)
   (mapc mapcpy)
   (print Nprint)))
 (defq
  COMP-MACROS
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
  do-lambda
  (lambda
   (x tabs y)
   (unless tabs (setq tabs 16))
   (cond
    ((atom x) x)
    ((equal (car x) 'quote) x)
    ((equal (car x) 'function) (do-lambda (cadr x) tabs))
    ((equal (car x) 'lambda)
     (comp-lambda
      (list 'lambda (cadr x) (cons 'progn (cddr x)))
      tabs))
    (t (cons (do-lambda (car x) tabs) (do-lambda (cdr x) tabs))))))
 (defq
  comp-lambda
  (lambda
   (x tabs)
   (unless tabs (setq tabs 8))
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
    (comp-progn
     (macroexpand (do-lambda (cddr x) (+ 4 tabs)))
     (+ tabs 4)
     (quote return))
    (cr)
    (cr)
    name)))
 (defq
  comp
  (lambda
   (x file)
   (setq LAMBDA-ARGS nil)
   (setq z (if (identp x) (list 'setq x (eval x)) x))
   (if
    file
    (with-out-file
     file
     (function
      (lambda
       ()
       (print
        (compress
         (cdr
          (quote
           (34 102 114 111 109 32 110 111 107 111 108
            105 115 32 105 109 112 111 114 116 32 42)))))
       (cr)
       (comp2 (expand4ever z) 0)
       (cr)
       (link-str x)
       (cr))))
    (comp2 (expand4ever z)))
   (cr)
   file))
 (defq
  comp-progn
  (lambda
   (x tabs return)
   (unless (member (caar x) '(setq progn prog1)) (cr) (tab tabs))
   (when
    (and
     return
     x
     (not (cdr x))
     (not
      (member (caar x) '(foreach elif python-foreach python_for for setq progn if while prog1))))
    (print 'return)
    (sp))
   (comp2 (car x) tabs (unless (cdr x) return))
   (if (cdr x) (comp-progn (cdr x) tabs return))))
 (defq
  lambda-args
  (lambda
   (x eka)
   (if
    eka
    (progn (printc 40) (lambda-args x) (printc 41))
    (if
     x
     (progn (print (pop x)) (if x (print ',)) (lambda-args x))))))
 (defq
  COMP
  (esimerkki_copy esimerkki ch-name want_value STATEMENTS link-str comment-on-compiler expand4ever CH-NAME COMP-MACROS do-lambda
   comp-lambda comp comp-progn lambda-args COMP comp2))
 (defq
  comp2
  (lambda
   (x tabs return)
   (unless tabs (setq tabs 0))
   (if
    (assoc (car x) CH-NAME)
    (setq x (cons (cadr (assoc (car x) CH-NAME)) (cdr x))))
   (cond
    ((numberp x) (print x))
    ((identp x) (print x))
    ((atom x) (printc 91) (printc 93))
    ((identp (car x))
     (if
      (assoc (car x) COMP-MACROS)
      (comp2
       (macroexpand
        (eval (backquote QUOTE (cadr (assoc (car x) COMP-MACROS)) QUOTE (cdr x))))
       tabs
       return)
      (case
       (car x)
       (setq
        (if
         (member (car (caddr x)) STATEMENTS)
         (comp2
          (do-lambda
           (backquote setq , (cadr x) ((function (lambda () , (caddr x)))))
           tabs)
          tabs)
         (progn
          (cr)
          (tab tabs)
          (print (cadr x))
          (print '=)
          (comp2 (caddr x) (+ 4 tabs))
          (car x))))
       (function (comp2 (cadr x) tabs))
       (quote
        (cond
         ((numberp (cadr x)) (print (cadr x)))
         ((identp (cadr x)) (printc 34) (print (cadr x)) (printc 34))
         (t (print (str-raw (cadr x))))))
       ((eq eqn plus difference times greaterp lessp quotient)
        (printc 40)
        (comp2 (cadr x) tabs)
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
             (quotient /))))))
        (printc 32)
        (comp2 (caddr x) tabs)
        (printc 41))
       (defq
        (comp2
         (list 'setq (cadr x) (list 'function (caddr x)))
         tabs
         return))
       (while
        (print 'while)
        (sp)
        (comp2 (cadr x) tabs)
        (print ':)
        (comp-progn (cddr x) (+ 4 tabs)))
       ((if elif)
        (if
         (equal (cadr x) 't)
         (comp2 (cons (car x) (list 'True (caddr x))) tabs return)
         (progn
          (print (car x))
          (sp)
          (comp2 (cadr x) tabs)
          (print ':)
          (comp-progn (list (caddr x)) (+ 4 tabs) return)
          (when
           (cadddr x)
           (setq x (cadddr x))
           (if
            (equal 'if (car x))
            (comp-progn (list (cons 'elif (cdr x))) tabs return)
            (progn
             (cr)
             (tab tabs)
             (print 'else:)
             (comp-progn (list x) (+ 4 tabs) return)))))))
       (progn (comp-progn (cdr x) tabs return))
       (prog1
        (let
         ((name (gensym)))
         (comp2
          (backquote progn (setq , name , (cadr x)) @ (cddr x) , name)
          tabs
          return)))
       (list
        (if
         (cddr x)
         (comp2 (list 'cons (cadr x) (cons 'list (cddr x))))
         (comp2 (list 'cons (cadr x) '()))))
       ((and or)
        (if
         (cddr x)
         (progn
          (printc 40)
          (comp2 (cadr x) tabs)
          (printc 32)
          (print (car x))
          (printc 32)
          (comp2 (cons (car x) (cddr x)))
          (printc 41))
         (comp2 (cadr x) tabs)))
       (python_for
        (print 'for)
        (sp)
        (print (car (cadr x)))
        (sp)
        (print 'in)
        (sp)
        (print 'range)
        (printc 40)
        (comp2 (cadr (cadr x)) tabs)
        (print ',)
        (comp2 (list 'plus 1 (caddr (cadr x))) tabs)
        (when
         (cdddr (cadr x))
         (print ',)
         (comp2 (cadddr (cadr x)) tabs))
        (printc 41)
        (print ':)
        (comp-progn (macroexpand (cddr x)) (+ 4 tabs)))
       (python-foreach
        (print 'for)
        (sp)
        (print (car (cadr x)))
        (sp)
        (print 'in)
        (sp)
        (print 'list2array)
        (printc 40)
        (comp2 (cadr (cadr x)) tabs)
        (printc 41)
        (print ':)
        (comp-progn (macroexpand (cddr x)) (+ 4 tabs)))
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
          (comp2 (if rest (pop rest) (car args)) tabs)
          (pop args)
          (if args (print ',))))
        (printc 41)))))))))
