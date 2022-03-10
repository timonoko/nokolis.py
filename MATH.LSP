
(progn
 (defq MODULE MATH)
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
 (defq MATH (curve PRIMES prime PYTHON fib math2 define-all MATH math))
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
   (setq PI (python-eval 'math.pi))
   (setq E (python-eval 'math.e))
   (setq
    round
    (backquote
     lambda
     (x)
     (python-eval (compress (list (explode 'round) 40 (explode x) 41)))))
   MATH-ALL))
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
  fib
  (lambda
   (x)
   (if
    (< x 2)
    x
    (+ (fib (- x 1)) (fib (- x 2))))))
 (defq PYTHON (PRIMES prime fib))
 (defq
  prime
  (lambda
   (end)
   (global PRIMES)
   (if (equal PRIMES ()) (setq PRIMES '(2 3)) pass)
   (for
    (x 2 end)
    (setq yes True)
    (foreach (y PRIMES) (if (= (% x y) 0) (setq yes False)))
    (if yes (if (member x PRIMES) pass (push x PRIMES))))
   (car PRIMES)))
 (defq PRIMES (31 29 23 19 17 13 11 7 5 2 3))
 (defq
  curve
  (lambda
   ()
   (setq im (newimage 600 600 '(0 50 0)))
   (imagetext
    im
    '(30 30)
    '(FreeSansBold.ttf 40 (0 255 255))
    (quote SIN))
   (setq start '(0 0))
   (for
    (x 0 599 10)
    (setq
     end
     (list x (int (+ 300 (* 200 (sin (radians x)))))))
    (imagedraw im start end WHITE)
    (setq start end))
   (showimage im))))
