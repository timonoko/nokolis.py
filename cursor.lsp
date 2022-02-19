    
(defun set_cursor
 (v h)
 (print
  (compress
   (backquote 27 91 @ (explode v) 59 @ (explode h) 72))))

(defq erase_page (progn (repeat-times 49 (cr)) (home)))

(defq home (set_cursor 0 0))
