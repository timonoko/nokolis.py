# Python Nokolisp
I copied best part of Peter Norvig's Python Lisp. https://norvig.com/lispy.html

But I made real Lisp lists:

(str-raw (cons 'Lets 'Go)) ==> ['Lets', 'Go']

(str-raw (list 1 2 'a 'b)) ==> [1, [2, ['a', ['b', []]]]]

And dynamic scoping in Lisp-1. To the best Nokolisp tradition. It is 50 years old soon. And I am 70 soon.

This made me happy in 1975:

(compress (reverse (explode 'INNOSTUNUTSONNI))) ==> INNOSTUNUTSONNI
