# Python Nokolisp
I copied best part of Peter Norvig's Python Lisp. https://norvig.com/lispy.html

But I made real Lisp lists:

(str-raw (cons 'Lets 'Go)) ==> ['Lets', 'Go']

(str-raw (list 1 2 'a 'b)) ==> [1, [2, ['a', ['b', []]]]]
