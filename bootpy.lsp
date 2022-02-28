
(progn
 (defq MODULE BOOTPY)
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
   (if m%x (cons (m%f (car m%x)) (mapp m%f (cdr m%x))))))
 (defq
  koe
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
 (defq
  fib
  (lambda
   (x)
   (if
    (< x 2)
    x
    (+ (fib (- x 1)) (fib (- x 2))))))
 (defq
  save
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
       (quote
        (lambda
         (x)
         (if (assoc x _COMPILED_) (uncompile x))
         (list 'defq x (eval x))))
       (eval m))))
    'pretty)
   (list m 'saved)))
 (defq BOOTPY (uncompile compile mapp koe fib save BOOTPY)))
