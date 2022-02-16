
'((16 / 2 - 2022) (19 : 46 : 41 78))
(defq *package* BOOTPY)

(defmacro forr
 ((varb alku loppu steppi) . body)
 (if steppi () (setq steppi 1))
 (backquote lett
  ((, varb , alku))
  (repeat-times
   (/ (- (+ , loppu , steppi) , alku) , steppi)
   @ body
   (setq , varb (plus , varb , steppi)))))

(defq backquote (macro (ZYKSX) (blockq2 ZYKSX)))

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

(defmacro lett
 (vars . rest)
 (backquote
  (quote
   (lambda , (if (caar vars) (mab car vars) vars) @ rest))
  @
  (if (caar vars) (mab cadr vars))))

(defun mab
 (m%f m%x)
 (if m%x
  (cons (m%f (car m%x)) (mab m%f (cdr m%x)))))

(defun blockq2
 (XYPY)
 (cond
  ((atom XYPY) XYPY)
  ((eq (car XYPY) ',)
   (list 'cons (cadr XYPY) (blockq2 (cddr XYPY))))
  ((eq (car XYPY) '@)
   (list 'append (cadr XYPY) (blockq2 (cddr XYPY))))
  ((atom (car XYPY))
   (list
    'cons
    (list 'quote (car XYPY))
    (blockq2 (cdr XYPY))))
  ((equal (car XYPY) '',)
   (list
    'cons
    (list 'list 'quote (cadr XYPY))
    (blockq2 (cddr XYPY))))
  (t
   (list 'cons (blockq2 (car XYPY)) (blockq2 (cdr XYPY))))))

(defq BOOTPY (forr backquote save lett mab blockq2 BOOTPY))
