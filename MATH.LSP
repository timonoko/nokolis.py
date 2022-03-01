
(progn
 (defq MODULE MATH)
 (defq PRIMES (31 29 23 19 17 13 11 7 5 2 3))
 (defq
  prime
  (lambda
   (end)
   (if (equal PRIMES ()) (setq PRIMES '(2 3)) pass)
   (for
    (x 2 end)
    (setq yes True)
    (foreach (y PRIMES) (if (= (% x y) 0) (setq yes False)))
    (if yes (if (member x PRIMES) pass (push x PRIMES))))
   (car PRIMES)))
 (defq PYTHON (PRIMES prime fib))
 (defq
  fib
  (lambda
   (x)
   (if
    (< x 2)
    x
    (+ (fib (- x 1)) (fib (- x 2))))))
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
 (defq MATH (PRIMES prime PYTHON fib math2 define-all MATH math))
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
        41))))))))
