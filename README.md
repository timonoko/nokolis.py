# Python Nokolisp
I copied best part of Peter Norvig's Python Lisp. https://norvig.com/lispy.html

But I made real Lisp lists:

(str-raw (cons 'Lets 'Go)) ==> ['Lets', 'Go']

(str-raw (list 1 2 'a 'b)) ==> [1, [2, ['a', ['b', []]]]]

Print Novelty: if X[2] exists X is not a LispList, but a Python Array:

(list2array '(1 2 3)) ==> [1, 2, 3]

(list2array '(1 2)) ==> (1  .  2 )
