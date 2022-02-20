
'((20 / 2 - 2022) (10 : 5 : 0 69))
(defq *package* BOOTPY)

(defun eeinsert
 (v x y)
 (if
  (lessp v 1)
  (setq x (cons () x))
  (rplacd
   (nthcdr (plus v -1) x)
   (cons () (nthcdr v x))))
 (if y
  (rplaca (nthcdr v x) y)
  (progn
   (eeprint x)
   (set_cursor (plus v 2) 4)
   (rplaca (nthcdr v x) (read))))
 x)

(defun locate
 (x y)
 (if
  (atom y)
  nil
  (if
   (member x y)
   (list (sub1 (length (member x (reverse y)))))
   (let
    ((z 0) (z2))
    (while
     (and y (not z2))
     (if
      (not (setq z2 (locate x (pop y))))
      (setq z (add1 z))))
    (if z2 (cons z z2))))))

(defq koe
 (((cr) defq)
  (list ('quote 'quote) (list (date) (time)))
  (happa)
  (hui ())
  'defq
  5 asdasd
  (out 0)
  ((close y))
  (asd)
  (asd)
  dsd))

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
 (x dept goto exit v)
 (if (null x) (setq x (list 'tyhja)))
 (if goto (setq v (pop goto)))
 (if (null dept) (setq dept 0))
 (if (null arrayp) (defun arrayp () ()))
 (if (null v) (setq v 0))
 (eeprint x)
 (while
  (and (not exit) (not EXIT))
  (setq THIS (nth v x))
  (if goto
   (setq ch 6)
   (progn
    (set_cursor 2 1)
    (progn
     (repeat-times (length x) (sp) (sp) (sp) (sp) (cr))
     (printc 41)
     (sp)
     (sp)
     (sp))
    (set_cursor (+ v 2) 1)
    (print '===>)
    (repeat-times (- (length x) v) (cr))
    (setq ch (readcc))
    (if (eqn ch 27) (setq ch (readcc)))
    (if
     (member ch '(0 91))
     (setq ch (plus 200 (readcc)))
     (setq ch (compress (list ch))))))
  (cond
   ((equal ch 6)
    (print goto)
    (if
     (atom THIS)
     ()
     (rplaca (nthcdr v x) (nedit THIS (add1 dept) goto)))
    (setq goto nil)
    (eeprint x))
   ((member ch '(275 268)) (setq exit t))
   ((member ch '(280 266))
    (if (lessp v (length x)) (setq v (plus v 1))))
   ((member ch '(272 265))
    (if (greaterp v 0) (setq v (plus v -1))))
   ((member ch '(277 267))
    (if
     (atom THIS)
     ()
     (rplaca
      (nthcdr v x)
      (if
       (arrayp (nth v x))
       (list2array (nedit (array2list (nth v x))))
       (nedit (nth v x)))))
    (eeprint x))
   ((eq ch 'n)
    (setq x (eeinsert v x))
    (eeprint x))
   ((eq ch 'y)
    (push THIS JEMMA)
    (if
     (eqn v 0)
     (setq x (cdr x))
     (rplacd
      (nthcdr (- v 1) x)
      (nthcdr (+ v 1) x)))
    (eeprint x))
   ((eq ch 'q)
    (rplaca (nthcdr v x) (list 'quote (nth v x)))
    (eeprint x))
   ((eq ch 'r)
    (if
     (eqn v 0)
     (setq x
      (append (nth v x) (nthcdr (plus v 1) x)))
     (rplacd
      (nthcdr (plus v -1) x)
      (append (nth v x) (nthcdr (plus v 1) x))))
    (eeprint x))
   ((eq ch 'a)
    (rplaca (nthcdr v x) (list (nth v x)))
    (eeprint x))
   ((eq ch 'b)
    (if
     (eqn v 0)
     (setq x (cons (car x) x))
     (rplacd
      (nthcdr (- v 1) x)
      (cons (nth v x) (nthcdr v x))))
    (eeprint x))
   ((eq ch 'w)
    (if
     (eqn v 0)
     (setq x
      (cons (list (car x) (cadr x)) (cddr x)))
     (rplacd
      (nthcdr (- v 1) x)
      (cons
       (list (nth v x) (nth (plus v 1) x))
       (nthcdr (plus v 2) x))))
    (eeprint x))
   ((eq ch 'p)
    (erase_page)
    (pprint x)
    (cr)
    (readcc)
    (eeprint x))
   ((eq ch 'l)
    (set_cursor 25 1)
    (print 'locate:)
    (if
     (setq goto (locate (read) x))
     (setq v (pop goto))
     (eprint x))
    (eeprint x))
   ((eq ch '+)
    (setq x (eeinsert v x (pop JEMMA)))
    (eprint x))
   ((eq ch 'e)
    (set_cursor 25 1)
    (print 'EVAL:)
    (eeinsert v x (eval (read)))
    (eeprint x))
   ((eq ch '-) (setq EXIT t))
   ((eq ch 'z)
    (if (identp THIS) (set THIS (nedit (eval THIS))))
    (setq EXIT nil)
    (eeprint x))
   (t
    (erase_page)
    (pprint
     (quote
      ((numerot = ylos alas sisaan ulos etc)
       (l S = etsi S)
       (n S = tunge tahan S)
       (e S = tunge tahan (eval S))
       (y = poista tama)
       (p = nayta kunnolla)
       (r = poista sulut)
       (a = lisaa sulut)
       (w = yhdista kaksi)
       (s = korvaa tama talla)
       (b = tama tublana)
       (v = vaihda 2 keskenaan)
       (z = editoi tunnuksen arvoa)
       (c = jatka tata listaa sita seuraavalla)
       (f = virkista naytto)
       (k = fl kopio tasta)
       (q = tahan kojootti)
       (- = ulos kaikesta)
       (h = hexa-tulostus JUU/EI))))
    (readcc)
    (eeprint x))))
 (erase_page)
 x)

(defun eeprint25
 (x)
 (sp)
 (sp)
 (cond
  ((atom x) (print x))
  ((arrayp x) (print x))
  (t
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
    (printc 41))))
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
 (eeinsert locate koe depthless nedit eeprint25 eeprint orderp
  merge1 nmerge1 nmerge split mergesort fib save BOOTPY))
