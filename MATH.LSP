
(progn
 (defq MODULE MATH)
 (defq
  define-all
  (lambda
   ()
   (python-exec (compress (list (explode 'import) 32 (explode 'math))))
   (setq
    MATH-ALL
    (array2list
     (python-eval (compress (list (explode 'dir) 40 (explode 'math) 41)))))
   (map
    (function
     (lambda
      (x)
      (unless
       (equal (getchar x 1) 95)
       (set x (backquote lambda (y) (math QUOTE x y)))
       x)))
    MATH-ALL)
   (setq pi (python-eval 'math.pi))
   (setq e (python-eval 'math.e))
   (setq
    round
    (backquote
     lambda
     (x)
     (python-eval (compress (list (explode 'round) 40 (explode x) 41)))))
   MATH-ALL))
 (defq MATH (define-all MATH math))
 (defq
  math
  (lambda
   (f x)
   (python-eval
    (compress (list (explode 'math.) (explode f) 40 (explode x) 41)))))

(define-all)
 )

