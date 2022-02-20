
(progn

(defq eek
  (nlambda
   (THISNAME)
   (setq EXIT ())
   (when
    (identp THISNAME)
    (if MODULE
     (if
      (not (member THISNAME (eval MODULE)))
      (set MODULE (cons THISNAME (eval MODULE))))
     (progn
      (setq MODULE 'NEW)
      (setq NEW (list 'NEW THISNAME))))
    (if
     (not (member MODULE (eval MODULE)))
     (set MODULE (cons MODULE (eval MODULE))))
    (set THISNAME (nedit (eval THISNAME))))
   THISNAME))

(defq eeinsert
  (lambda
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
   x))

(defq locate
  (lambda
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
      (if z2 (cons z z2)))))))
 (defq depthless
  (lambda
   (n x)
   (if
    (> 0 n)
    0
    (if
     (atom x)
     (- n 1)
     (depthless (depthless n (car x)) (cdr x))))))
 (defq nedit
  (lambda
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
      (repeat-times (- (+ 1 (length x)) v) (cr))
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
      (unless EXIT (eeprint x)))
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
       (setq v (pop goto)))
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
      (if (identp THIS) (eval (list 'eek THIS)))
      (setq EXIT nil)
      (eeprint x))
     ((eq ch 'c)
      (if
       (atom THIS)
       ()
       (if
        (eqn v 0)
        (setq x
         (cons (append (car x) (list (cadr x))) (cddr x)))
        (rplacd
         (nthcdr (- v 1) x)
         (cons
          (append (nth v x) (list (nth (plus v 1) x)))
          (nthcdr (plus v 2) x)))))
      (eeprint x))
     ((eq ch 'v)
      (setq ch (nth v x))
      (rplaca (nthcdr v x) (car (nthcdr (add1 v) x)))
      (rplaca (nthcdr (add1 v) x) ch)
      (setq v (add1 v))
      (eeprint x))
     ((eq ch 'f) (eeprint x))
     ((eq ch 'k)
      (setq x (copy x))
      (eeprint x))
     ((eq ch 's)
      (set_curso 25 1)
      (print 'SUBST:)
      (setq eka (read))
      (print 'WITH:)
      (setq toka (read))
      (setq x (subst eka toka x))
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
   x))

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
 (repeat-times 40 (sp))
 (print THISNAME)
 (sp)
 (print MODULE)
 (cr)
 (for
  (p 0 22)
  (when
   (nthcdr p x)
   (tab 3)
   (eeprint25 (nth p x))
   (cr)))
 (if (nthcdr 23 x) (print '*MORE*) (printc 41)))

(defq EDITOR (eek eeinsert locate depthless nedit eeprint25 eeprint EDITOR))

(map compile EDITOR)

(setq edit eek)
)))
