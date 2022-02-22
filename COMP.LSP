
(progn
 (defq MODULE COMP)
 (defq
  comp-macros
  ((repeat-times
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
        'lambda
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
   (if (identp x) (setq x (list 'setq x (eval x))))
   (if
    file
    (with-out-file file '(comp2 (do-lambda (macroexpand x))))
    (comp2 (do-lambda (macroexpand x))))
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
     (not (member (caar x) '(progn if while))))
    (print 'return)
    (sp))
   (comp2 (car x) tabs return)
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
 (defq COMP (comp-macros do-lambda comp-lambda comp comp-progn lambda-args COMP comp2))
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
        (t (let ((name (gensym))) (set name (cadr x)) (print name)))))
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
        (comp-progn (list (cadddr x)) (+ 4 tabs) return)))
      (progn (comp-progn (cdr x) tabs return))
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
       (print (car x))
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
