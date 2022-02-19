
'((19 / 2 - 2022) (15 : 37 : 22 11))
(defq *package* BOOTPY)

(defun orderp
 (x y)
 (cond
  ((equal x y) t)
  ((null x) t)
  ((null y) nil)
  ((atom x)
   (if
    (atom y)
    (cond
     ((numberp x)
      (if (numberp y) (not (greaterp x y)) t))
     ((identp x)
      (if
       (identp y)
       (let
        ((n 1))
        (while
         (eqn (getchar x n) (getchar y n))
         (setq n (add1 n)))
        (not (greaterp (getchar x n) (getchar y n))))
       nil))
     (t t))
    t))
  ((atom y) nil)
  ((equal (car x) (car y))
   (orderp (cdr x) (cdr y)))
  (t (orderp (car x) (car y)))))

(defq BOOTPY.LSP ())

(defq merge1 (----))

(defun nmerge1
 (a b)
 (let
  ((res a) (tmp a))
  (let
   ((ali
     (quote
      (lambda
       (x y z)
       (while
        (and x (orderp (car x) (car y)))
        (setq tmp x)
        (pop x))
       (rplacd tmp y)
       (setq tmp y)
       (pop y)
       (setq a (if z x y))
       (setq b (if z y x))))))
   (pop a)
   (while b
    (ali a b t)
    (if a (ali b a) (setq b nil)))
   res)))

(defun nmerge
 (a b)
 (cond
  ((null a) b)
  ((null b) a)
  ((orderp (car a) (car b)) (nmerge1 a b))
  (t (nmerge1 b a))))

(defun split
 (l)
 (and
  (cdr l)
  (setq l
   (nthcdr (int (sub1 (quotient (length l) 2))) l))
  (prog1 (cdr l) (rplacd l nil))))

(defun mergesort
 (a)
 (cond
  ((null (cdr a)) a)
  ((null (cddr a))
   (if
    (orderp (car a) (cadr a))
    a
    (let
     ((tmp (cadr a)))
     (rplaca (cdr a) (car a))
     (rplaca a tmp))))
  (t
   (let
    ((b (split a)))
    (nmerge (mergesort a) (mergesort b))))))

(defun fib
 (x)
 (if
  (< x 2)
  x
  (+ (fib (- x 1)) (fib (- x 2)))))

(defun save
 (y x)
 (hex)
 (if
  (or (atom x) (not (identp y)))
  (progn
   (prints
    '*package*
    'name
    'assumed
    'to
    'be
    *package*)
   (cr)
   (setq x (eval *package*))
   (setq y
    (compress (nconc (explode *package*) (cons 46 (explode 'LSP)))))
   (prints 'filename 'assumed 'to 'be y)))
 (let
  ((back
    (compress
     (reverse
      (append (explode 'KAB) (member 46 (reverse (explode y))))))))
  (cr)
  (prints 'old y '=> back)
  (unlink back)
  (rename-file y back))
 (setq y (create y))
 (out y)
 (cr)
 (print (list 'quote (list (date) (time))))
 (cr)
 (print (list 'defq '*package* *package*))
 (cr)
 (mapc x
  (quote
   (lambda
    (x)
    (out 0)
    (cr)
    (print x)
    (out y)
    (cr)
    (if
     (eq *package* 'BOOT)
     (pprint (list 'defq x (definition-of x)))
     (ppr-def x (definition-of x)))
    (cr))))
 (out 0)
 (close y))

(defq BOOTPY (orderp BOOTPY.LSP merge1 nmerge1 nmerge split mergesort fib save BOOTPY))
