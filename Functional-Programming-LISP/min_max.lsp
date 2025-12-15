(define (funcMax lis)
  (cond
    ((null? (cdr lis)) (car lis)) 
    ((> (car lis) (funcMax (cdr lis))) (car lis))
    (else (funcMax (cdr lis)))
    )
)

(define (funcMin lis)
  (cond
    ((null? (cdr lis)) (car lis))
    ((< (car lis) (funcMin (cdr lis))) (car lis))
    (else (funcMin (cdr lis)))
    )
)

(define (findNum lis)
  (list (funcMax lis) (funcMin lis))
)
