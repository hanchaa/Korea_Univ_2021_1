#include <linux/syscalls.h>
#include <linux/kernel.h>
#include <linux/linkage.h>
#include <linux/slab.h>

typedef struct queue_node {
    int data;
    struct queue_node *next;
} Node; // 큐의 노드로 사용되는 구조체

typedef struct queue {
    Node *front; // 큐의 첫번째 노드를 가르키는 포인터
    Node *rear; // 큐의 마지막 노드를 가르키는 포인터
    int size; // 큐에 현재 들어있는 노드의 개수를 나타내는 변수
} Queue; // 큐의 정보를 가지고 있는 구조체

Queue q;

SYSCALL_DEFINE1(oslab_enqueue, int, a) {
    Node *i = q.front; // loop에서 사용할 변수

    if (temp == NULL) {
        printk(KERN_INFO "[Error] - QUEUE IS FULL--------------------\n");
        return -2;
    } // 메모리가 남아있지 않다면 큐가 꽉 찼다고 출력하며 함수 종료

    while (i != NULL) {
        if (i->data == a) {
            printk(KERN_INFO "[Error] - Duplicate integer in queue--------------------\n");
            return -2;
        }
        i = i->next;
    } // 큐의 첫 번째 노드부터 마지막 노드까지 지나가면서 중복된 데이터가 있는지 확인

    printk(KERN_INFO "[System call] oslab_enqueue(); -----\n");

    Node *temp = (Node *)kmalloc(sizeof(Node), GFP_KERNEL); // malloc을 통해서 새로 추가할 데이터를 담은 노드를 생성
    temp->data = a;
    temp->next = NULL;

    if (q.size == 0) { // 큐가 비어있다면 프론트와 리어 노드를 모두 새 노드로 할당
        q.front = q.rear = temp;
    }
    else { // 큐의 마지막 노드의 다음 노드로 새 노드 할당 / 큐의 리어 노드를 새 노드로 변경
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
    Node *i = NULL; // loop에 사용될 변수
    Node *temp = NULL; // pop 되는 노드를 임시로 저장할 변수
    int res = 0; // pop 되는 값을 저장할 변수

    if (q.size == 0) { // 큐가 비어있다면 비었다고 출력 후 함수 종료
        printk(KERN_INFO "[Error] - EMPTY QUEUE--------------------\n");
        return -2;
    }

    printk(KERN_INFO "[System call] oslab_dequeue(); -----\n");

    temp = q.front;
    res = temp->data;
    q.front = temp->next;
    q.size -= 1;
    kfree(temp);
    // 큐의 프론트 노드를 pop 후 res에 pop 된 노드의 data를 옮기고 큐의 프론트 노드는 pop 된 노드의 다음 노드로 변경, 큐에 들어있는 노드 개수 감소, pop 된 노드는 메모리 할당 해제

    printk(KERN_INFO "Queue Front--------------------\n");

    i = q.front;
    while (i != NULL) {
        printk(KERN_INFO "%d\n", i->data);
        i = i->next;
    }

    printk(KERN_INFO "Queue Rear--------------------\n");

    return res;
}
