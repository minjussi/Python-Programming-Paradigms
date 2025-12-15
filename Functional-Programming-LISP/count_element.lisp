(define (countElement x aList)
  (cond
    ((null? aList) 0)
    ((eq? (car aList) x) (+ 1 (countElement x (cdr aList))))
    (else (countElement x (cdr aList)))
  )
)
