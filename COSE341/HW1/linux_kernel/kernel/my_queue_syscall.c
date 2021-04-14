#include <linux/syscalls.h>
#include <linux/kernel.h>
#include <linux/linkage.h>
#include <linux/slab.h>

typedef struct queue_node {
    int data;
    struct queue_node *next;
} Node;

typedef struct queue {
    Node *front;
    Node *rear;
    int size;
} Queue;

Queue q;

SYSCALL_DEFINE1(oslab_enqueue, int, a) {
    Node *i = q.front; // variable used for iteration
    Node *temp = (Node *)kmalloc(sizeof(Node), GFP_KERNEL);

    if (temp == NULL) {
        printk(KERN_INFO "[Error] - QUEUE IS FULL--------------------\n");
        return -2;
    } // check whether there is space for new data

    while (i != NULL) {
        if (i->data == a) {
            printk(KERN_INFO "[Error] - Duplicate integer in queue--------------------\n");
            return -2;
        }
        i = i->next;
    } // check there exists duplicate integer in queue

    printk(KERN_INFO "[System call] oslab_enqueue(); -----\n");

    temp->data = a;
    temp->next = NULL;

    if (q.size == 0) {
        q.front = q.rear = temp;
    }
    else {
        (q.rear)->next = temp;
        q.rear = temp;
    }

    q.size += 1;

    printk(KERN_INFO "Queue Front--------------------\n");

    i = q.front;

    while (i != NULL) {
        printk(KERN_INFO "%d\n", i->data);
        i = i->next;
    }

    printk(KERN_INFO "Queue Rear--------------------\n");

    return a;
}

SYSCALL_DEFINE0(oslab_dequeue) {
    Node *i = NULL; // variable used for iteration
    Node *temp = NULL;
    int res = 0;

    if (q.size == 0) {
        printk(KERN_INFO "[Error] - EMPTY QUEUE--------------------\n");
        return -2;
    }

    printk(KERN_INFO "[System call] oslab_dequeue(); -----\n");

    temp = q.front; // pop integer from queue
    res = temp->data;
    q.front = temp->next;
    q.size -= 1;
    kfree(temp);

    printk(KERN_INFO "Queue Front--------------------\n");

    i = q.front;
    while (i != NULL) {
        printk(KERN_INFO "%d\n", i->data);
        i = i->next;
    }

    printk(KERN_INFO "Queue Rear--------------------\n");

    return res;
}
