
'((20 / 2 - 2022) (0 : 18 : 10 10))
(defq *package* BOOTPY)

(defq koe
 (((''lambda))
  y x
  '-
  as
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
   (prints 'filename 'assumed 'to 'be y))
  (let
   ((back
     (compress
      (reverse
       (append (explode 'KAB) (member 46 (reverse (explode y))))))))
   (cr)
   (prints 'old y '=> back)
   (unlink back)
   (rename-file y back))
  ((y) ('()))
  ('())
  (list 'quote (list (date) (time)))
  (cr)
  '(print (list 'defq '*package* *package*))
  '(cr)
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
  (close y)
  asd))

(defq iik ())

(defun depthless
 (n x)
 (if
  (> 0 n)
  0
  (if
   (atom x)
   (- n 1)
   (depthless (depthless n (car x)) (cdr x)))))

(defun nedit
 (x exit v)
 (eeprint x)
 (setq v 0)
 (while
  (not exit)
  (set_cursor 2 1)
  (progn
   (repeat-times (length x) (sp) (sp) (sp) (sp) (cr))
   (printc 41)
   (sp)
   (sp)
   (sp))
  (set_cursor (+ v 2) 1)
  (print '===>)
  (cr)
  (setq ch (readcc))
  (if (eqn ch 27) (setq ch (readcc)))
  (if
   (member ch '(0 91))
   (setq ch (plus 200 (readcc))))
  (cond
   ((member ch '(275 268)) (setq exit t))
   ((member ch '(280 266))
    (if (lessp v (length x)) (setq v (plus v 1))))
   ((member ch '(272 265))
    (if (greaterp v 0) (setq v (plus v -1))))
   ((member ch '(13 110))
    (if
     (lessp v 1)
     (setq x (cons () x))
     (rplacd
      (nthcdr (plus v -1) x)
      (cons () (nthcdr v x))))
    (eeprint x)
    (set_cursor (plus v 2) 4)
    (rplaca (nthcdr v x) (read))
    (eeprint x))
   ((member ch '(277 267))
    (nedit (nth v x))
    (eeprint x))
   ((eqn ch 121)
    (if
     (eqn v 0)
     (setq x (cdr x))
     (rplacd
      (nthcdr (- v 1) x)
      (nthcdr (+ v 1) x)))
    (eeprint x))
   ((eqn ch 113)
    (rplaca (nthcdr v x) (list 'quote (nth v x)))
    (eeprint x))
   ((eqn ch 114)
    (if
     (eqn v 0)
     (setq x
      (append (nth v x) (nthcdr (plus v 1) x)))
     (rplacd
      (nthcdr (plus v -1) x)
      (append (nth v x) (nthcdr (plus v 1) x))))
    (eeprint x))
   ((eqn ch 97)
    (rplaca (nthcdr v x) (list (nth v x)))
    (eeprint x))
   ((eqn ch 98)
    (if
     (eqn v 0)
     (setq x (cons (car x) x))
     (rplacd
      (nthcdr (- v 1) x)
      (cons (nth v x) (nthcdr v x))))
    (eeprint x))
   ((eqn ch 119)
    (if
     (eqn v 0)
     (setq x
      (cons (list (car x) (cadr x)) (cddr x)))
     (rplacd
      (nthcdr (- v 1) x)
      (cons
       (list (nth v x) (nth (plus v 1) x))
       (nthcdr (plus v 2) x))))
    (eeprint x))))
 x)

(defun eeprint25
 (x)
 (sp)
 (sp)
 (if
  (atom x)
  (print x)
  (let
   ((dec 10))
   (printc 40)
   (while
    (and x (lessp (tab) 60))
    (cond
     ((atom x)
      (printc 46)
      (sp)
      (print x)
      (setq x nil))
     ((lessp dec 0) (print '&))
     ((atom (car x))
      (print (car x))
      (if (cdr x) (sp)))
     ((< 1 (depthless dec (car x))) (print (car x)))
     (t (print '&) (sp)))
    (setq dec (plus dec -3))
    (pop x))
   (printc 41)))
 (hex nil))

(defun eeprint
 (x)
 (erase_page)
 (if *MORE* (print '*MORE*) (printc 40))
 (cr)
 (for
  (p 0 22)
  (when
   (nthcdr p x)
   (tab 3)
   (eeprint25 (nth p x))
   (cr)))
 (if (nthcdr 23 x) (print '*MORE*) (printc 41)))

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

(defq merge1 ())

(defun nmerge1
 (a b)
 (let
  ((res a) (tmp a))
  (pop a)
  (while b
   (nmerge2 a b t)
   (if a (nmerge2 b a) (setq b nil)))
  res))

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

(defq BOOTPY
 (koe iik depthless nedit eeprint25 eeprint orderp merge1
  nmerge1 nmerge split mergesort fib save BOOTPY))
