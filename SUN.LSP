
(progn
 (defq MODULE SUN)
 (defq
  eka
  (lambda
   (paper)
   (progn
    (global RED)
    (global GREEN)
    (global BLACK)
    (global WHITE)
    (global YELLOW)
    (global GREY '(80 80 80))
    (global WID 1000)
    (global HEI 700)
    (global MAX (int (sun_alt 6 21 10 1)))
    (global MIN (int (sun_alt 12 22 10 1)))
    (global KUVA 0)
    (setq KUVA (newimage WID HEI (iff paper WHITE BLACK)))
    (imagetext
     KUVA
     '(30 30)
     (list 'FreeSans.ttf 30 (iff paper '(80 80 0) YELLOW))
     (compress
      (cdr
       (quote
        (34 83 85 78 32 65 78 71 76 69 32
         64 32 72 69 76 83 73 78 75 73)))))
    (imagetext
     KUVA
     '(30 70)
     (list 'FreeSans.ttf 30 (iff paper '(80 80 0) YELLOW))
     (compress
      (cdr
       (quote
        (34 69 86 69 82 89 32 77 79 78 84
         72 44 32 68 65 89 32 38 32 72 79
         85 82))))))
   (defun
    ycoord
    (y)
    (int (- HEI (* HEI (/ (- y MIN) (- MAX MIN))))))
   (defun
    xcoord
    (m d)
    (int
     (*
      WID
      (/ (+ (* 30 (- m 1)) (- d 1)) 360))))
   (for
    (a MIN MAX)
    (imagetext
     KUVA
     (list 0 (ycoord a))
     (list 'FreeSans.ttf 10 (iff paper BLACK WHITE))
     (int a))
    (imagedraw KUVA (list 0 (ycoord a)) (list WID (ycoord a)) GREY)
    (if
     (= 0 (% (int a) 10))
     (progn
      (print a)
      (imagedraw
       KUVA
       (list 0 (ycoord a))
       (list WID (ycoord a))
       (iff paper '(80 80 0) YELLOW)))))
   (for
    (m 1 12)
    (imagetext
     KUVA
     (list (xcoord m 1) (- HEI 15))
     (list 'FreeSans.ttf 15 (iff paper '(80 80 0) YELLOW))
     m)
    (imagedraw
     KUVA
     (list (- (xcoord m 1) 1) (- HEI 11))
     (list (- (xcoord m 1) 1) 0)
     (iff paper '(80 80 0) YELLOW))
    (for
     (d 1 28 3)
     (imagetext
      KUVA
      (list (xcoord m d) (- HEI 11))
      (list 'FreeSans.ttf 10 (iff paper BLACK WHITE))
      d)
     (imagedraw
      KUVA
      (list (xcoord m d) (- HEI 11))
      (list (xcoord m d) 0)
      GREY)))
   (for
    (h 3 21)
    (setq h2 (- h 2))
    (print h)
    (cr)
    (setq
     COLOR
     (if
      (< h 13)
      (iff paper '(0 120 0) GREEN)
      (iff paper '(120 0 0) RED)))
    (setq x2 0)
    (setq y2 0)
    (for
     (m 1 12)
     (for
      (d 1 28 10)
      (setq alt (sun_alt m d h2 0))
      (setq y (int (ycoord alt)))
      (setq x (int (xcoord m d)))
      (if
       (and (= m 6) (= d 1))
       (imagetext KUVA (list x y) (list 'FreeSansBold.ttf 15 COLOR) h))
      (if (< y HEI) (imagedraw KUVA (list x2 y2) (list x y) COLOR))
      (setq x2 x)
      (setq y2 y))))
   (showimage KUVA)
   (saveimage KUVA 'KUVA.PNG)))
 (defq SUN (EKA SUN eka))
 (defq EKA (lambda (x) x)))
