
The purpose of this project seems to be now that I can dick around in Lisp-environment using Nokolisp-editor and easily produce errorfree python code.

Has python-like primitives like "return", which is (throw return) and the lambda has the (catch return).  And "global" which initiates and imports variables to/from python globals()-environment

Nokolisp had no strings, but I invented new practise: a flat list of numbers with first number as 34, is prettyprinted as string in the editor. Then you can edit the numberlist normally and the editor shows range(32,256) as characters alongsside.

Now with flags -e, -f, -s etc, which are defined at the end of nokolisp.py . 

Problems with logical falsehood continue. Now the symbol guoted "False" is the best bet for the Falsehood, if you are to "comppy" a function. 

New macros: iff, condf and casef are for the expressions in comppy.  There is a generic solution but we are not going to implement, because we want this layer to be as 1-to-1 pythonic as possible.

"compile" is just the macroexpand. "comppy" translates to python in situ. "uncompile" reverses them both.
