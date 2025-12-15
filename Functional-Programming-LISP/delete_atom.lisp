(define (deleteatom a lis)
  (cond
    ((null? lis) '())
    ((eq? (car lis) a) (deleteatom a (cdr lis)))
    (else (cons (car lis) (deleteatom a (cdr lis))))
  )
)
