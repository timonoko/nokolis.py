
(progn
 (defq MODULE MATH)
 (defq
  math2
  (lambda
   (func)
   (set
    func
    (backquote
     lambda
     (argu argu2)
     (python-eval
      QUOTE
      (compress
       (list
        (explode 'math.)
        (explode func)
        40
        (explode 'oblist.)
        (explode (oblist-name-raw 'argu))
        (explode ',)
        (explode 'oblist.)
        (explode (oblist-name-raw 'argu2))
        41)))))))
 (defq
  define-all
  (lambda
   ()
   (python-exec (compress (list (explode 'import) 32 (explode 'math))))
   (setq
    MATH-ALL
    (array2list
     (python-eval (compress (list (explode 'dir) 40 (explode 'math) 41)))))
   (map math MATH-ALL)
   (map math2 '(pow log copysign))
   (setq pi (python-eval 'math.pi))
   (setq e (python-eval 'math.e))
   (setq
    round
    (backquote
     lambda
     (x)
     (python-eval (compress (list (explode 'round) 40 (explode x) 41)))))
   MATH-ALL))
 (defq MATH (math2 define-all MATH math))
 (defq
  math
  (lambda
   (func)
   (set
    func
    (backquote
     lambda
     (argu)
     (python-eval
      QUOTE
      (compress
       (list
        (explode 'math.)
        (explode func)
        40
        (explode 'oblist.)
        (explode (oblist-name-raw 'argu))
        41)))))))
(define-all)
 )
