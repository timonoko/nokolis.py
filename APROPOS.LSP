
(progn
 (defq MODULE APROPOS)
 (defq
  autocomp
  (lambda
   ()
   (setq n 100)
   (setq w (list (readcc)))
   (while
    (< 1 n)
    (setq y (apro (print (compress (reverse w)))))
    (cr)
    (pprint (sort y))
    (cr)
    (if (< 1 (setq n (length y))) (push (readcc) w)))
   (car y)))
 (defq
  apro
  (lambda
   (x)
   (sort
    (map
     compress
     (hai
      (setq x (explode x))
      (map explode (oblist))
      (- (length x) 1))))))
 (defq
  hai
  (lambda
   (x y n)
   (if
    y
    (if
     (setq y (hui x y n))
     (if (= n 0) y (hai x y (- n 1)))))))
 (defq
  hui
  (lambda
   (x y n)
   (if
    y
    (if
     (equal (nth n x) (nth n (car y)))
     (cons (car y) (hui x (cdr y) n))
     (hui x (cdr y) n)))))
 (defq APROPOS (autocomp apro hai hui APROPOS)))
