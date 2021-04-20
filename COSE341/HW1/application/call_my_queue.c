#include <stdio.h>
#include <unistd.h>

#define my_queue_enqueue 335
#define my_queue_dequeue 336

int main() {
    int res = 0;

    res = syscall(my_queue_enqueue, 1);
    printf("Enqueue: %d\n", res);
    res = syscall(my_queue_enqueue, 2);
    printf("Enqueue: %d\n", res);
    res = syscall(my_queue_enqueue, 3);
    printf("Enqueue: %d\n", res);
    res = syscall(my_queue_enqueue, 3);
    printf("Enqueue: %d\n", res);

    res = syscall(my_queue_dequeue);
    printf("Dequeue: %d\n", res);
    res = syscall(my_queue_dequeue);
    printf("Dequeue: %d\n", res);
    res = syscall(my_queue_dequeue);
    printf("Dequeue: %d\n", res);

    return 0;
}
