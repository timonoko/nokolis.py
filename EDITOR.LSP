
(progn
 (defq MODULE EDITOR)
 (defq compile-edit (lambda () (map compile '(depthless eeprint25 eeprint locate))))
 (defq
  edit
  (nlambda
   (THISNAME)
   (setq e (list 'edit THISNAME))
   (uncompile THISNAME)
   (setq EXIT ())
   (when
    (identp THISNAME)
    (if
     MODULE
     (if
      (not (member THISNAME (eval MODULE)))
      (set MODULE (cons THISNAME (eval MODULE))))
     (progn (setq MODULE 'NEW) (setq NEW (list 'NEW THISNAME))))
    (if
     (not (member MODULE (eval MODULE)))
     (set MODULE (cons MODULE (eval MODULE))))
    (set THISNAME (nedit (copy (eval THISNAME)))))
   THISNAME))
 (defq
  eeinsert
  (lambda
   (v x y)
   (if
    (lessp v 1)
    (setq x (cons () x))
    (rplacd (nthcdr (plus v -1) x) (cons () (nthcdr v x))))
   (if
    y
    (rplaca (nthcdr v x) y)
    (progn
     (eeprint x)
     (set_cursor (plus v 2) 4)
     (printc 9)
     (rplaca (nthcdr v x) (readline))))
   x))
 (defq
  locate
  (lambda
   (x y)
   (if
    (atom y)
    nil
    (if
     (member x y)
     (list (sub1 (length (member x (reverse y)))))
     ((function
       (lambda
        (z z2)
        (while
         (and y (not z2))
         (if
          (setq z2 (locate x (prog1 (car y) (setq y (cdr y)))))
          ()
          (setq z (add1 z))))
        (if z2 (cons z z2))))
      0
      ())))))
 (defq
  depthless
  (lambda
   (n x)
   (if
    (> 0 n)
    0
    (if
     (atom x)
     (- n 1)
     (depthless (depthless n (car x)) (cdr x))))))
 (defq
  nedit
  (lambda
   (x dept goto exit v)
   (setq x (copy x))
   (setq vasen-sulku (compress (list 40)))
   (if (null x) (setq x (list 'tyhja)))
   (if goto (setq v (pop goto)))
   (if (null dept) (setq dept 0))
   (if (null arrayp) (defun arrayp () ()))
   (if (null v) (setq v 0))
   (erase_page)
   (eeprint x)
   (while
    (and (not exit) (not EXIT))
    (setq THIS (nth v x))
    (if
     goto
     (setq ch 6)
     (progn
      (set_cursor 2 1)
      (progn
       (repeat-times
        (length x)
        (sp)
        (sp)
        (sp)
        (sp)
        (sp)
        (sp)
        (cr))
       (printc 41)
       (sp)
       (sp)
       (sp)
       (sp)
       (sp))
      (set_cursor (+ v 2) 3)
      (print '===>)
      (repeat-times (- (+ 1 (length x)) v) (cr))
      (repeat-times 60 (print '-))
      (cr)
      (setq ch (readcc))
      (if (member ch '(111 40 13 32)) (setq ch 110))
      (if (eqn ch 27) (setq ch (readcc)))
      (if
       (member ch '(0 91))
       (setq ch (plus 200 (readcc)))
       (setq ch (compress (list ch))))))
    (case
     ch
     (6
      (print goto)
      (if
       (atom THIS)
       ()
       (rplaca (nthcdr v x) (nedit THIS (add1 dept) goto)))
      (setq goto nil)
      (eeprint x))
     ((275 268) (setq exit t))
     ((280 266)
      (if (lessp v (length x)) (setq v (plus v 1))))
     ((272 265) (if (greaterp v 0) (setq v (plus v -1))))
     ((277 267)
      (if
       (and (atom THIS) (not (identp THIS)))
       ()
       (rplaca
        (nthcdr v x)
        (if
         (identp THIS)
         (compress (nedit (explode THIS)))
         (if
          (arrayp (nth v x))
          (list2array (nedit (array2list (nth v x))))
          (nedit (nth v x))
          ()))))
      (unless EXIT (eeprint x)))
     (n (setq x (eeinsert v x)) (eeprint x))
     (y
      (push THIS JEMMA)
      (if
       (eqn v 0)
       (setq x (cdr x))
       (rplacd (nthcdr (- v 1) x) (nthcdr (+ v 1) x)))
      (eeprint x))
     (q
      (rplaca (nthcdr v x) (list 'quote (nth v x)))
      (eeprint x))
     (r
      (if
       (eqn v 0)
       (setq x (append (nth v x) (nthcdr (plus v 1) x)))
       (rplacd
        (nthcdr (plus v -1) x)
        (append (nth v x) (nthcdr (plus v 1) x))))
      (eeprint x))
     (a (rplaca (nthcdr v x) (list (nth v x))) (eeprint x))
     (b
      (if
       (eqn v 0)
       (setq x (cons (copy (car x)) x))
       (rplacd
        (nthcdr (- v 1) x)
        (cons (copy (nth v x)) (nthcdr v x))))
      (eeprint x))
     (w
      (if
       (eqn v 0)
       (setq x (cons (list (car x) (cadr x)) (cddr x)))
       (rplacd
        (nthcdr (- v 1) x)
        (cons
         (list (nth v x) (nth (plus v 1) x))
         (nthcdr (plus v 2) x))))
      (eeprint x))
     (p (erase_page) (cr) (pprint x 1 True) (cr) (readcc) (eeprint x))
     (l
      (print 'locate:)
      (if (setq goto (locate (readline) x)) (setq v (pop goto)))
      (eeprint x))
     (+ (setq x (eeinsert v x (copy (pop JEMMA)))) (eeprint x))
     (e (print 'EVAL:) (eeinsert v x (eval (readline))) (eeprint x))
     (- (setq EXIT t))
     (z
      (if
       (and (identp THIS) (not (equal (type (eval THIS)) (type car))))
       (eval (list 'edit THIS)))
      (setq EXIT nil)
      (eeprint x))
     (c
      (if
       (atom THIS)
       ()
       (if
        (eqn v 0)
        (setq x (cons (append (car x) (list (cadr x))) (cddr x)))
        (rplacd
         (nthcdr (- v 1) x)
         (cons
          (append (nth v x) (list (nth (plus v 1) x)))
          (nthcdr (plus v 2) x)))))
      (eeprint x))
     (v
      (when
       (cdr (nthcdr v x))
       (setq ch (nth v x))
       (rplaca (nthcdr v x) (car (nthcdr (add1 v) x)))
       (rplaca (nthcdr (add1 v) x) ch)
       (setq v (add1 v)))
      (eeprint x))
     (f (eeprint x))
     (k (setq x (copy x)) (eeprint x))
     (s
      (print 'SUBST:)
      (setq eka (readline))
      (print 'WITH:)
      (setq toka (readline))
      (setq x (subst eka toka x))
      (eeprint x))
     (m (setq x (eeinsert v x (explode (read-str)))) (eeprint x))
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
         (m = lisää merkkijono)
         (h = hexa-tulostus JUU/EI))))
      (readcc)
      (eeprint x))))
   x))
 (defq
  eeprint25
  (lambda
   (x dec)
   (printc 9)
   (cond
    ((numberp x)
     (print x)
     (printc 9)
     (if (< 32 x 256) (print (compress (list x)))))
    ((atom x) (print x))
    ((arrayp x) (print x))
    ((and (flat x) (equal 34 (car x))) (print x True))
    (t
     (setq dec 10)
     (printc 40)
     (while
      x
      (cond
       ((atom x) (printc 46) (sp) (print x) (setq x nil))
       ((lessp dec 0) (print '&))
       ((atom (car x)) (print (car x)) (if (cdr x) (sp)))
       ((< 1 (depthless dec (car x))) (print (car x)))
       (t (print '&) (sp)))
      (setq dec (plus dec -3))
      (pop x))
     (printc 41)))))
 (defq
  eeprint
  (lambda
   (x)
   (erase_page)
   (printc 40)
   (repeat-times 40 (sp))
   (print THISNAME)
   (sp)
   (print MODULE)
   (cr)
   ((function
     (lambda
      (p)
      (repeat-times
       (quotient (difference (plus 39 1) 0) 1)
       (if (nthcdr p x) (progn (eeprint25 (nth p x)) (cr)))
       (setq p (plus p 1)))))
    0)
   (printc 41)))
 (defq
  set_cursor
  (lambda
   (v h)
   (print (compress (backquote 27 91 @ (explode v) 59 @ (explode h) 72)))))
 (defq erase_page (progn (repeat-times 10000 (sp)) (home)))
 (defq home (set_cursor 0 0))
 (defq EDITOR (compile-edit edit eeinsert locate depthless nedit eeprint25 eeprint set_cursor erase_page home EDITOR)))
