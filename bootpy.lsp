(progn
 (defq MODULE BOOTPY)
 (defq compile
  (lambda
   (x)
   (if
    (assoc x *COMPILED*)
    x
    (progn
     (push (cons x (eval x)) *COMPILED*)
     (set x (macroexpand (eval x)))
     (list x 'compiled)))))
 (defq mapp
  (lambda
   (m%f m%x)
   (if m%x
    (cons (m%f (car m%x)) (mapp m%f (cdr m%x))))))
 (defq save-module
  (lambda
   (m)
   (if (null m) (setq m MODULE))
   (print-to-file
    (compress (append (explode m) '(46 76 83 80)))
    (cons
     'progn
     (cons
      (list 'defq 'MODULE m)
      (mapp
       '(lambda (x) (list 'defq x (eval x)))
       (eval m))))
    'pretty)
   (list m 'saved)))
 (defq koe
  (lambda
   (x)
   ((function
     (lambda
      (y)
      (repeat-times
       (quotient (difference (plus 100 1) 1) 1)
       (print (plus x y))
       (sp)
       (setq y (plus y 1)))))
    1)))
 (defq fib
  (lambda
   (x)
   (if
    (lessp x 2)
    x
    (+ (fib (- x 1)) (fib (- x 2))))))
 (defq save
  (lambda
   (m command)
   (if (null m) (setq m MODULE))
   (print-to-file
    (compress (append (explode m) '(46 76 83 80)))
    (cons
     'progn
     (cons
      (list 'defq 'MODULE m)
      (cons
       (mapp
       '(lambda (x) (list 'defq x (eval x)))
        (eval m))
       (list command))))
     'pretty)
   (list m 'saved)))
 (defq BOOTPY
  (compile mapp save-module  koe
    fib save BOOTPY)))
