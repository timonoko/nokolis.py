
The purpose of this project seems to be now that I can dick around in Lisp-environment using Nokolisp-editor and easily produce errorfree python code.

Has python-like primitives like "return", which is (throw return) and the lambda has the (catch return).  And "global" which initiates and imports variables to/fron python globals()-environment.

At the end of nokolis.py are examples of generated python code.

Nokolisp had no strings, but I invented new practise: a flat list of numbers with first number as 34, is prettyprinted as string in the editor. Then you can edit the numberlist normally and the editor shows range(32,256) as chracters alongsside.

Now with flags -e, -f, -s etc, which are defined at the end of nokolisp.py . 




