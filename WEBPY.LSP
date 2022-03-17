
(progn
 (defq MODULE WEBPY)
 (defq
  webbi
  (lambda
   (port web)
   (progn
    (print-nice (34 105 109 112 111 114 116 32 119 101 98))
    (cr)
    (print-nice
     (34 119 101 98 46 99 111 110 102 105 103
      46 100 101 98 117 103 61 70 97 108 115
      101))
    (cr)
    (print-nice (34 99 108 97 115 115 32 100 97 116 111 106 97 58))
    (cr)
    (print-nice
     (34 32 117 114 108 115 61 40 39 47 39
      44 39 105 110 100 101 120 39 41))
    (cr)
    (print-nice (34 99 108 97 115 115 32 105 110 100 101 120 58))
    (cr)
    (print-nice
     (34 32 100 101 102 32 71 69 84 40 115
      101 108 102 41 58))
    (cr)
    (print-nice (34 32 32 32 114 101 116 117 114 110 32))
    (html web)
    (cr)
    (cr))
   (foreach
    (x web)
    (progn
     (print 'datoja.urls+=)
     (printc 40)
     (printc 39)
     (print '/)
     (print (car x))
     (printc 39)
     (print ',)
     (printc 39)
     (print (car x))
     (printc 39)
     (printc 41)
     (cr))
    (progn
     (print 'class)
     (sp)
     (print (car x))
     (print ':)
     (cr)
     (sp)
     (sp)
     (print 'def)
     (sp)
     (print 'GET)
     (print '(self))
     (print ':)
     (cr)
     (progn
      (sp)
      (sp)
      (sp)
      (print 'lsp)
      (printc 40)
      (printc 34)
      (print (list 'setq 'RESULT (cons 'progn (cdr x))))
      (printc 34)
      (printc 41))
     (cr)
     (print-nice (34 32 32 32 114 101 116 117 114 110 32))
     (html web)
     (cr)
     (cr)))
   (progn
    (print-nice
     (34 111 115 46 101 110 118 105 114 111 110
      91 34 80 79 82 84 34 93 61 34))
    (print port)
    (printc 34)
    (cr)
    (print-nice
     (34 97 112 112 32 61 32 119 101 98 46
      97 112 112 108 105 99 97 116 105 111 110
      40 100 97 116 111 106 97 46 117 114 108
      115 44 103 108 111 98 97 108 115 40 41
      41))
    (cr)
    (print-nice (34 97 112 112 46 114 117 110 40 41))
    (cr))))
 (defq WEBPY (web-site testi html print-nice WEBPY webbi))
 (defq print-nice (nlambda (x) (print (compress (cdr x)))))
 (defq
  html
  (lambda
   (web)
   (print-nice (34 34 34 34))
   (print-nice (34 60 104 116 109 108 62))
   (cr)
   (print-nice
    (34 34 34 34 43 108 115 112 40 34 82
     69 83 85 76 84 34 41 43 34 34 34))
   (print '<p><p>)
   (cr)
   (foreach
    (x web)
    (print-nice (34 60 97 32 104 114 101 102 61))
    (print (car x))
    (print '>)
    (print (car x))
    (print-nice (34 60 97 62 60 112 62))
    (cr))
   (print-nice (34 60 47 104 116 109 108 62))
   (cr)
   (print-nice (34 34 34 34))))
 (defq
  testi
  (lambda
   (x)
   (with-out-file 'tempo.py (webbi 6789 web-site))
   (python-exec (file2str 'tempo.py))))
 (defq
  web-site
  ((A (print 'AAA) (cr) 'Tilanne=AAA)
   (B (print 'EEE) (cr) 'TILANNE:BEE)
   (hapa (print 'HAPPAA) (cr) 'TLOS:HAPA))))
