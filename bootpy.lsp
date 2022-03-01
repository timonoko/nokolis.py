
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
 (defq BOOTPY (uncompile compile mapp koe fib BOOTPY)))
