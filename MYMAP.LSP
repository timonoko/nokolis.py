
(progn
 (defq MODULE MYMAP)
 (defq koti (lambda (zoom) (showimage (mymap 60.1945 24.9397 zoom)) (readcc) (killdisplay)))
 (defq
  mymap
  (lambda
   (lat lon zoom)
   (setq eka (maptile lat lon zoom))
   (setq im (googlemap (car eka) (cadr eka) zoom))
   (setq x (* 256 (- (car eka) (int (car eka)))))
   (setq y (* 256 (- (cadr eka) (int (cadr eka)))))
   (cross im x y)))
 (defq MYMAP (koti mymap MYMAP cross))
 (defq
  cross
  (lambda
   (im x y size color)
   (unless color (setq color RED))
   (unless size (setq size 10))
   (imagedraw im (list x (- y size)) (list x (+ y size)) color)
   (imagedraw im (list (- x size) y) (list (+ x size) y) color)
   im)))
