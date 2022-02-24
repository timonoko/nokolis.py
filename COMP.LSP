
(progn
 (defq MODULE COMP)
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
 (defq
  expand4ever
  (lambda
   (x y)
   (if (equal x y) x (expand4ever (do-lambda (macroexpand x)) x))))
 (defq CH-NAME ((eval Neval) (print Nprint)))
 (defq
  comp-macros
  ((printc lambda (x) (backquote print (chr @ x)))
   (repeat-times
    lambda
    (x)
    (let
     ((name (gensym)))
     (backquote
      progn
      (setq , name , (car x))
      (while
       (< 0 , name)
       (progn @ (cdr x))
       (setq , name (- , name 1))))))))
 (defq
  do-lambda
  (lambda
   (x y)
   (cond
    ((atom x) x)
    ((equal (car x) 'quote) x)
    ((equal (car x) 'function) (do-lambda (cadr x)))
    ((equal (car x) 'lambda)
     (push (append (cadr x) (car DYN-VARS)) DYN-VARS)
     (prog1
      (comp-lambda
       (list
        (quote lambda)
        (cadr x)
        (macroexpand (do-lambda (macroexpand (cons 'progn (cddr x))))))
       0)
      (pop DYN-VARS)))
    ((setq y (assoc (car x) comp-macros))
     (do-lambda (macroexpand (do-lambda ((cdr y) (cdr x))))))
    (t (cons (do-lambda (car x)) (do-lambda (cdr x)))))))
 (defq
  comp-lambda
  (lambda
   (x tabs)
   (cr)
   (print 'def)
   (sp)
   (let
    ((name (gensym)) (new-args (car DYN-VARS)))
    (print name)
    (push (cons name new-args) LAMBDA-ARGS)
    (lambda-args new-args t)
    (print ':)
    (comp-progn (cddr x) 4 'return)
    (cr)
    (cr)
    name)))
 (defq
  comp
  (lambda
   (x file)
   (setq DYN-VARS nil)
   (setq LAMBDA-ARGS nil)
   (setq z (if (identp x) (list 'setq x (eval x)) x))
   (if
    file
    (with-out-file file (function (lambda () (comp2 (expand4ever z)) (cr) (link-str x))))
    (comp2 (expand4ever z)))
   (cr)
   file))
 (defq
  comp-progn
  (lambda
   (x tabs return)
   (unless (equal (caar x) 'progn) (cr) (tab tabs))
   (when
    (and
     return
     x
     (not (cdr x))
     (not (member (caar x) '(setq progn if while prog1))))
    (print 'return)
    (sp))
   (comp2 (car x) tabs (unless (cdr x) return))
   (if (cdr x) (comp-progn (cdr x) tabs return))))
 (defq
  lambda-args
  (lambda
   (x eka)
   (if eka (printc 40))
   (if
    (atom x)
    (print x)
    (progn
     (lambda-args (car x))
     (when (cdr x) (print ',) (lambda-args (cdr x)))))
   (if eka (printc 41))))
 (defq COMP (link-str comment-on-compiler expand4ever CH-NAME comp-macros do-lambda comp-lambda comp comp-progn lambda-args COMP comp2))
 (defq
  comp2
  (lambda
   (x tabs return)
   (unless tabs (setq tabs 0))
   (cond
    ((numberp x) (print x))
    ((identp x) (print x))
    ((atom x) (printc 91) (printc 93))
    ((identp (car x))
     (case
      (car x)
      (setq
       (print (cadr x))
       (print '=)
       (comp2 (caddr x) tabs)
       (car x))
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
       (comp2 (list 'setq (cadr x) (list 'function (caddr x)))))
      (while
       (print 'while)
       (sp)
       (comp2 (cadr x) tabs)
       (print ':)
       (comp-progn (cddr x) (+ 4 tabs)))
      (if
       (if
        (equal (cadr x) 't)
        (comp-progn (list (caddr x)) tabs return)
        (progn
         (print 'if)
         (sp)
         (comp2 (cadr x) tabs)
         (print ':)
         (comp-progn (list (caddr x)) (+ 4 tabs) return)
         (when
          (cadddr x)
          (cr)
          (tab tabs)
          (print 'else:)
          (comp-progn (list (cadddr x)) (+ 4 tabs) return)))))
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
       (printc 41))))))))
